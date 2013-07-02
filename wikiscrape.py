from lxml.html import parse
import networkx as nx
import matplotlib.pyplot as plt 
import sys, traceback
import logging
import signal
from optparse import make_option, OptionParser

sig_received = False

FORMAT = '%(asctime)s %(levelname)-8s %(message)s'

MAX_RETRY = 3
SOVEREIGN_STATES = 'http://en.wikipedia.org/wiki/List_of_sovereign_states'

class SovereignStates():
    def __init__(self, max=sys.maxint, layout=1):
        self.max = max
        self.layout = layout
        self.states = {}
        self.graph = nx.DiGraph()

        #setup logging and signal handling
        self.log = logging.getLogger('SovereignStates')
        self.log.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setFormatter(logging.Formatter(FORMAT))
        ch.setLevel(logging.DEBUG)
        self.log.addHandler(ch)
        
        def signal_handler(signum, frame):
            global sig_received
            if signum == signal.SIGINT or signum == signal.SIGTERM or signum == signal.SIGHUP:
                sig_received = True
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        signal.signal(signal.SIGHUP, signal_handler)
    
    #main flow
    def run(self):
        self.get_states()
        self.build_graph()
        self.draw_graph()

    #helper function, handles making url requests with retries
    def make_request(self, url, retry=MAX_RETRY):
        attempts = 0
        doc = None
        global sig_received
        
        while True:
            if sig_received:
                self.log.info('signal received')
                sys.exit(0)
            
            try:
                doc = parse(url).getroot()
                break
            except:
                self.log.debug('request failed')
                attempts = attempts + 1
                if attempts > retry:
                    break
                self.log.debug('retrying request')
        return doc

    #traverses the page to get the list of states and their urls
    def get_states(self):
        doc = self.make_request(SOVEREIGN_STATES)
        if doc is None:
            self.log.error('unable to request list of sovereign states')
            sys.exit(1)
                      
        doc.make_links_absolute()
        flags = doc.find_class('flagicon')
        
        for flag in flags:
            #exclude territories
            parent = flag.getparent()
            if parent.tag != 'b':
                continue

            #grab the country title and url
            a = parent.cssselect('a')[0]
            title = a.get('title')
            url = a.get('href')
            self.states[url] = title

            if len(self.states) >= self.max:
                break

    #find connections between sovereign states
    def build_graph(self):
        urls = self.states.keys()
        for url,title in self.states.items():
            doc = self.make_request(url)
            if doc is None:
                self.log.error('unable to request %s' % title)
                continue
            doc.make_links_absolute()

            #check every url on the page to see if its in our list of states' urls
            self.graph.add_node(title)
            for link in doc.cssselect('a'):
                if link.get('href') in urls:
                    self.graph.add_edge(title, self.states[link.get('href')])

    #draw the graph with different possible layouts
    def draw_graph(self):
        if self.layout == 1:
            pos=nx.spring_layout(self.graph,iterations=10)
        elif self.layout == 2:
            pos=nx.circular_layout(self.graph)
        elif self.layout == 3:
            pos=nx.random_layout(self.graph)
        else:
            pos=nx.spectral_layout(self.graph)

        nx.draw(self.graph,pos,node_size=0,alpha=0.4,edge_color='r',font_size=16)
        plt.show()

if __name__ == '__main__':
    option_list = [
                   make_option('-m', '--max', dest='max', default=sys.maxint, type='int',
                               help='max number of sovereign state nodes'),
                   make_option('-l', '--layout', dest='layout', default=1, type='int',
                               help='different drawing technique [1-4]'),                   
                   ]
    parser = OptionParser(option_list=option_list)
    (options, args) = parser.parse_args()
    
    assert options.max > 0, 'Max nodes must be a positive integer'
    assert len(args) == 0, 'No input arguments, only options'
    
    states = SovereignStates(*args, **options.__dict__)
    try:
        states.run()
    except:
        traceback.print_exc()
