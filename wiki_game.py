#Uses python3

import requests
from bs4 import BeautifulSoup
import urllib
import re
from igraph import * 

class Wikipidea:

    g = Graph(directed=True)
    template = 'https://en.wikipedia.org/wiki/'
    
    def __init__(self):
        pass

    @classmethod
    def _generate_random_wiki_page(cls) -> str:
    
        random_page = requests.get("https://en.wikipedia.org/wiki/Special:Random")
        soup = BeautifulSoup(random_page.content, "html.parser")
        url = soup.find(class_="firstHeading").text
        cls.g.add_vertex(url)
        return  urllib.parse.quote(url)

    @classmethod
    def _reach_philosophy(cls):

        def _check_vertex(vertex):
                try:
                    x = cls.g.vs.find(vertex).index
                except:
                    x = -1
                return True if x > 0 else False
            

        def find_first_link(url): # returns the text of the first link

            
            def _get_paranthesis(text):
            
                # check if the link is in between "()", if there are no "()" -> has to be valid
                query = re.search('\(.*?\)', text, flags = re.DOTALL)
                if query is None:
                    return float('inf'), 0
                return query.start(0), query.end(0)

            def _validate_link(link,  paragraph, range_start, range_end): 

                # all relevent links in wikipedia have a title attr
                # if link dosent have title or title has been seen -> invalid link
                if (not link.has_attr('title')) or bool(re.search('/wiki/Wikipedia:', link['href'])):
                    return False

                escaped_text = re.escape(link.text)
                if escaped_text in seen_links:

                    text_indexes = re.finditer(escaped_text,paragraph.text)
                    for index, match in enumerate(text_indexes):
                        if index == seen_links[escaped_text]:
                            link_start = match.start(0)
                    seen_links[escaped_text] += 1

                else:
                    
                    text_indexes = re.search(escaped_text, paragraph.text)
                    link_start = text_indexes.start(0)
                    seen_links[escaped_text] = 1

                return  not (range_start < link_start < range_end)
    
            def _get_html_content(url):
                
                url  = cls.template + url 
                try:
                    r = requests.get(url)
                except:
                    return -1
                return BeautifulSoup(r.content, 'html.parser')

            html_content = _get_html_content(url)
            if html_content == -1:
                return -1 
            main_body = html_content.find('div', {'id' : 'mw-content-text'})
            if main_body is None:
                return -1
            
            # iterates through all links in all paragraphs and returns the first link that is by the rules
            for paragraph in main_body.find_all('p'):
                seen_links = {} ## keeps track if ive seen links
                open_paranthesis, close_paranthesis = _get_paranthesis(paragraph.text)
                for link_number, link in enumerate(paragraph.find_all(href=True)):
                    ## change it so i can get the index during the findall
                    if _validate_link(link, paragraph, open_paranthesis, close_paranthesis):
                        return link['href'][6:]
            
            # reached a page with no links
            print('failed')
            return -1
            
        current_page = cls._generate_random_wiki_page()

        while current_page != 'Philosophy':  
            
            next_page = find_first_link(current_page) #function returns -1 if there are no links
            if next_page == -1:
                break
            
            next_vertex, current_vertex = urllib.parse.unquote(next_page), urllib.parse.unquote(current_page)
            if _check_vertex(next_vertex):
                cls.g.add_edge(current_vertex, next_vertex)
                break
            
            cls.g.add_vertex(next_vertex)
            cls.g.add_edge(current_vertex, next_vertex)
            current_page = next_page 
        

    @classmethod
    def print_philosophy_graph(cls):
        
        cls.g.vs["label"] = cls.g.vs['name']
        color = {"Philosophy" : "blue"}
        cls.g.vs['color'] = [color.get(name, 'red') for name in cls.g.vs['name']]
        plot(cls.g, vertex_color = cls.g.vs['color'], bbox = (1200,800))


if __name__ == '__main__':

    wiki = Wikipidea()
    for i in range(int(input())):
        Wikipidea._reach_philosophy()
        print(f"managed cycle {i}")

    Wikipidea.print_philosophy_graph()
    

    
    

    
        
    
