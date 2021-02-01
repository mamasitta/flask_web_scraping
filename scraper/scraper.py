import re
from urllib.request import urlopen



from db import db
from helpers.helpers_scraper import get_links_with_lvl, get_pages_from_links
from models.models import Task, Page


# scraper for scraping data from website
def scraping_data(url, lvl, date):
    # if level of scraping not in post request make it 1
    if lvl is None:
        lvl = 1
    else:
        lvl = lvl
    # get main url for website (for future saving and processing data)
    site_domain = url[8:].split('/')[0]
    clean_url = "https://{}".format(site_domain)
    links = get_links_with_lvl(url, lvl, clean_url)
    # get celery task saved to db to make relationship with pages
    task = Task.query.filter_by(date=date).first()
    # saving all unique pages from user link with level of scraping to db
    for link in links:
        url_link = "{}{}".format(clean_url, link)
        text = get_pages_from_links(url_link)
        page = Page(name=link, text=text, task_id=task)
        task.pages.append(page)
        db.session.add(page)
        db.session.commit()
    return 0


