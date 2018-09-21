import requests
import time

cookie = input("Paste the session cookie from your workbench session. In chrome hit f12 click network, load a page, select the first row, go to request headers and copy the cookie string.\n\n")

payload = {"Host": "workbench.sidora.si.edu"
,"Connection": "keep-alive"
,"Accept": "application/json, text/javascript, */*; q=0.01"
,"X-Requested-With": "XMLHttpRequest"
,"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
,"Referer": "https://workbench.sidora.si.edu/sidora/workbench/"
,"Accept-Encoding": "gzip, deflate, br"
,"Accept-Language": "en-US,en;q=0.9"
,"Cookie": cookie
}

while True:
    time.sleep(20)
    response = requests.get("https://workbench.sidora.si.edu/sidora/workbench/", headers=payload)
    if response.status_code != 200:
        print(response.status_code)