import re
from urllib.request import urlopen

import mechanicalsoup as mechanicalsoup

from db import db
from helpers.helpers_scraper import get_links_with_lvl, get_pages_from_links
from models.models import Task, Page


def scraping_data(url, lvl):
    if lvl is None:
        lvl = 1
    else:
        lvl = lvl
    site_domain = url[8:].split('/')[0]
    clean_url = "https://{}".format(site_domain)
    links = get_links_with_lvl(url, lvl, clean_url)
    task = Task(link=url)
    for link in links:
        url_link = "{}{}".format(clean_url, links[0])
        text = get_pages_from_links(url_link)
        page = Page(name=link, text=text, task_id=task)
        task.pages.append(page)
        db.session.add(page)
    db.session.add(task)
    db.session.commit()
    return 0
    # for link in links:





#
# scraping_data('https://planeks.net/', 3)
