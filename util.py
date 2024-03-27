def compute_total(devices):
    """
    Compute the total size of a list of devices.
    """
    totalsize = 0

    for device in devices:
        totalsize += device["size"]

    return totalsize

def compute_deficit_and_greatest(devices, totalsize, charwidth):
    """
    Compute both the deficit and greatest length of a list of devices.

    The deficit is how much room we should pull off of the largest devices
    assuming that we leave room for 2 characters on even the smallest device block.

    The greatest size is just the device block with the largest size.
    """
    deficit_len = 0
    greatest_size = 0

    for device in devices:
        dev_size = device["size"]

        local_disc_print_len = _get_raw_percent_bar_count(dev_size, totalsize, charwidth)

        if local_disc_print_len < 2:
            local_disc_print_len = 2
            deficit_len = deficit_len + (local_disc_print_len - 2)
        if dev_size > greatest_size:
            greatest_size = dev_size

    return deficit_len, greatest_size

def get_fixed_percent_bar_count(dev_size, totalsize, charwidth, greatest_size, deficit_len):
    """
    Returns the length in characters that the device block's bar chart should consume,
    taking into account how many characters need to be subtracted from the largest device block
    with the total deficit_len.
    """
    local_disc_print_len = _get_raw_percent_bar_count(dev_size, totalsize, charwidth)

    if local_disc_print_len < 2:
        local_disc_print_len = 2
    if dev_size == greatest_size:
        local_disc_print_len -= deficit_len
    if local_disc_print_len > 4:
        local_disc_print_len -= 4

    return local_disc_print_len

def _get_raw_percent_bar_count(current, total, tofit):
    """
    Gets character length for a given device block,
    given the total bytes for the drive, and the character length to fit in.
    """
    percent = current/ total
    asfit = percent * tofit
    return int(asfit)
