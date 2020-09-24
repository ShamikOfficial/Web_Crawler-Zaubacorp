from bs4 import BeautifulSoup as BS
import requests, json
import pandas as pd

def parser(url):
    agent = {"User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
    page=requests.get(url,headers=agent)      #requesting page using an agent
    soup = BS(page.text, 'html.parser')
    return soup
