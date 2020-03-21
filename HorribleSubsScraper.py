import requests
from bs4 import BeautifulSoup
import webbrowser
import re
import time

def getrows(parser):
    return parser.find_all('tr', class_ = "success")

quality = ["[480p]", "[720p]", "[1080p]"]

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

#Add validation
print("Now enter the range of episodes you want to download. \nFor example to download all episodes between and including episodes 1 and 10, enter 1 and then 10.\nIf you want to download the whole series, just press enter. You could then manually delete the torrents you don't want to keep from your client.\n")
minepisode = int(input("Enter the episode you want to start downloading from:\n"))
maxepisode = int(input("Enter the episode you want to stop downloading at:\n"))

# define number of pages to scrape
n_pages = (maxepisode - minepisode)//25 + 1

downloadurl = 'https://nyaa.si{}'

for p in range(1, n_pages+1):

    url = 'https://nyaa.si/user/HorribleSubs?f=0&c=0_0&q='+anime+'&o=desc&p={}'.format(p)
    html = requests.get(url).text
    parser=BeautifulSoup(html, "html.parser")

    rows = getrows(parser)

    q = quality[qselector]
    for r in rows:

        # find title
        elements = r.find_all('a')
        for elem in elements:
            if anime.upper() in elem['title'].upper():
                title = elem['title']
                break

        # find quality
        ep_number = int(re.search(r'[HorribleSubs].+-\s(\d+)', title).group(1))
        if q in title and minepisode <= ep_number <= maxepisode:
            endpoint = r.find_all('td', class_='text-center')[0].find_all('a')[0]['href']

            print(title, downloadurl.format(endpoint))

            torrent = requests.get(downloadurl.format(endpoint))

            with open('downloaded/{}.torrent'.format(title), 'wb') as f:
                f.write(torrent.content)

            time.sleep(1)
