PROGRAMMING ASSIGNMENT
----------------------

The goals are: 

1) Make sure you are a confident programmer who can deal efficiently with ordinary programming tasks
2) See how you organize and structure your code. 

You may use any language or libraries that you want, but you must provide clear instructions on how to get the program running on our machines. Our computers are macs, but you shouldn't assume anything else about them.  You may provide additional libraries along with your code. It should take less than an hour to run your program. 


Wikipedia Scraping:

We want to know about how countries relate to each other. 

At the link below you'll find a list of countries. 
http://en.wikipedia.org/wiki/List_of_sovereign_states

We want you to build us a graph showing which countries are connected to each other. You'll need to scrape through each of the pages on the list of countries looking for links to other countries on that list. 

For example: 
Thhe India page (http://en.wikipedia.org/wiki/India) links to the Burma page (http://en.wikipedia.org/wiki/Burma), Bangledesh page (http://en.wikipedia.org/wiki/Bangladesh), as well as many others. 

Once you have that information in a graph structure, we want you to generate a visualization of the graph. It doesn't need to be pretty, but it should be clear and distinguish between 1 way and two way connections.  



SOLUTION
--------

INSTALLATION
------------

sudo port install python26
cd
wget --no-check-certificate https://raw.github.com/pypa/virtualenv/master/virtualenv.py
python virtualenv.py --distribute rhone
source ~/rhone/bin/activate

~/rhone/bin/pip install lxml
~/rhone/bin/pip install networkx
~/rhone/bin/pip install numpy
~/rhone/bin/pip install matplotlib
~/rhone/bin/pip install python-dateutil==1.5

echo "backend: MacOSX" > ~/.matplotlib/matplotlibrc


USAGE
-----

python wikiscrape.py -m 25 -l 1

-m .. max number of sovereign states to traverse (optional)
-l .. a layout pattern for the nodes, valid values are 1, 2, 3 or 4 (optional)


SCRATCH NOTES (IGNORE)
----------------------

sudo easy_install pip
pip install virtualenv
virtualenv rhone
sudo port install py26-matplotlib +cairo+gtk2

