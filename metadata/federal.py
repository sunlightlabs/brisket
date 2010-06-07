#!/usr/bin/python

from BeautifulSoup import BeautifulSoup
import urllib2

'''
Pulls in metadata for federal senators and representatives. 
'''

# former reps:
# http://en.wikipedia.org/wiki/List_of_former_members_of_the_United_States_House_of_Representatives

# former senators:
# http://en.wikipedia.org/wiki/List_of_former_United_States_senators


def build_soup(url):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'SunlightLabs-Brisket/1.0')]
    fp = opener.open(url)
    page = fp.read()
    soup = BeautifulSoup(page)
    return soup

def get_current():
    reps = get_reps()
    senators = get_senators()

def get_current_senators():
    current_senators_url = "http://en.wikipedia.org/w/index.php?title=List_of_current_United_States_Senators&printable=yes"
    soup = build_soup(current_senators_url)
    members_heading = soup.find(attrs={'id':'Members'})
    tbl = members_heading.parent.findNext('table').findNext('table')
    # get the content rows from the table (not first or last)
    rows = tbl.findAll('tr')[1:-1]
    links = {}
    for row in rows:
        a = row.findAll('td')[3].find('a')
        link = a.get('href')
        name = a.text
        links[name] = link
    return links

def get_current_reps():
    ''' get links to the wikipedia pages of the current list of
    federal politicians as maintained by wikipedia. '''
    # use the pretty-print wikipedia url format
    current_reps_url = "http://en.wikipedia.org/w/index.php?title=List_of_current_members_of_the_United_States_House_of_Representatives_by_seniority&printable=yes"
    soup = build_soup(current_reps_url)
    # extract the rows and leave off the header row, which we're not
    # interested in.
    rows = soup.find('table').findAll('tr')[1:]
    links = {}
    for row in rows:
        a = row.find('a')
        if a:
            name = a.text
            link = a.get('href')            
            links[name] = link
    return links


def get_bio():
    pass

def 

def get_bioguide():
    # get the bioguide id of the politician
    pass


if __name__ == '__main__':
    
