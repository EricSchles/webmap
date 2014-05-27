import requests
import lxml.html

def link_grab(url,base_url):
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
    basis = link_grab(base_url,base_url)
    link_list = []
    count = 0
    while count < depth:
        #print link_grab(base_url) #check to ensure things still work    
        for links in basis:
            tmp = link_grab(links,base_url)
            for link in tmp:
                if link in link_list:
                    continue
                link_list.append(link)
        count += 1
    return link_list
