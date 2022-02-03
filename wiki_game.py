#Uses python3


import requests
from bs4 import BeautifulSoup
import urllib
import re
import networkx as nx
import matplotlib.pyplot as plt

class My_graph:
    
    COLORS = {
        'start_color' : 'green',
        'end_color' : 'blue',
        'normal_color' : 'red',
        'circle_color' :'yellow',
        'fail_color' : 'black'
    }

    def __init__(self):

        self.color_map = []
        self.circle = False
        self.G = nx.DiGraph()

    def try_insert_first(self, node, color = COLORS['start_color']):

        if self.G.has_node(node):
            return False
        self.G.add_node(node)
        self.add_color(node, color)
        return True

    def insert_node(self, node):

        if node is None:
            return
        if self.G.has_node(node):
            self.circle = True
        else:
            self.G.add_node(node)
            self.add_color(node)

    def insert_edge(self, start_node, end_node):

        self.G.add_edge(start_node, end_node)
        if self._check_circle(start_node, end_node):
            self.change_colors([start_node, end_node], self.COLORS['circle_color'])

    def _check_circle(self, node1, node2):

        if self.G.has_edge(node1, node2) and self.G.has_edge(node2, node1):
            return True
        return False

    def add_color(self, node, color = COLORS['normal_color']):

        self.G.nodes[node]['color'] = color

    def change_color(self, node, color):

        self.G.nodes[node]['color'] = color

    def change_colors(self, nodes : list, color):

        for node in nodes:
            self.G.nodes[node]['color'] = color

    def print_graph(self):
        
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
    g.circle = False
    topic = wiki.get_random_page_href()
    if g.try_insert_first(wiki.parse_wiki_href_to_node(topic)):
        while topic != wiki.END and not g.circle:
    
            current = topic
            topic = wiki.get_next_topic_href(topic)
            current_node = wiki.parse_wiki_href_to_node(current)
            next_node = wiki.parse_wiki_href_to_node(topic)
            g.insert_node(next_node)
            g.insert_edge(current_node, next_node)

            if next_node == None:
                g.change_color(current_node, g.COLORS['fail_color'])
            if topic == wiki.END:
                g.change_color(next_node, g.COLORS['end_color'])

if __name__ == '__main__':

    g = My_graph()
    wiki = Wikipedia
    for i in range(int(input())):
        build_wiki_graph()
        print(f'managed cycle {i}')
    g.print_graph()

    
    

    
        
    






