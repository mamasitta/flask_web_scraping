import mechanicalsoup


def check_address(address):
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


def get_links_with_lvl(url, lvl, clean_url):
    lvl = lvl -1
    links = []
    while lvl > 0:
        if len(links) == 0:
            url = url
            new_links = get_links(url, clean_url)
            links.append(new_links)
            lvl -= 1
        else:
            for link in links[len(links) - 1]:
                url = '{}{}'.format(clean_url, link)
                new_links = get_links(url, clean_url)
                links.append(new_links)
                lvl -= 1
    result = []
    for link in links:
        for i in link:
            if i not in result:
                result.append(i)
    return result



def get_links(url, clean_url):
    browser = mechanicalsoup.Browser()
    page = browser.get(url)
    new_links = []
    all_links_from_page = page.soup('a')
    for link in all_links_from_page:
        try:
            address = link['href']
            if len(address) > 0 and address[:7] != 'http://' and address[:8] != 'https://' and address[len(address) - 1] != ';':
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
    print(len(new_links))
    return new_links


# def get_page_data(url):



# def scraping_in_lvl(clean_url, lvl, links):
#     lvl = lvl
#     links = links
#     print(len(links))
#     links_for_lvl = [links]
#     while lvl != 0:
#         new_links = []
#         for link in links_for_lvl[len(links_for_lvl) - 1]:
#             browser = mechanicalsoup.Browser()
#             url = "{}{}".format(clean_url, link)
#             page = browser.get(url)
#             all_links = page.soup.select('a')
#             for link in all_links:
#                 try:
#                     address = link['href']
#                     if len(address) > 0 and address[0] == '/':
#                         address = check_address(address)
#                         if address not in new_links and address not in links:
#                             new_links.append(address)
#                             links.append(address)
#                     elif address[:len(clean_url)] == clean_url:
#                         processed_link = address[len(clean_url):]
#                         if len(processed_link) > 0:
#                             address = check_address(processed_link)
#                             if address not in links and address not in new_links:
#                                 new_links.append(address)
#                                 links.append(address)
#                 except KeyError:
#                     pass
#         print(new_links)
#         print(lvl)
#         links_for_lvl.append(new_links)
#         lvl -= 1
#     print(len(links))
#     return links
