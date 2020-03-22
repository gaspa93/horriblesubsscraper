# horriblesubsscraper
An application to automatically download HorribleSubs torrents from nyaa.si.

This scraper will search for the entered show at the selected quality on HorribleSubs page on nyaa.si and download the torrent in the specified folder.

# Features
* searches for shows using the same search engine as on nyaa.si
* allows user to select quality (480p, 720p or 1080p)
* select range of episodes to download, including episodes with decimals e.g. 13.5
* doesn't download premade batch files which are already available by HorribleSubs on nyaa.si
* loads torrents from latest uploaded to nyaa.si

**Soon:**
* use horriblesubs.info instead of nyaa.si
* optimise how the number of pages are found, based on the episodes range input
* add validation to episodes range input

# Requirements
* Python 3.7
* Any BitTorrent client which allows for magnet links

# Installation
* Download HorribleSubsScraper.py and run it through Python IDLE, Python 3.7+ is what it was made with.

# Usage
1. Enter the show's name as you would search for it on nyaa.si/user/HorribleSubs
2. Enter a number corresponding to the quality you want it to be downloaded in
3. Enter the range of episodes you need

# Additional information
If the specified show at the specified quality is not available, it will not be downloaded and you'd have to check that manually.

**Note**: To fully automatize the process, set the automatic load of torrents of your BitTorrent client from the folder you use in this script.
