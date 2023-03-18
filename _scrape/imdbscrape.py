import csv
import logging
import json
import re
from imdb import Cinemagoer

listloc = './list.csv'
extrasloc = './extras.csv'
ia = Cinemagoer()
list = []
extras = dict()
episodes = []
fnamesanitise = r"^[ .]|[/<>:\"\\|?*]+|[ .]$"

logging.basicConfig(level=logging.INFO)

with open(listloc, newline='') as listfile:
    listreader = csv.reader(listfile)
    rowindex = 0
    for row in listreader:
        if rowindex == 0:
            rowindex += 1
            continue

        epindex = str(int(float(row[0]))).rjust(3, '0')
        if (float(row[0]) % 1) != 0:
            epindex = epindex + str(round(float(row[0]) % 1, 1))[1:]

        list.append(
            {
                "epindex": epindex,
                "listindex": row[1].lower(),
                "imdbid": row[2],
                "spotifyid": row[3],
                "type": row[4].lower(),
            }
        )

        rowindex += 1

with open(extrasloc, newline='') as extrasfile:
    extrasreader = csv.reader(extrasfile)
    rowindex = 0
    for row in extrasreader:
        if rowindex == 0:
            rowindex += 1
            continue

        extras[str(row[0])] = {
            "listindex": row[0].lower(),
            "coverurl": row[1],
            "title": row[2],
            "releasedate": row[3],
            "rating": row[4],
            "plotoutline": row[5],
        }

        rowindex += 1

# for ep in list:

# the way im reading in ep is a little weird and it should probably some flavour
# of known class so that the linter can actually recognise it
for ep in list:
    print(ep["epindex"])

    if ep["type"] == 'a' or (ep["type"] == 'b' and ep["imdbid"] != None and ep["imdbid"] != ''):
        movie = ia.get_movie(ep["imdbid"])

        # some movies only have a year or a month and year, so try your best
        # to get the correct year
        if len(movie.get('original air date').split()) == 1:
            releasedate = movie.get('original air date').split()[0]
        elif len(movie.get('original air date').split()) == 2:
            releasedate = movie.get('original air date').split()[1]
        else:
            releasedate = movie.get('original air date').split()[2]

        coverurl = movie.get('cover url').replace(
            "101", "202").replace("150", "300")
        # coverurl = movie.get('cover url')

        e = {
            "epindex": ep["epindex"],
            "tfoindex": ep["listindex"],
            "imdbid": ep["imdbid"],
            "spotifyurl": "https://open.spotify.com/episode/" + ep["spotifyid"] if ep["spotifyid"] else "https://open.spotify.com/show/39lr9bBUcXgZRXsxTw1axM",
            "coverurl": coverurl,
            "title": movie.get('localized title'),
            "releasedate": releasedate,
            "rating": movie.get('rating'),
            "plotoutline": movie.get('plot outline')
        }
        # catch future bonus episodes where a film has not been selected
    elif ep["type"] == 'b':
        e = {
            "epindex": ep["epindex"],
            "tfoindex": ep["listindex"],
            "imdbid": "",
            "coverurl": "",
            "title": "upcoming bonus episode",
            "releasedate": "",
            "rating": "?",
            "plotoutline": ""
        }
    else:
        e = {
            "epindex": ep["epindex"],
            "tfoindex": ep["listindex"],
            "imdbid": "",
            "spotifyurl": "https://open.spotify.com/episode/" + ep["spotifyid"] if ep["spotifyid"] else "https://open.spotify.com/show/39lr9bBUcXgZRXsxTw1axM",
            # i am truly a terrible fucking programmer
            "coverurl": extras[ep["listindex"]]["coverurl"],
            "title": extras[ep["listindex"]]["title"],
            "releasedate": extras[ep["listindex"]]["releasedate"],
            "rating": extras[ep["listindex"]]["rating"],
            "plotoutline": extras[ep["listindex"]]["plotoutline"]
        }

    fname = f'../src/episodes/{e["epindex"]}-{re.sub(fnamesanitise, "_", e["title"].replace(" ","-"))}.md'

    out = f'---\ntags: episode\n'
    out += f'epindex: {e["epindex"]}\n'
    out += f'tfoindex: {e["tfoindex"]}\n'
    out += f'imdbid: {e["imdbid"]}\n'
    out += f'coverurl: {e["coverurl"]}\n'
    out += f'spotifyurl: {e["spotifyurl"]}\n'
    out += f'title: "{e["title"]}"\n'
    out += f'releasedate: {e["releasedate"]}\n'
    out += f'rating: {e["rating"]}\n'
    out += f'---\n\n'
    out += f'{e["plotoutline"]}'
    
    f = open(fname, 'w')
    f.write(out)
    f.close()