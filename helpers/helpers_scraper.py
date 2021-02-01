import mechanicalsoup


def check_address(address):
    # processing urls to write in db and future use
    check = [i for i in address.split('#')]
    if len(check) > 1:
        address = check[0]
    else:
        address = address
    if len(address) == 0:
        return None
    if address[len(address) - 1] != '/':
        address = "{}/".format(address)
    if address[0] != '/':
        address = "/{}".format(address)
    return address


# get all links from href in pages with level of scraping
def get_links_with_lvl(url, lvl, clean_url):
    count = lvl
    level = lvl
    links = []
    # if needed just 1 level of scraping
    if level == 1:
        new_link = []
        link = check_address(url[len(clean_url):])
        if link is None:
            link = ''
        new_link.append(link)
        links.append(new_link)
    # if more than 1 level of scraping use count to count levels
    else:
        count -= 1
        while count > 0:
            if len(links) == 0:
                url = url
                new_links = get_links(url, clean_url)
                links.append(new_links)
                count -= 1
            else:
                # for each level new list of links in main list of links
                for link in links[len(links) - 1]:
                    url = '{}{}'.format(clean_url, link)
                    new_links = get_links(url, clean_url)
                    links.append(new_links)
                    count -= 1
    # final list with all unique links
    result = []
    for link in links:
        for i in link:
            if i not in result:
                result.append(i)
    return result


# processing links from pages if they belong to website adding them to list of links
def get_links(url, clean_url):
    # get data from pages with MechanicalSoup
    browser = mechanicalsoup.Browser()
    page = browser.get(url)
    new_links = []
    # search for href in <a> element of HTML
    all_links_from_page = page.soup('a')
    for link in all_links_from_page:
        try:
            address = link['href']
            # checking if href belong to website
            if len(address) > 0 and address[:7] != 'http://' and address[:8] != 'https://' and address[len(address) - 1] != ';':
                # processing url from hrefs
                address = check_address(address)
                if address not in new_links and address is not None:
                    new_links.append(address)
            elif address[:len(clean_url)] == clean_url:
                processed_link = address[len(clean_url):]
                if len(processed_link) > 0:
                    address = check_address(processed_link)
                    if address not in new_links and address is not None:
                        new_links.append(address)
        except KeyError:
            pass
    return new_links


# het data (html, css, js, media) from each link
def get_pages_from_links(url):
    browser = mechanicalsoup.Browser()
    page = browser.get(url)
    text = str(page.soup)
    return text


