import requests

def get_index(url):
    response=requests.get(url)
    if response.status_code == 200 :
