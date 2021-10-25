import requests
from bs4 import BeautifulSoup
import json 



def get_gclb():
    url = "https://sitereview.bluecoat.com/"
    headers = {"Host":"sitereview.bluecoat.com","User-Agent":"Mozilla/5.0","Accept":"text/html","Accept-Language":"en-US,en;q=0.5","Accept-Encoding":"gzip, deflate, br","Referer":"https://google.com"}
    response = requests.get(url,headers=headers)
    if response.status_code==200:
        gclb_cookie = response.headers.get("Set-Cookie").split(";")[0]
        return gclb_cookie
    else:
        return None
    

def get_session():
    url = "https://sitereview.bluecoat.com/resource/content/en_US"
    gclb_cookie = get_gclb()
    if gclb_cookie is None:
        print("Error level 2")
        return False
    headers = {"Host":"sitereview.bluecoat.com","User-Agent":"Mozilla/5.0","Accept-Language":"en-US,en;q=0.5","Accept-Encoding":"gzip, deflate, br","Referer":"https://sitereview.bluecoat.com/","Cookie":gclb_cookie}
    response = requests.get(url,headers=headers)
    if response.status_code == 200:
        jsession_id = response.headers.get("Set-Cookie").split(";")[0]
        return {"gclb":gclb_cookie, "jsession_id":jsession_id}
    else:
        return None

def get_csrf_token():
    url = "https://sitereview.bluecoat.com/resource/captcha-request"
    cookie = get_session()
    if cookie is None:
        print("Error level 3")
        return False
    cookie_string = cookie["gclb"]+";"+cookie["jsession_id"]
    headers = {"Host":"sitereview.bluecoat.com","User-Agent":"Mozilla/5.0","Accept-Language":"en-US,en;q=0.5","Accept-Encoding":"gzip, deflate, br","Referer":"https://sitereview.bluecoat.com/","Cookie":cookie_string}
    response = requests.get(url,headers=headers)
    csrf_token = response.headers.get("Set-Cookie").split(";")[0]
    cookie["csrf"] = csrf_token
    print(cookie)
    return cookie
  


def get_category(query_url):
    query_url = query_url.replace("https://","").replace("http://","")
    url = "https://sitereview.bluecoat.com/resource/lookup"
    cookie = get_csrf_token()
    cookie_string = cookie["csrf"]+";"+cookie["gclb"]+";"+cookie["jsession_id"]
    csrf=cookie["csrf"].replace("XSRF-TOKEN=","")
    headers = {"Host":"sitereview.bluecoat.com","User-Agent":"Mozilla/5.0","Accept-Language":"en-US,en;q=0.5","Accept-Encoding":"gzip, deflate, br","Referer":"https://sitereview.bluecoat.com/","Cookie":cookie_string,"X-XSRF-TOKEN":csrf}
    payload = {"captcha":"", "key":csrf,"phrase":"RXZlbiBpZiB5b3UgYXJlIG5vdCBwYXJ0IG9mIGEgY29tbWVyY2lhbCBvcmdhbml6YXRpb24sIHNjcmlwdGluZyBhZ2FpbnN0IFNpdGUgUmV2aWV3IGlzIHN0aWxsIGFnYWluc3QgdGhlIFRlcm1zIG9mIFNlcnZpY2U=","source":"new lookup","url":query_url}
    response = requests.post(url,json=payload,headers=headers)
    if response.status_code == 200:
        print("successful --------")
        res_json = json.loads(response.content.decode())
        q_url = res_json.get("url")
        print('*'*30)
        print("URL --> ",q_url)
        print("--Categorisation--")
        for i in res_json.get("categorization"):
            print(i["name"])
        print('*'*30)
    else:
        print("Invalid Url Entered")

get_category("google.com")