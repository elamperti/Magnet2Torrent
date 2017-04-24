# Magnet2Torrent

A command line tool that converts magnet links in to `.torrent` files.

## Requirements
* python
* python-libtorrent (libtorrent-rasterbar version 0.16 or later)

### Ubuntu
`sudo apt-get install python-libtorrent -y`

### macOS
`brew install libtorrent-rasterbar --with-python`

## How to Use
`python Magnet_To_Torrent2.py <magnet file> <torrent file> [<timeout in seconds>]`

Timeout defaults to 60 seconds. Current implementation considers rough seconds since the torrent creation (not since program started).

## Licenses
All code is licensed under the [GPL version 3](http://www.gnu.org/licenses/gpl.html)
