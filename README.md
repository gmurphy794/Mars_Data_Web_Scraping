# Mars Data Web Scraping Script


This repository contains a Python webscraping script [scrape_mars.py], used to scrape data from twitter, nasa, astrogeology.usgs.gov, and space_facts.com, store that data in a dictionary to be later put in a mondgoDB database. 

The repository also contians a Python script [app.py] used to create a local Flask server to render the HTML file with the scraped data, run scrape_mars.py, and store and pull the scraped data into the database.

Libraries Used:
- Pandas
- BeautifulSoup
- Requests
- Splinter
- PyMongo
- Flask



