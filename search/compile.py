import requests
import os
from dotenv import load_dotenv
from collections import deque
from bs4 import BeautifulSoup
import tldextract
from urllib.parse import urlparse
import time
import re

load_dotenv()

max_pages = 10

# Track original URLs we've already processed (to avoid re-archiving them)
archived_urls = set()

def main():
  search_term = "Backstreet Boys"
  # get_from_gifcities(search_term)
  google_api_search(search_term)

  # NOTE: When done compiling, don't forget to run remove_top_bar.py, but only once!
  # TODO: make this better (so the top bar is removed by default??)


# ********************** USES GIFCITIES TO FIND WEBSITES ************************
# def get_from_gifcities(term):
#   try:
#     if not term:
#         raise Exception("Search query required. None currently passed")

#     url = f"https://gifcities.archive.org/api/v1/gifsearch?q={term}"

#     res = requests.get(url)
#     res.raise_for_status()

#     data = res.json()

#     urls = {item['page'] for item in data} # unique-ness

#     with open("data/scrapelist.txt", "a") as my_file:
#       my_file.write("\n")
#       my_file.write("\n".join(urls))

#   except Exception as e:
#     print(f"An error occurred: {e}")

# *********************** THESE ARE METHODS FOR CRAWLING THRU LINKS FROM ONE PAGE **************
# def main():
#     entry_point = "https://gifcities.archive.org/api/v1/gifsearch?q=charmed"  # some url that will then traverse stuff
#     url_q = deque([entry_point])  # queue of urls found from page
#     res_count = 0
#     max_links_for_try = 50
#     base_domains = set()  # A set to keep track of unique base domains

#     while len(url_q) > 0 and res_count < max_links_for_try:
#         page_url = url_q.popleft()
#         next_pgs = request_urls(page_url)  # returns a list of urls to compile next

#         # Filter out duplicate base domains from next_pgs
#         for url in next_pgs:
#             # Check if it's a web.archive.org link and handle it differently
#             print(f"Attempting to archive {url}")
#             if "web.archive.org/web" in url:
#                 original_url = extract_original_url_from_archive(url)
#                 print(f"web archive original url is: {original_url}")
#                 if original_url and original_url not in archived_urls:
#                     archived_urls.add(original_url)
#                     # Add the archive URL only if the original URL hasn't been archived yet
#                     base_domain = get_base_domain(url)
#                     if base_domain not in base_domains:
#                         base_domains.add(base_domain)
#                         res_count += 1
#                         with open("data/scrapelist.txt", "a") as my_file:
#                             my_file.write(f"{url}\n")

#         # Add the next set of URLs to the queue
#         for url in next_pgs:
#             url_q.append(url)

#         # Add a delay to avoid getting blocked (4 seconds to make 15 requests per minute)
#         time.sleep(4)

#     print(f"Successfully compiled {res_count} unique base domains.")

# def request_urls(entry_point):
#     try:
#         tmp = []  # holder for links
#         # get all urls from requesting the webpage
#         data = requests.get(entry_point)
#         data.raise_for_status()

#         html = BeautifulSoup(data.text, 'html.parser')

#         for link in html.find_all('a', href=True):
#             url = str(link.get('href'))
#             # only archive "http*" links
#             if len(url) > 4 and url[:4] == "http":
#                 tmp.append(url)

#         return tmp
#     except Exception as e:
#         print(f"Something went wrong :-( {e}")
#         return []

# def get_base_domain(url):
#     """
#     Helper function to extract the base domain from a URL (e.g., 'https://im.spacehey.com/page' -> 'spacehey.com').
#     """
#     parsed_url = tldextract.extract(url)
#     # The domain will be 'spacehey.com', without any subdomains
#     base_domain = f"{parsed_url.domain}.{parsed_url.suffix}"
#     return base_domain

# def extract_original_url_from_archive(archive_url):
#     """
#     Extracts the original URL from a Wayback Machine archive URL.
#     For example: 'https://web.archive.org/web/20091021233148/http://geocities.com/lobomagicwolf/sukee-friends'
#     will return 'http://geocities.com/lobomagicwolf/sukee-friends'..
#     """
#     try:
#         parts = archive_url.split("http://", 1)  # Split off the 'http://' part
#         if len(parts) > 1:
#             return "http://" + parts[1]  # Return the original URL after 'http://'
#         parts = archive_url.split("https://", 1)
#         if len(parts) > 1:
#             return "https://" + parts[1]  # Return the original URL after 'https://'
#         return None
#     except Exception as e:
#         print(f"Error extracting original URL: {e}")
#         return None

#******** OLD METHODS USING GOOGLE SEARCH THAT I'M TOO SCARED TO DELETE ********

def google_api_search(query):
  next_page = 0
  num_requests = 0

  while next_page is not None and num_requests < max_pages:
    next_page = request_urls(query, next_page)
    num_requests += 1

  print(f"Successfully compiled {num_requests * 10} results!")

def request_urls(query, start):
  try:
    search_url = f"https://www.googleapis.com/customsearch/v1?key={os.getenv('GOOGLE_KEY')}&cx={os.getenv('GOOGLE_CUSTOM_ENGINE_ID')}&q={query}&start={start}"
    res = requests.get(search_url)
    res.raise_for_status()

    res = res.json()

    has_next_page = "nextPage" in res["queries"]

    processed_urls = [i["link"] for i in res["items"]]

    with open("data/scrapelist.txt", "a") as my_file:
      my_file.write("\n")
      my_file.write("\n".join(processed_urls))

    if not has_next_page or res["queries"]["nextPage"][0]["startIndex"] > 100:
      return None

    return res["queries"]["nextPage"][0]["startIndex"]

  except Exception as e:
    print(e)
    print("Something went wrong :-(")

if __name__=="__main__":
  main()