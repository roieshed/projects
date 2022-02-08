#Uses python3


from tracemalloc import start
import requests
from bs4 import BeautifulSoup
import urllib
import re
import networkx as nx
import matplotlib.pyplot as plt
import time

class My_graph:
    
    COLORS = {
        'start_color' : 'green',
        'end_color' : 'blue',
        'normal_color' : 'red',
        'circle_color' :'yellow',
        'fail_color' : 'black'
    }

    def __init__(self):

        self.color_map = []#TODO
        self.G = nx.DiGraph()

    def insert_node(self, node, first_node = False, color = COLORS['normal_color']):

        if node is None or self.G.has_node(node):
            return None
        else:
            if first_node:
                color = self.COLORS['start_color']
            self.G.add_node(node)
            self.add_color(node, color)
            return node

    def insert_edge(self, start_node, end_node):

        self.G.add_edge(start_node, end_node)

    def _check_circle(self, node1, node2):

        if self.G.has_edge(node1, node2) and self.G.has_edge(node2, node1):
            return True
        return False

    def add_color(self, node, color):
        
        self.G.nodes[node]['color'] = color

    def change_color(self, node, color):

        self.G.nodes[node]['color'] = color

    def change_colors(self, nodes : list, color):

        for node in nodes:
            self.change_color(node, color)

    def print_graph(self):
        
        for cycle in nx.simple_cycles(self.G):
            for node in cycle:
                self.G.nodes[node]['color'] = self.COLORS['circle_color']
        colors_map = [self.G.nodes[x].get('color', 'red') for x in self.G.nodes]
        nx.draw(self.G ,node_color = colors_map , with_labels=True)
        plt.show()
    

    

        

class Wikipedia:
    
    RANDOM_PAGE = "https://en.wikipedia.org/wiki/Special:Random"
    RANDOM_PAGE_TOPIC = ('link', {'rel' : 'canonical'})
    MAIN_BODY_XPATH = ('div', {'id' : 'mw-content-text'})
    TEMPLATE = 'https://en.wikipedia.org'
    END = '/wiki/Philosophy'
   
    

    def __init__(self):
        pass
    
    @classmethod
    def parse_main_body(cls, bs4_content):

        return bs4_content.find(*cls.MAIN_BODY_XPATH)
    
    @staticmethod
    def validate_paragraph(paragraph):

        if paragraph.find_parent('table'):
            return False
        else:
            return True

    @classmethod
    def get_next_topic_href(cls, topic):

        content = cls.parse_url_to_bs4(f'{cls.TEMPLATE}{topic}')
        main_body = cls.parse_main_body(content)
        for paragraph in cls.find_all_paragraphs(main_body):
                if cls.validate_paragraph(paragraph):
                    for link in cls.find_all_links(paragraph):
                        if cls.validate_link(link):
                            return link['href']
        
        return None

    @classmethod
    def get_random_page_href(cls):

        soup = cls.parse_url_to_bs4(cls.RANDOM_PAGE)
        topic = soup.find(*cls.RANDOM_PAGE_TOPIC)['href']
        return topic.split(cls.TEMPLATE)[-1]

    @staticmethod
    def parse_url_to_bs4(url):

        try:
            r = requests.get(url)   
        except:
            raise "failed to get url"
        return BeautifulSoup(r.content, 'html.parser')
    
    @staticmethod
    def validate_link(link):

        edge_cases = ['/wiki/Geographic_coordinate_system']
        parantheis = []
        for sibling in link.previous_siblings:
            parantheis += re.findall('[\(\)]', sibling.text)
        
        valid = len(parantheis) % 2 == 0 and not bool(re.match('.*?:.*?', link['href'])) and link['href'] not in edge_cases
        return valid

    @staticmethod
    def find_all_paragraphs(bs4_content):

        paragraphs = bs4_content.find_all('p')
        return paragraphs

    @staticmethod
    def find_all_links(paragraph):

        links = paragraph.find_all('a', href=lambda x: x is not None and x.startswith("/wiki/")) 
        return links

    @staticmethod
    def parse_wiki_href_to_node(wiki_href):

        if wiki_href is None:
            return wiki_href
        return wiki_href.split('/')[-1]

def build_wiki_graph():
    ## this function feels very disorginized to me, how would you reccomend to do it?
    topic_in_db = False
    next_topic = wiki.get_random_page_href()
    if g.insert_node(wiki.parse_wiki_href_to_node(next_topic), first_node=True):
        while next_topic != wiki.END and not topic_in_db:
    
            current_topic = next_topic
            next_topic = wiki.get_next_topic_href(next_topic)
            current_node = wiki.parse_wiki_href_to_node(current_topic)
            next_node = wiki.parse_wiki_href_to_node(next_topic)
            if not g.insert_node(next_node):
                topic_in_db = True

            if next_node == None:
                g.change_color(current_node, g.COLORS['fail_color'])
            else: 
                g.insert_edge(current_node, next_node)

            if next_topic == wiki.END:
                g.change_color(next_node, g.COLORS['end_color'])

if __name__ == '__main__':

    start_time = time.time()
    g = My_graph()
    wiki = Wikipedia
    for i in range(int(input("how many times?"))):
        cycle_start_time = time.time()
        build_wiki_graph()
        cycle_end_time = time.time()
        print(f'managed cycle {i} in {cycle_end_time - cycle_start_time} seconds')

    g.print_graph()
    end_time = time.time()
    print(f"it took {end_time - start_time} seconds for everything")

    
#TODO  -> 1) find a graph DB and add to there - NEO4J
#         2) add asyncIO to function, while waiting for the request start a new random
#         3) make docker image
#         4) run multiple containers togethor


    
## make it async
## with DB
## with docker
## with workerim


    






