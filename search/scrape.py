## TODO: Write the web scraping function here.
from bs4 import BeautifulSoup # HTML parsing
import requests
import spacy
from keyword_spacy import KeywordExtractor
from spacy.lang.en.stop_words import STOP_WORDS
import os
from openai import OpenAI
import json
from dotenv import load_dotenv
import sqlite3
from archivenow import archivenow
import time
from yaspin import yaspin
from yaspin.spinners import Spinners
from collections import deque

load_dotenv()

# instantiate stop words with custom words
stop_words = STOP_WORDS.union({"like", "know"})

# keyword extractor setup
nlp = spacy.load("en_core_web_md")
nlp.add_pipe("keyword_extractor", last=True, config={"top_n": 10})
req_session = requests.Session()

def main():
    try:
        url_queue = deque(load_list())  # Convert to deque for fast pop from front
        cons_err_count = 0

        while url_queue:  # Keep processing while there are URLs left in the queue
            url = url_queue.popleft()  # Get the next URL to process

            with yaspin(Spinners.earth, text=f"Indexing: {url}") as spinner:
                try:
                    if not is_url_indexed(url):  # Check if the URL is indexed in the database
                        scrape_site(url, False)  # Scrape the site if it's not indexed
                        spinner.ok("✅ ")
                        cons_err_count = 0
                        time.sleep(10)  # Delay to stay within archive limits
                    else:
                        spinner.ok("✅ ")
                        cons_err_count = 0
                        print(f"URL {url} is already archived - skipping")

                except Exception as e:
                    spinner.fail("❌ ")
                    print(f"Error processing {url}: {e}")
                    cons_err_count = cons_err_count + 1

                    if cons_err_count > 10:
                       print("Encountered more than 10 consecutive errors- aborting!")
                       req_session.close()
                       break
                    # Optionally, you can re-add the URL to the queue if you'd like to retry it later
                    # url_queue.append(url)  # Uncomment this line if you want to retry failed URLs

    except Exception as e:
        print(f"An error occurred: {e}")
        print("Something went wrong, no sites were scraped.")
        req_session.close()


def is_url_indexed(url):
  conn = sqlite3.connect("data/sites.db")
  cursor = conn.cursor()

  query = "SELECT * FROM sites WHERE url LIKE ?"
  urltest = url

  if len(url) > 24 and url[:24] == "https://web.archive.org/":
     urltest = f"%{url[46:]}%"

  cursor.execute(query, (urltest,))
  result = cursor.fetchone()

  conn.close()

  return result is not None

def load_indexed():
  """
  Returns a list of sites that are in the db but might not have been archived
  """
  conn = sqlite3.connect("data/sites.db")
  cursor = conn.cursor()

  query = """
  SELECT DISTINCT url
  FROM sites
  """
  cursor.execute(query)

  res = [val[0] for val in cursor.fetchall()]
  conn.close()

  return res

def load_archived():
  """
  Returns a list of urls for websites that have already been submitted to an archive
  """
  conn = sqlite3.connect("data/sites.db")
  cursor = conn.cursor()

  query = """
  SELECT url
  FROM sites
  WHERE archive_url IS NOT NULL
  """
  cursor.execute(query)

  res = [val[0] for val in cursor.fetchall()]
  conn.close()

  return res

def load_list():
  """
  Loads the list of urls to be indexed from a text file.
  """
  # load list of urls and return as an array
  f = open('data/scrapelist.txt', 'r')
  content = f.read()
  f.close()

  return content.split("\n")

def process_raw_text(text):
  """
  Removes extra empty lines from the page text
  """
  mod_text = '\n'.join([line for line in text.splitlines() if line.strip()])

  return mod_text

def get_keywords(text):
  """
  Removes stop words and extracts keywords from text
  """
  mod_text = ' '.join([word for word in text.split() if word not in stop_words])
  doc = nlp(mod_text)
  return [n[0] for n in doc._.keywords]

def get_summary(text):
  """
  Writes a little summary about the website
  """
  try:
    response = req_session.post(
      url="https://openrouter.ai/api/v1/chat/completions",
      headers={
        "Authorization": f"Bearer {os.getenv('OPENROUTER_KEY')}"
      },
      data=json.dumps({
        "model": "openai/gpt-4o-2024-11-20", # Optional
        "messages": [
          {
            "role": "system",
            "content": "The user will give you the unorganized text contents of a webpage.  You are to respond with a two-sentence summary describing the contents of the website.  Your summary must not sound as if you're describing the website, but rather as a blurb that could appear on a search engine page."
          },
          {
            "role": "user",
            "content": text[:7000] if len(text) > 7000 else text
          }
        ]

      })
    )

    response.raise_for_status()
    res = response.json()
    return res["choices"][0]["message"]["content"]
  except Exception as e:
    print(f"ERROR: {e}")
    print("Couldn't generate summary :-/")
    return None

def scrape_site(url, archive=False):
  """
  Gets the website content, generates informatioin about it and sticks it into
  a database
  """
  data = req_session.get(url)
  # print status
  data.raise_for_status()

  html = BeautifulSoup(data.text, 'html.parser')

  page_body = html.select("body")

  if not page_body:
    # Skip processing this site
    raise Exception(f"No <body> found for URL: {url}")

  page_text = process_raw_text(page_body[0].get_text().lower())[:1600]

  tags = get_keywords(page_text)
  summary = get_summary(page_text) if len(page_text) > 50 else "No summary available"
  title = url

  if html.title and len(html.title.text.strip()) > 0:
    title = html.title.text

  archived_url = "XXXXXX"

  if archive:
    archived_url = archivenow.push(url, "ia")
    archived_url = archived_url[0]

  if archived_url[0:5] == "https":
    insert_statement = """
      INSERT INTO sites ("title", "url", "summary", "tags", "archive_url")
      VALUES (?, ?, ?, ?, ?)
    """
    # insert into sql database
    with sqlite3.connect("data/sites.db") as conn:
      cursor = conn.cursor()
      cursor.execute(insert_statement, (title, url, summary, ', '.join(tags), archived_url))
      conn.commit()
  else:
    insert_statement = """
      INSERT INTO sites ("title", "url", "summary", "tags")
      VALUES (?, ?, ?, ?)
    """
    # insert into sql database
    with sqlite3.connect("data/sites.db") as conn:
      cursor = conn.cursor()
      cursor.execute(insert_statement, (title, url, summary, ', '.join(tags)))
      conn.commit()

if __name__=="__main__":
  main()