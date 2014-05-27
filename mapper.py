import requests
import lxml.html

def link_grab(url,base_url):
    """Returns all complete links on the page.  
    Aka all those links who include the base url in the link."""
    base = ""
    if "//" in base_url:
        base = base_url.split("//")[1]
    if "/" in base:
        base = base.split("/")[0]
        
    r = requests.get(url)
    obj = lxml.html.fromstring(r.text)
    links_obj = obj.xpath("//a")

    links = []
    incomplete_links = [] # use this if you want
    for link in links_obj:
        tmp = [elem for elem in link.values() if base in elem]
        if tmp != []:
            elem = tmp.pop()
            if elem.startswith("/"):
                incomplete_links.append(elem)
                continue
            links.append(elem)
    return links

def map_website(base_url,depth):
    link_list = []
    return map_website(base_url,base_url,depth,link_list)

def map_website(url,base_url,depth,link_list):
    if depth <= 0:
        return link_list
    links_on_page = link_grab(url,base_url)
    tmp = []
    for link in links_on_page:
        if not link in link_list:
            link_list.append(link)
            tmp = map_website(link,base_url,depth-1,link_list)
            for elem in tmp:
                if not elem in link_list:
                    link_list.append(elem)
    return link_list
    

print map_website("https://www.google.com",2)
