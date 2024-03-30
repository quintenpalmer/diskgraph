#!/usr/bin/env python

import dfio
import draw

def main():
    df_json = dfio.get_df_jq_file_system_report()

    lsblk_json = dfio.get_lsblk_block_report()

    disk_usage = dfio.key_df_jq_report(df_json)

    charwidth = dfio.get_term_width()

    for blockdevices in lsblk_json["blockdevices"]:
        try:
            devices = blockdevices["children"]
        except KeyError:
            continue

        draw.draw_all(devices, disk_usage, charwidth)

if __name__ == '__main__':
    main()
