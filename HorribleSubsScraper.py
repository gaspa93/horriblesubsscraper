import requests
from bs4 import BeautifulSoup
import re
import time

# template urls
searchurl = 'https://nyaa.si/user/HorribleSubs?f=0&c=0_0&q={}&o=desc&p={}'
downloadurl = 'https://nyaa.si{}'
quality = ["[480p]", "[720p]", "[1080p]"]

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

#Add validation
print("Now enter the range of episodes you want to download. \nFor example to download all episodes between and including episodes 1 and 10, enter 1 and then 10.\nIf you want to download the whole series, just press enter. You could then manually delete the torrents you don't want to keep from your client.\n")
minepisode = int(input("Enter the episode you want to start downloading from:\n"))
maxepisode = int(input("Enter the episode you want to stop downloading at:\n"))

# define number of pages to scrape: web page contains 25 distinct episodes (x3 qualities)
n_pages = (maxepisode - minepisode)//25 + 1

# set quality to search
q = quality[qselector]

for p in range(1, n_pages+1):

    url = searchurl.format(anime, p)
    html = requests.get(url).text
    parser=BeautifulSoup(html, "html.parser")

    rows = parser.find_all('tr', class_ = "success")

    for r in rows:

        # find title element and check quality
        elements = r.find_all('a')
        eptitle = None
        for elem in elements:
            if anime.upper() in elem['title'].upper() and q in elem['title']:
                eptitle = elem['title']
                break

        if eptitle is not None:

            ep_number = int(re.search(r'[HorribleSubs].+-\s(\d+)', title).group(1))
            if minepisode <= ep_number <= maxepisode:
                endpoint = r.find_all('td', class_='text-center')[0].find_all('a')[0]['href']

                print(title, downloadurl.format(endpoint))

                torrent = requests.get(downloadurl.format(endpoint))
                with open('downloaded/{}.torrent'.format(title), 'wb') as f:
                    f.write(torrent.content)

                time.sleep(1)
        else:
            print('Quality {} for {} not found'.format(q, title))
