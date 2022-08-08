import requests, time, json
from threading import Thread
from datetime import datetime
from .models import Darckysources, Capture, Phishing

class DarkyToreq:
    def __init__(self, url, network="tor"):
        self.url = url
        self.req = requests
        self.lenght = 0
        self.content= ""
        self.network= network
    
    def _do_req(self):
        session = self.req.session()
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Cache-Control": "max-age=0"
            }
        if self.network == "tor":
            session.proxies = {
                'http' : 'socks5h://torify:9050',
                'https': 'socks5h://torify:9050'
            }
        else:
            pass
        req = session.get(self.url, headers=header)
        self.content = req.text
        self.lenght = len(self.content)
        return req.status_code
    
    def _commit_data(self):
        
        darky = Darckysources.objects(onion=self.url).first()
        if len(darky.caps): 
            Track = int(darky.caps[-1].lenght)
            if self.lenght == Track:
                print("mo commit")
                return "no commit"

        track=Capture(
                content=self.content,
                lenght=str(self.lenght),
                darky=darky
        ).save()
        darky.caps.append(track)
        darky.save()
    
    def start(self):
        self._do_req()
        self._commit_data()

    def __repr__(self) -> str:
        return f"Onion: {self.url}"

def PhishingUpdate():
    urls = [url for url in requests.get("https://openphish.com/feed.txt").text.split("\n") ]

    for url in urls:
        if url :
            exist = Phishing.objects(url=url).first()
            if not exist:
                Phishing(url=url).save()

def PhishScan(methode, word):
    headers = {
        'authority': 'phishstats.info:2096',
        'accept': '*/*',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    }
    if methode == "word":
        response = requests.get(f'https://phishstats.info:2096/api/phishing?_where=(title,like,~{word}~)~or(url,like,~{word}~)&_sort=-id',
                            headers=headers)
    elif methode == "url":
        response = requests.get(f'https://phishstats.info:2096/api/phishing?_where=(title,like,~{word}~)&_sort=-id',
                            headers=headers)
    elif methode == "cuntry":
        response = requests.get(f'https://phishstats.info:2096/api/phishing?_where=(countrycode,eq,{word})',
                            headers=headers)
    
    return response.json()

class IsPhish:
    def __init__(self, url) -> None:
        self.url = url
    def test(self):

        cookies = {
            'PHPSESSID': '8ia2p99vmuecipperpkvciolvmvugq6j',
            }

        headers = {
            'authority': 'www.phishtank.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'fr,en;q=0.9',
            'cache-control': 'max-age=0',
            # 'cookie': 'PHPSESSID=8ia2p99vmuecipperpkvciolvmvugq6j',
            'origin': 'https://www.phishtank.com',
            'referer': 'https://www.phishtank.com/index.php',
            'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'sec-gpc': '1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
        }

        data = {
            'isaphishurl': f'{self.url}',
            'formtoken': 'd4e2dfd28c0a856a58100eafb0470009',
        }

        response = requests.post('https://www.phishtank.com/index.php', cookies=cookies, headers=headers, data=data)

def job():

    PhishingUpdate()
    
    all_darkys = Darckysources.objects()

    print(len(all_darkys))
    for darky in all_darkys:
        req = DarkyToreq(
            url=darky.onion,
            network=darky.network
        )
        th = Thread(target=req.start)
        th.start()
        time.sleep(3)

#http://relateoak2hkvdty6ldp7x67hys7pzaeax3hwhidbqkjzva3223jpxqd.onion/_.dz/