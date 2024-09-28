import requests
import argparse
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor

def enum(url: str):
    if not urlparse(url).scheme:
        return f'http://{url}'
    return url

def check_url(url: str, word: str):
    word = word.strip()
    endpoint = url + word
    try:
        r = requests.get(endpoint, timeout=0.5)
        if r.status_code != 404:
            print(f"{word}    {r.status_code}")
    except requests.exceptions.Timeout:
        print(f"Timeout with {url}")
    except requests.ConnectionError:
        print(f"Failed connection {url}")

def brute(url: str, wordlist: list, threads: int = 10):
    url = enum(url)
    if not url.endswith("/"):
        url += "/"
    
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(check_url, url, word) for word in wordlist]
        for future in futures:
            future.result()  


parser = argparse.ArgumentParser()
parser.add_argument("base_url", help="The base URL to brute-force")
parser.add_argument("--wordlist", help="Path to the wordlist file", required=True)
parser.add_argument("--threads", type=int, default=10, help="Number of threads to use")
args = parser.parse_args()

with open(args.wordlist, "r") as file:
    wordlist = file.readlines()

brute(args.base_url, wordlist, threads=args.threads)
