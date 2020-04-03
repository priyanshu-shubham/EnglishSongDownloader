import requests
from bs4 import BeautifulSoup
print("""
                                        ╔═══╗
                                        ║███║
                                        ║(O)║ ♫ ♪ ♫ ♪
                                        ╚═══╝
                                 ▄ █ ▄ █ ▄ ▄ █ ▄ █ ▄ █
                                 Min●- - - - - - -●Max
                                ENGLISH SONG DOWNLOADER
                                 """)
song=input("Enter song name or artist name: ")

def getsongavailable(song):
    try:
        songnames=[]
        artists=[]
        urls=[]
        content=requests.get("https://en.muzmo.org/search?q="+"+".join(song.split()),headers={
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'})
        content=content.content.decode()
        soup=BeautifulSoup(content,"lxml")
        soup=(soup.find("div",id="ajax-wrap"))
        soup=soup.findAll("div",class_="item-song ajax-item")
        for i in soup:
            soup=i.find("tr")
            artist=soup.a.b.text
            songname=list(soup.find("br").next_siblings)[0].strip()
            songnames.append(songname)
            artists.append(artist)
            url=soup.a["href"]
            urls.append(url)
        songs={"songnames":songnames,"artists":artists,"urls":urls}
        return songs
    except:
        print("Song Not Found!")
        quit()
songs=getsongavailable(song)

def printsongs():
    for i in range(len(songs["urls"])):
        print("{:3d}  {}  ----   {}".format(i+1,songs["songnames"][i],songs["artists"][i]))

while True:
    try:
        printsongs()
        rchoice=(input("Enter the Song Number to download: "))
        choice=int(rchoice)
        content=requests.get("https://en.muzmo.org"+songs["urls"][choice-1],)
        soup=BeautifulSoup(content.content.decode(),"html.parser")
        downloadlink=soup.findAll("div",class_="mzmdrk")[1].a["href"]
        print("Starting Download")
        content=requests.get("https://en.muzmo.org"+downloadlink).content
        fhand=open("{}.mp3".format(songs["songnames"][choice-1]),"wb")
        fhand.write(content)
        fhand.close()
        print("Song Downloaded")
        break
    except:
        if rchoice.lower()=="q":
            quit()
        print("This Song couldn't be downloaded.Try Another.")
        print("Press Q to quit.")
