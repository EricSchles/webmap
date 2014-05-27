import requests
import lxml.html
import time
"""
Functions for the user:

map_images(base_url,depth): Gets the links for all the images on a given set of web pages

pdf_grab(url,depth): Gets the links for all the pdfs on a given set of web pages

map_links(base_url,depth): Gets all the links for all the pages of a given website, upto a certain depth.

Recommended depth: 3 - 6 (otherwise request may time out)
"""

def link_grab(url,base_url):
    """Returns all links on the page.  
    Aka all those links who include the base url in the link."""
        
    r = requests.get(url)
    obj = lxml.html.fromstring(r.text)
    links_obj = obj.xpath("//a")

    links = []
    incomplete_links = [] 

    for link in links_obj:
        fully_qualified = [elem for elem in link.values() if elem.startswith(base_url)] #fully qualified link as in https://www.google.com/services/
        partial_links = [elem for elem in link.values()] # not fully qualified as in /int1/en/policies/

        for ind,item in enumerate(partial_links):
            if item in fully_qualified:
                partial_links.pop(ind)

        if fully_qualified != []:
            elem = fully_qualified.pop()
            links.append(elem)
        if partial_links != []:
            elem = partial_links.pop()
            if "/" in elem:
                incomplete_links.append(elem)
    
    for link in incomplete_links:
        if link.startswith("http"):
            links.append(link)
            continue
        if base_url.endswith("/"):
            if link.startswith("/"):
                link = link.lstrip("/")
                link = base_url + link
        else:
            link = base_url + link
        links.append(link)
    return links

def map_links(base_url,depth):
    link_list = []
    return mapper(base_url,base_url,depth,link_list)

def mapper(url,base_url,depth,link_list):
    """Grabs all the links on a given set of pages, does this recursively."""
    if depth <= 0:
        return link_list
    links_on_page = link_grab(url,base_url)
    tmp = []
    for link in links_on_page:
        if not link in link_list:
            link_list.append(link)
            tmp = mapper(link,base_url,depth-1,link_list)
            for elem in tmp:
                if not elem in link_list:
                    link_list.append(elem)
    return link_list
    
def pdf_grab(url,depth):
    """Grabs all the pdfs on a given set of pages."""
    links = map_website(url,depth)
    pdfs = []
    for link in links:
        if ".pdf" in link:
            pdfs.append(link)
    return pdfs

def image_grab(url,base_url):
    """Returns all images on the page."""        
    time.sleep(2)
    r = requests.get(url)
    obj = lxml.html.fromstring(r.text)
    img_obj = obj.xpath("//img")

    images = []
    for link in img_obj:
         img_link = [elem for elem in link.values()] 
         if img_link != []:
             for elem in img_link:
                 if img_check(elem):
                     if base_url.endswith("/"):
                         if elem.startswith("/"):
                             elem = elem.lstrip("/")
                             elem = base_url + elem
                     else:
                         elem = base_url + elem
                     images.append(elem)
    return images

def img_check(img_url):
    """Checks to see if a given link has a img extension.  Specifically checks for png, jpg, and gif image types."""
    if img_url.endswith(".gif") or img_url.endswith(".jpg") or img_url.endswith(".png"):
        return True
    return False


def map_images(base_url,depth):
    """Grabs all urls of images on a given website, use depth to determine how much of the website should be visited"""
    
    links = map_links(base_url,depth)

    img_links = []
    for link in links:
        for img in image_grab(link,base_url):
            img_links.append(img)

    return img_links

