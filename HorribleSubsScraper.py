import requests
from bs4 import BeautifulSoup
import re
import time

# template urls
searchurl = 'https://nyaa.si/user/HorribleSubs?f=0&c=0_0&q={}&o=desc&p={}'
downloadurl = 'https://nyaa.si{}'
downloadfolder = 'downloaded' # set in your torrent client the automatic upload of torrents from this folder to completely automatizew the process
quality = ["[480p]", "[720p]", "[1080p]"]
order = ["asc", "desc"]

# get user input
anime = input("Enter anime name (as uploaded by HorribleSubs): ")

while True:
    try:
        qselector = int(input("Select quality:\n0 = 480p\n1 = 720p\n2 = 1080p\n"))
        if qselector not in [0, 1, 2]:
            print("Enter a valid number: 0, 1 or 2")
        else:
            break

    except ValueError:
        print("Enter a valid number: 0, 1 or 2")

print("Now enter the range of episodes you want to download. \nFor example to download all episodes between and including episodes 1 and 10, enter 1 and then 10.")
minepisode = int(input("Enter the episode you want to start downloading from:\n"))
maxepisode = int(input("Enter the episode you want to stop downloading at:\n"))

# define number of pages to scrape: web page contains 25 distinct episodes (x3 qualities)
# need latest episode to get correct number of pages
latest_ep = int(re.search(r'[HorribleSubs].+-\s(\d+)', requests.get(searchurl.format(anime, '')).text).group(1))
n_pages = (latest_ep - minepisode)//25 + 1

# set quality to search
q = quality[qselector]

for p in range(1, n_pages+1):

    url = searchurl.format(anime, p)
    html = requests.get(url).text
    parser=BeautifulSoup(html, "html.parser")

    rows = parser.find_all('tr', class_ = "success")

    pag_episodes = {}
    for r in rows:

        episode = {}

        # get list of elements that contain links
        rowelements = r.find_all('a')
        for elem in rowelements:
            if elem.has_attr('title') and anime.upper() in elem['title'].upper():
                eptitle = elem['title']
                epnumber = int(re.search(r'[HorribleSubs].+-\s(\d+)', elem['title']).group(1))
                episode['num'] = epnumber
                break

        endpoints = r.find_all('td', class_='text-center')[0].find_all('a')

        episode['download'] = endpoints[0]['href']
        episode['magnet'] = endpoints[1]['href']

        pag_episodes[eptitle] = episode

    for eptitle in pag_episodes:
        epnumber = pag_episodes[eptitle]['num']
        endpoint = pag_episodes[eptitle]['download']

        if minepisode <= epnumber <= maxepisode and q in eptitle:

            print(epnumber, downloadurl.format(endpoint))

            torrent = requests.get(downloadurl.format(endpoint))
            with open('{}/{}.torrent'.format(downloadfolder, eptitle), 'wb') as f:
                f.write(torrent.content)

            time.sleep(1)
