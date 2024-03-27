import util
import drawutil
from drawutil import printraw

def draw_all(devices, disk_usage, charwidth):
    """
    Draws the entire device with headers and bar charts.
    """
    totalsize = util.compute_total(devices)

    draw_headers(devices, disk_usage, totalsize, charwidth)

    draw_bars(devices, disk_usage, totalsize, charwidth)

def draw_headers(devices, disk_usage, totalsize, charwidth):
    """
    Draws the header information, spacing each header based on how much space its bar will take up.
    """
    deficit_len, greatest_size = util.compute_deficit_and_greatest(devices, totalsize, charwidth)

    indent = ''
    for i, device in enumerate(devices):
        dev_size = device["size"]

        printraw(indent, color='red')
        printraw('┌', color='red')
        printraw(device["name"], color='blue')
        print('')
        printraw(indent, color='red')
        printraw('├', color='red')
        if device["mountpoints"][0]:
            printraw(device["mountpoints"][0], color='green')
        else:
            printraw("<unmntd>", color='green')
        print('')

        try:
            local_disk_usage = disk_usage["/dev/" + device["name"]]
        except KeyError:
            local_disk_usage  = {
                'space_total': device["size"],
                'space_used': 0,
                'space_avail': device["size"],
            }

        printraw(indent, color='red')
        printraw('├', color='red')
        printraw(drawutil.format_bytes(local_disk_usage['space_used']))
        printraw('/', color='red')
        printraw(drawutil.format_bytes(local_disk_usage['space_total']))

        local_disk_print_len = util.get_fixed_percent_bar_count(dev_size, totalsize, charwidth, greatest_size, deficit_len)

        indent = indent + '│'
        indent = indent + (' ' * (local_disk_print_len + 1))

        print('')

def draw_bars(devices, disk_usage, totalsize, charwidth):
    """
    Draws the actual bars, with smart spacing for each partition.
    """
    deficit_len, greatest_size = util.compute_deficit_and_greatest(devices, totalsize, charwidth)

    # Print the top of the bar
    for device in devices:
        dev_size = device["size"]

        local_disk_print_len = util.get_fixed_percent_bar_count(dev_size, totalsize, charwidth, greatest_size, deficit_len)

        draw_bar_header(local_disk_print_len)

    print('')

    # Print the contents of the bar
    for device in devices:
        dev_size = device["size"]

        try:
            local_disk_usage = disk_usage["/dev/" + device["name"]]
        except KeyError:
            local_disk_usage  = {
                'space_total': device["size"],
                'space_used': 0,
                'space_avail': device["size"],
            }

        local_disk_print_len = util.get_fixed_percent_bar_count(dev_size, totalsize, charwidth, greatest_size, deficit_len)

        draw_bar(local_disk_print_len, local_disk_usage)

    print('')

    # Print the bottom of the bar
    for device in devices:
        dev_size = device["size"]

        local_disk_print_len = util.get_fixed_percent_bar_count(dev_size, totalsize, charwidth, greatest_size, deficit_len)

        draw_bar_footer(local_disk_print_len)


    print('')

def draw_bar_header(local_disk_print_len):
    """
    Draws the top of the bar, in blue.
    """
    printraw('┌', color='blue')
    printraw('─' * local_disk_print_len, color='blue')
    printraw('┐', color='blue')

def draw_bar(local_disk_print_len, local_disk_usage):
    """
    Draws the inner portion of the bar, with green bars for consumed disk space.
    """
    used_disk_percent = local_disk_print_len * local_disk_usage['space_used'] / local_disk_usage['space_total']
    local_used_disk = (1 if used_disk_percent > 0 and int(used_disk_percent) == 0 else int(used_disk_percent))

    # this should integer-friendily equal: int(local_disk_print_len * local_disk_usage['space_avail'] / local_disk_usage['space_total'])
    local_unused_disk = local_disk_print_len - local_used_disk

    printraw('│', color='blue')
    printraw('█' * local_used_disk, color='green')
    printraw(' ' * local_unused_disk)
    printraw('│', color='blue')

def draw_bar_footer(local_disk_print_len):
    """
    Draws the bottom of the bar, in blue.
    """
    printraw('└', color='blue')
    printraw('─' * local_disk_print_len, color='blue')
    printraw('┘', color='blue')
