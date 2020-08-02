import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbsparta

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.genie.co.kr/chart/top200?ditc=D&rtm=N&ymd=20200713',headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

songs = soup.select('#body-content > div.newest-list > div > table > tbody > tr')

for song in songs:
    updown = song.select_one('span.rank')
    updown.extract() #순위변동태그(상승, 하락) 제거
    song_rank = song.select_one('td.number').text.strip()
    song_title = song.select_one('td.info > a.title.ellipsis').text.strip()
    song_artist = song.select_one('td.info > a.artist.ellipsis').text
    print(song_rank, song_title, song_artist)
    doc = {'rank': song_rank, 'title': song_title, 'artist': song_artist}
    db.genie.insert_one(doc)
