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

load_dotenv()

def main():
  try:
    no_summary_sites = get_no_summary_sites()

    for url in no_summary_sites:
      # TODO: start spinner
      with yaspin(Spinners.earth, text=f"Summarizing: {url}") as spinner:
        try:
          summarize(url)
          spinner.ok("✅ ")
        except Exception as e:
          spinner.fail("❌ ")
          print(e)
  except Exception as e:
    print(e)
    print("blah something went wrong and no sites could be scraped.")

def get_no_summary_sites():
  """
  Returns a list of sites that are in the db but might not have been archived
  """
  conn = sqlite3.connect("data/sites.db")
  cursor = conn.cursor()

  query = """
  SELECT DISTINCT url
  FROM sites
  WHERE summary IS NULL
  """
  cursor.execute(query)

  res = [val[0] for val in cursor.fetchall()]
  conn.close()

  return res

def process_raw_text(text):
  """
  Removes extra empty lines from the page text
  """
  mod_text = '\n'.join([line for line in text.splitlines() if line.strip()])

  return mod_text

def get_summary(text):
  """
  Writes a little summary about the website
  """
  try:
    response = requests.post(
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

    if "error" in res:
      raise Exception(res["error"]["message"])

    return res["choices"][0]["message"]["content"]
  except Exception as e:
    print(f"\n{e}")
    print("\nCouldn't generate summary :-/")
    return None

def summarize(url):
  """
  Generate a summary and update the database
  """
  data = requests.get(url)
  data.raise_for_status()

  html = BeautifulSoup(data.text, 'html.parser')

  page_body = html.select("body")

  if not page_body:
    # Skip processing this site
    raise Exception(f"No <body> found for URL: {url}")

  page_text = process_raw_text(page_body[0].get_text().lower())
  summary = get_summary(page_text) if len(page_text) > 100 else "No summary available"

  update_statement = """
    UPDATE sites
    SET summary = ?
    WHERE url = ?
  """
  # insert into sql database
  with sqlite3.connect("data/sites.db") as conn:
    cursor = conn.cursor()
    cursor.execute(update_statement, (summary, url))
    conn.commit()

if __name__=="__main__":
  main()