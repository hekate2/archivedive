import requests
import os
from dotenv import load_dotenv

load_dotenv()

max_pages = 10

def main():
  query = "shoegaze" # I haven't searched for this yet
  next_page = 0
  num_requests = 0

  while next_page is not None and num_requests < max_pages:
    next_page = request_urls(query, next_page)
    num_requests += 1

  print(f"Successfully compiled {num_requests * 10} results!")

def request_urls(query, start):
  try:
    search_url = f"https://www.googleapis.com/customsearch/v1?key={os.getenv('GOOGLE_KEY')}&cx=b0d824ba798db44fb&q={query}&start={start}"
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