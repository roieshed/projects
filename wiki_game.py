#Uses python3

from os import stat
import requests
from bs4 import BeautifulSoup
import urllib
import re
import networkx as nx
import matplotlib.pyplot as plt
import time
from neo4j import GraphDatabase
from py2neo import Graph, Node, Relationship


class My_graph:
    
    COLORS = {
        'start_color' : 'green',
        'end_color' : 'blue',
        'normal_color' : 'red',
        'circle_color' :'yellow',
        'fail_color' : 'black'
    }
    PASSWORD = 'Rughtas12!'
    rel_name = 'next'

    def __init__(self):
        self.g= nx.DiGraph()
        self.G = Graph(password = self.PASSWORD)
        
    @staticmethod
    def check_if_node_in_graphDB(graph_DB, node):

        if len(graph_DB.nodes.match(topic = node)):
            return True
        return False

    def insert_node(self, node, first_node = False, website = 'website'):

        if node is None or self.check_if_node_in_graphDB(self.G, node):
            return None
        else:
            if first_node:
                self.G.create(Node(website, 'first_node', topic = node))
            else:
                self.G.create(Node(website, topic = node)) 
            self.g.add_node(node)
            return node

    def insert_edge(self, start_node, end_node):

        first_node = self.G.nodes.match(topic = start_node).first()
        second_node = self.G.nodes.match(topic = end_node).first()
        self.G.create(Relationship(first_node, self.rel_name , second_node))
        self.g.add_edge(start_node, end_node)

    def _check_circle(self, node1, node2):

        pass

    def add_color(self, node, color):
        
        pass

    def change_color(self, node, color):

        node = self.G.nodes.match(topic=node).first()
        node.add_label(color)
        self.G.push(node)

    def change_colors(self, nodes : list, color):

        for node in nodes:
            self.change_color(node, color)

    def update_node(self, node, label):

        node = self.G.nodes.match(topic=node).first()
        node.add_label(label)
        self.G.push(node)

    def update_nodes(self, nodes, label):
        
        for node in nodes:
            self.update_node(node, label)

    def print_graph(self):

        "printing graph"
        for cycle in nx.simple_cycles(self.g):
            self.update_nodes(cycle, 'cycle')

    

    

        

class Wikipedia:
    
    RANDOM_PAGE = "https://en.wikipedia.org/wiki/Special:Random"
    RANDOM_PAGE_TOPIC = ('link', {'rel' : 'canonical'})
    MAIN_BODY_XPATH = ('div', {'id' : 'mw-content-text'})
    TEMPLATE = 'https://en.wikipedia.org'
    END = '/wiki/Truth'
   
    

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
        print(url)
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
                g.update_node(current_node, 'fail')
            else: 
                g.insert_edge(current_node, next_node)

            if next_topic == wiki.END:
                g.update_node(next_node, 'end')

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

    
#TODO  -> 1) ADDED TO DB - still need to find cycles in DB -> currently saving a NX graph locally
#         2) add asyncIO to function, while waiting for the request start a new random
#         3) make docker image
#         4) run multiple containers togethor


    
## make it async
## with DB
## with docker
## with workerim


    






