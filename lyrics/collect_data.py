import urllib.request
from bs4 import BeautifulSoup
from time import sleep
import json
import os
import re

# url to scrape the songs list from
base_url = "https://www.song-list.net/{}/songs"

# list of artists
artists = ["arianagrande", "taylorswift"]
print('List of artists: ', artists)
songs_dict = {}

user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
headers={'User-Agent':user_agent}

for artist in artists:
    url = base_url.format(artist)
    request = urllib.request.Request(url,None,headers)
    response = urllib.request.urlopen(request)
    data = response.read()
    soup = BeautifulSoup(data, 'html.parser')
    songs = soup.find_all("div", class_="divTableCell songname")    
    songs_dict[artist] = [song.find("a").text for song in songs]
    sleep(1)


for key,val in songs_dict.items():
    print(f'Artist Name: {key}')
    print(f'Number of songs: {len(val)}')

# save the songs list to a json file
json_file = "data/artists-songs.json"
with open(json_file, 'w') as file:
    json.dump(songs_dict, file)

# get the lyrics for each song
def get_songs_list(artist):
    songs = songs_dict[artist]
    processed_songs = []

    # preprocessing the songs name
    for song in songs:
        song_name = re.sub(r'\(.*\)',"",song)
        processed_song = re.sub(r'\W+', '', song_name).lower()
        processed_songs.append(processed_song)

    # remove duplicates
    processed_songs = list(set(processed_songs))

    return processed_songs


def get_lyrics(artist):
    base_url = "https://www.azlyrics.com/lyrics/{}/{}.html"
    lyrics_file_path = f"data/lyrics/{artist}"
    if not os.path.exists(lyrics_file_path):
        os.makedirs(lyrics_file_path)

    lyrics_not_found_for = []
    delay = 10
    
    processed_songs = get_songs_list(artist)
    for song in processed_songs:
        final_url = base_url.format(artist,song)

        try:
            html_page = urllib.request.urlopen(final_url)
            soup = BeautifulSoup(html_page, 'html.parser')

            html_pointer = soup.find('div', attrs={'class':'ringtone'})
            song_name = html_pointer.find_next('b').contents[0].strip()
            lyrics = html_pointer.find_next('div').text.strip()

            song_name = song_name.replace('"', '')
            lyrics_file = f"{lyrics_file_path}/{song_name}.txt"
            with open(lyrics_file, "w") as file:
                file.write(lyrics)
        
        except:
            print("Lyrics not found for : " + song)
            lyrics_not_found_for.append(song)
        
        finally:
            sleep(delay)
        
    print(f'Total songs count: {len(songs)}')
    print(f'Lyrics found for {len(songs)-len(lyrics_not_found_for)} songs')

for artist in artists:
    print(f'Getting lyrics for {artist}')
    get_lyrics(artist)