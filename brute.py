import requests
import sys
import argparse
from urllib.parse import urlparse

def enum(url:str):
    if not urlparse(url).scheme:
        return f'http://{url}'
    return url

def brute(url:str,wordlist:list):
    url=enum(url)
    if not url.endswith("/"):
        url+="/"
    for word in wordlist:
        word=word.strip()
        endpoint=url+word
        try:
            r=requests.get(endpoint,timeout=0.5)
            if r.status_code!=404:
                print(f"{word}    {r.status_code}")
        except requests.exceptions.Timeout:
            print(f"Timeout with {url}")
        except requests.ConnectionError:
            print(f"failed connexion {url}")



parser=argparse.ArgumentParser()
parser.add_argument("base_url",help="The base URL to brute-force")
parser.add_argument("--wordlist",help="Path to the wordlist file",required=True)
args=parser.parse_args()

file=open(args.wordlist,"r")
wordlist=file.readlines()
file.close()
brute(args.base_url,wordlist)