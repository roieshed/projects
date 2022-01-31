#Uses python3

from ast import Sub
from http.client import FAILED_DEPENDENCY
import requests
from bs4 import BeautifulSoup
import urllib
import re




def find_path_to_philosphy(): 

    def find_first_link(wiki_page): # returns the text of the first link

        def _get_paranthesis(text):
            
            # check if the link is in between "()", if there are no "()" -> has to be valid
            query = re.search('\(.*?\)', text, flags = re.DOTALL)
            if query is None:
                return float('inf'), 0
            return query.start(0), query.end(0)

        # makes sure the link isnt in paranthesis ## still need to fix
        def _validate_link(link, paragraph, range_start, range_end): 

            # all relevent links in wikipedia have a title attr
            # if link dosent have title or title has been seen -> invalid link
            if (not link.has_attr('title')) or link['href'] in visited or bool(re.search('/wiki/Wikipedia:', link['href'])):
                return False

            ## need to see about bugs if same word is twice 

            link_indexs = re.search(re.escape(link.text), paragraph.text)
            link_start = link_indexs.start(0)
            return  not (range_start < link_start < range_end)

        # takes a url and returns html script ## need to add error handling
        def _get_html_content(url):
            try:
                r = requests.get(url)
            except:
                return -1
            return BeautifulSoup(r.content, 'html.parser')

        # finds the main text of the wiki page
        html_content = _get_html_content(wiki_page)
        if html_content == -1:
            return -1 
        main_body = html_content.find('div', {'id' : 'mw-content-text'})
        if main_body is None:
            return -1
        
        # iterates through all links in all paragraphs and returns the first link that is by the rules
        for paragraph in main_body.find_all('p'):

            open_paranthesis, close_paranthesis = _get_paranthesis(paragraph.text)
            for link in paragraph.find_all(href=True):
                if _validate_link(link, paragraph, open_paranthesis, close_paranthesis):
                    visited.add(link['href'])
                    return link['href']
        
        # reached a page with no links
        print('failed')
        return -1

       # returns a random wiki page
    def get_random_wiki_page_title():

        url = requests.get("https://en.wikipedia.org/wiki/Special:Random")
        # url = requests.get('https://en.wikipedia.org/wiki/Administrative_division')
        soup = BeautifulSoup(url.content, "html.parser")
        title = soup.find(class_="firstHeading").text
        return title

    template = 'https://en.wikipedia.org'
    title = get_random_wiki_page_title()
    visited = {title}
    current_page = template + '/wiki/' + urllib.parse.quote(title)

    while current_page != 'https://en.wikipedia.org/wiki/Philosophy':  

        next_page = find_first_link(current_page) #function returns -1 if there are no links
        if next_page == -1:
            break
        current_page = template + next_page #update current_page to a correct url

    if current_page == 'https://en.wikipedia.org/wiki/Philosophy':
        global SUCCES
        SUCCES.append(len(visited))
    else:
        global FAILED_COUNT
        FAILED_COUNT += 1 

if __name__ == '__main__':

    n = input()
    
    
    FAILED_COUNT = 0 
    SUCCES = []
    
    for i in range(int(n)):
        find_path_to_philosphy()
        print(f"finished cycle {i}")
        print(SUCCES)
    average = sum(num for num in SUCCES) / len(SUCCES)
    print(f"managed to reach philosophy {len(SUCCES)} out of {n} times")
    print(f"took an average of {average} steps")

    

    
        
    
        

    # for now just printing how many steps it took
    


## global vars in capslock 

## add a function where i can call it 
## class where each page is node