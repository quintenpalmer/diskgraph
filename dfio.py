import subprocess
import json
import shutil

def get_term_width():
    """
    Returns the current terminal width (with some padding space).
    """
    terminfo = shutil.get_terminal_size()
    # we subtract 4 to give a bit of extra room
    # for the last device block on a device to print header info
    # this is totally a hack
    charwidth = terminfo.columns - 4

    return charwidth

def get_lsblk_block_report():
    """
    Returns a python object representing the known devices.
    """
    # -b reports in bytes* as opposed to human-readable formats
    # * see key_df_jq_report for actual byte format returned
    # -J returns JSON
    lsblk_proc = subprocess.Popen(["lsblk", "-b", "-J"], stdout=subprocess.PIPE)

    out, error = lsblk_proc.communicate()

    lsblk_json = json.loads(out.decode('utf-8'))

    return lsblk_json

def get_df_jq_file_system_report():
    """
    Returns a python object representing the bytes used and available for all mounted devices.
    """
    # -P is a portability UNIX format flag to help with parsing
    df_proc = subprocess.Popen(["df", "-P"], stdout=subprocess.PIPE)

    # we consume the output from df and pass it into this jq monstrosity
    # all we are really doing is grabbing the lines that start with a mount-point '/'
    # and creating an object with appropriate names for the values
    jq_proc = subprocess.Popen(["jq", "-R", "-s", """
    [
      split("\\n") |
      .[] |
      if test("^/") then
        gsub(" +"; " ") | split(" ") | {mount: .[0], space_total: .[1], space_used: .[2], space_avail: .[3]}
      else
        empty
      end
    ]"""], stdin=df_proc.stdout, stdout=subprocess.PIPE)

    out, error = jq_proc.communicate()

    df_json = json.loads(out.decode('utf-8'))

    return df_json

def key_df_jq_report(v):
    """
    Keys the df | jq output on the device block names and converts from blocks to bytes for the space_ values.
    """
    ret = {}

    for entry in v:
        # the values are strings (hence the `int` conversion)
        # and they are actually a count of blocks, which are all KiB
        # so we turn them back into KB and then convert the blocks back into byte counts
        # I'm not entirely sure that the numerators and denominators are the correct 1024 vs 1000
        # but it seems to work
        entry['space_total'] = int(int(entry['space_total']) * 1024 / 1000) * 1000
        entry['space_used'] = int(int(entry['space_used']) * 1024 / 1000) * 1000
        entry['space_avail'] = int(int(entry['space_avail']) * 1024 / 1000) * 1000
        # we want to key based on the name for easy lookup later
        ret[entry["mount"]] = entry

    return ret
