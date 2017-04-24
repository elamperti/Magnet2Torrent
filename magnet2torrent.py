#!/usr/bin/env python
'''

    Original author: Dan Faless (2012)
    Complete refactor: Enrico Lamperti (2017)

    GNU GENERAL PUBLIC LICENSE - Version 3

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    http://www.gnu.org/licenses/gpl-3.0.txt

'''

import shutil
import tempfile
import os
import sys
from time import sleep

import libtorrent


def magnet2torrent(magnet_file, output_name, timeout):
    if not os.path.isfile(magnet_file):
        print ("Magnet file doesn't exist")
        sys.exit(1)

    if os.path.isfile(output_name):
        print ("Destination file already exists")  # avoids overwriting
        sys.exit(1)

    # Read magnet file
    with open(magnet_file, 'r') as mf:
        magnet = mf.read()

    # Let's get going!
    temp_dir = tempfile.mkdtemp()
    session = libtorrent.session()

    params = {
        'save_path': temp_dir,
        # 'storage_mode': libtorrent.storage_mode_t(2),
        'paused': False,
        'auto_managed': True,
        # 'duplicate_is_error': True,
        'url': magnet
    }
    new_torrent = session.add_torrent(params)

    def clean_up_and_exit(with_value=0):
        # Stop the torrent
        try:
            session.remove_torrent(new_torrent)
        except:
            session.pause()

        # Remove temp directory
        if os.path.isdir(temp_dir):
            shutil.rmtree(temp_dir)

        sys.exit(with_value)

    ticks = 0
    while (not new_torrent.has_metadata()):
        try:
            # Wait for the metadata
            sleep(1)

            # Or fail if wait time was exceeded
            ticks += 1
            if ticks == timeout:
                clean_up_and_exit(1)

        except (KeyboardInterrupt, SystemExit):
            clean_up_and_exit(1)

    # Now we have the metadata the torrent needs to be paused
    # (to avoid starting the download)
    session.pause()

    # Prepare torrent file
    torrent_info = new_torrent.get_torrent_info()
    torrent_file = libtorrent.create_torrent(torrent_info)
    output = libtorrent.bencode(torrent_file.generate())

    # and save it!
    with open(output_name, "wb") as of:
        of.write(output)

    # Clean up
    clean_up_and_exit()


def main():
    if len(sys.argv) < 3:
        print("Wrong arguments (expected: magnet_file output_name [timeout])")
        sys.exit(1)

    magnet_file = sys.argv[1]
    output_name = sys.argv[2]
    try:
        timeout = int(sys.argv[3])
    except:
        timeout = 60

    magnet2torrent(magnet_file, output_name, timeout)


if __name__ == "__main__":
    main()
