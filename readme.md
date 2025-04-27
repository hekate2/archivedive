# ArchiveDive
Last Update: April 2nd, 2025\
Contributors: hekate2

![Screenshot of ArchiveDive's search page](img/search-screenshot.png)

## About this tool
ArchiveDive is a search engine which both searches and archives older websites created before 2004.  Try it out at: [ArchiveDive.net](https://ArchiveDive.net);

## Try it out yourself
To run archivedive locally, first clone this repo, then run the front-end and back-end seperately.

The front-end files can be found in the `client` folder.  After navigating to it on the command line, run:
```
npm run dev
```
The back-end files can be found in the `search` folder.  In order to run these you'll first have to install the dependencies in `requirements.txt` with:
```
pip install -r requirements.txt
```
Then, to run the server just run
```
python main.py
```
from the `/search` folder

## Not Included:
To get stuff working you'll have to create a few files:
- `/search/.env` - this'll store your openrouter and google JSON search api keys
- `/search/data/sites.db` - database that will hold your websites.  It should have a `sites` table which can be initialised with this query:

```
CREATE TABLE "sites" (
	"id"	INTEGER NOT NULL,
	"title"	TEXT NOT NULL,
	"url"	TEXT NOT NULL,
	"summary"	TEXT,
	"tags"	NUMERIC NOT NULL,
	"archived_on"	DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	"visits"	INTEGER NOT NULL DEFAULT 0,
	"display_count"	INTEGER NOT NULL DEFAULT 0,
	"archive_url"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
```

## Archiving URLs
To get the thing working, you'll also have to archive some urls.  For this you'll run 3 scripts: `compile.py`, `remove_top_bar.py`*, and `scrape.py`.

### compile.py
This script will compile a list of links that you can then process and add into a database.  The list of links will have minimal
processing, so we'll handle that in subsequent scripts too.

There are three main methods for compiling sites:
1. gifcities API
2. Crawling from a single entry point
3. Google Search API

Here are the pros and cons of each:

**Gifcities API**\
This is in my opinion the best one- basically it runs a search for a query as you would on [gifcities.org](https://gifcities.org/),
and returns all sites with gifs with filenames corresponding to the search query.

Why it's good is:
- Compiles sites that are robust enough that the creator took the time to add gifs (less possibility for 'ghost' sites)
- The only method that is able to archive geocities sites.

Weaknesses are:
- It can only search geocities, which means no angelfire, lycos or tripod websites.

HOW TO RUN IT:

Go into the `compile.py` script and inside of the `main()` function change `search_term` to whatever search term you want.  Then, from the terminal run it with:
```
python compile.py
```
You might have to create `scrapelist.txt` if you don't already have it.

**Crawling from a single entry point**\
While the GifCities API method is the one that's uncommented- this method is commented right below it.  To use it, you'll have to comment out the uncommented code and uncomment everything under:

```
******* THESE ARE METHODS FOR CRAWLING THRU LINKS FROM ONE PAGE ****`
```

Then, you'll have to provide a website to start from (preferrably one with a lot of links!!) in the `entry_point` variable.

The just run:
```
python compile.py
```
And voila!

Why it's good is:
- Can archive a LOT of websites.
- Can archive a large variety of websites
- Doesn't require you to come up with search terms, potentially excluding topics that you don't think about regularly
- Traditional (?)

Why it's bad is:
- Tends to archive a lot of modern websites
- 'Stub' websites that don't link to anything can cause everything to stop.

**Google Search API**\
This method uses the Google JSON Search API- so you'll have to have an account and api key for that.  Once you have the information though, create a `.env` file in the `/server` folder, and do this:

```
GOOGLE_KEY="YOUR_API_KEY"
GOOGLE_SEARCHER_ID="YOUR_ENGINE_ID"
```
Then, uncomment the code below `*** GOOGLE SEARCH API CODE ***` (or whatever I wrote).  Then, when you call `request_urls(query, start)` from your loop in main (TODO: re-add the loop), change `query` to be whatever search query you want.

Why it's good is:
- Gets angelfire and lycos and tripod links- depending on how you configure your search engine in google developer.

Why it's bad is:
- If we're just archiving stuff that's already indexed by google... why not just use google?
- Caps out at 1000 results per day :-/

### remove_top_bar.py
** this method should only be run after compiling internet archive urls.  I mean, it won't screw up your database if you run it each time you make a search anyways, but it's not necessary.

If your results include internet archive urls, please run:
```
python remove_top_bar.py
```
This'll basically remove the default top bar that shows up when using the wayback machine and leads to a more immersive experience.

### scrape.py
This is where the magic happens.  This is the script which will look at each url, check if it's already in your `sites.db` database (which you should probably create if you haven't already)

At this point, you'll also need to create a gpt4 model on OpenRouter and get a key from them, then add it so `search/.env` as so:
```
OPENROUTER_KEY="YOUR_KEY_HERE"
```

Then, basically all you'll need to do is run:
```
python scrape.py
```
And the script will go on and visit each URL in `scrapelist.txt` (one every 10 seconds), parse the webpage content and populate `sites.db` with keywords and a summary of the content.