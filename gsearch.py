#!/usr/bin/python  
#-*- coding: utf-8 -*-
#
# Create by Meibenjin. 
#
# Last updated: 2013-04-02
#
# google search results crawler 

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import urllib2, socket, time
import gzip, StringIO
import re, random, types

from bs4 import BeautifulSoup 

base_url = 'https://www.google.com.hk/'
results_per_page = 10

user_agents = list()

# results from the search engine
# basically include url, title,content
class SearchResult:
    def __init__(self):
        self.url= '' 
        self.title = '' 
        self.content = '' 

    def getURL(self):
        return self.url

    def setURL(self, url):
        self.url = url 

    def getTitle(self):
        return self.title

    def setTitle(self, title):
        self.title = title

    def getContent(self):
        return self.content

    def setContent(self, content):
        self.content = content

    def printIt(self, prefix = ''):
        print 'url\t->', self.url
        print 'title\t->', self.title
        print 'content\t->', self.content
        print 

    def writeFile(self, filename):
        file = open(filename, 'a')
        try:
            file.write('url:' + self.url+ '\n')
            file.write('title:' + self.title + '\n')
            file.write('content:' + self.content + '\n\n')

        except IOError, e:
            print 'file error:', e
        finally:
            file.close()


class GoogleAPI:
    def __init__(self):
        timeout = 40
        socket.setdefaulttimeout(timeout)

    def randomSleep(self):
        sleeptime =  random.randint(60, 120)
        time.sleep(sleeptime)

    #extract the domain of a url
    def extractDomain(self, url):
        domain = ''
        pattern = re.compile(r'http[s]?://([^/]+)/', re.U | re.M)
        url_match = pattern.search(url)
        if(url_match and url_match.lastindex > 0):
            domain = url_match.group(1)

        return domain

    #extract a url from a link
    def extractUrl(self, href):
        url = ''
        pattern = re.compile(r'(http[s]?://[^&]+)&', re.U | re.M)
        url_match = pattern.search(href)
        if(url_match and url_match.lastindex > 0):
            url = url_match.group(1)

        return url 

    # extract serach results list from downloaded html file
    def extractSearchResults(self, html):
        results = list()
        soup = BeautifulSoup(html, 'html.parser')
        div = soup.find('div', id  = 'search')
        if (type(div) != types.NoneType):
            lis = div.findAll('li', {'class': 'g'})
            if(len(lis) > 0):
                for li in lis:
                    result = SearchResult()
                    h3 = li.find('h3', {'class': 'r'})
                    if(type(h3) == types.NoneType):
                        continue

                    # extract domain and title from h3 object
                    link = h3.find('a')
                    if (type(link) == types.NoneType):
                        continue

                    url = link['href']
                    url = self.extractUrl(url)
                    if(cmp(url, '') == 0):
                        continue
                    title = link.renderContents()
                    result.setURL(url)
                    result.setTitle(title)

                    span = li.find('span', {'class': 'st'})
                    if (type(span) != types.NoneType):
                        content = span.renderContents()
                        result.setContent(content)
                    results.append(result)
        return results

    # search web
    # @param query -> query key words 
    # @param lang -> language of search results  
    # @param num -> number of search results to return 
    def search(self, query, lang='en', num=results_per_page):
        search_results = list()
        query = urllib2.quote(query)
        if(num % results_per_page == 0):
            pages = num / results_per_page
        else:
            pages = num / results_per_page + 1

        for p in range(0, pages):
            start = p * results_per_page 
            url = '%s/search?hl=%s&num=%d&start=%s&q=%s' % (base_url, lang, results_per_page, start, query)
            retry = 3
            while(retry > 0):
                try:
                    request = urllib2.Request(url)
                    length = len(user_agents)
                    index = random.randint(0, length-1)
                    user_agent = user_agents[index] 
                    request.add_header('User-agent', user_agent)
                    request.add_header('connection','keep-alive')
                    request.add_header('Accept-Encoding', 'gzip')
                    request.add_header('referer', base_url)
                    response = urllib2.urlopen(request)
                    html = response.read() 
                    if(response.headers.get('content-encoding', None) == 'gzip'):
                        html = gzip.GzipFile(fileobj=StringIO.StringIO(html)).read()

                    results = self.extractSearchResults(html)
                    search_results.extend(results)
                    break;
                except urllib2.URLError,e:
                    print 'url error:', e
                    self.randomSleep()
                    retry = retry - 1
                    continue
                
                except Exception, e:
                    print 'error:', e
                    retry = retry - 1
                    self.randomSleep()
                    continue
        return search_results 

def load_user_agent():
    fp = open('./user_agents', 'r')

    line  = fp.readline().strip('\n')
    while(line):
        user_agents.append(line)
        line = fp.readline().strip('\n')
    fp.close()

def crawler():
    # Load use agent string from file
    load_user_agent()

    # Create a GoogleAPI instance
    api = GoogleAPI()

    # set expect search results to be crawled
    expect_num = 10
    # if no parameters, read query keywords from file
    if(len(sys.argv) < 2):
        keywords = open('./keywords', 'r')
        keyword = keywords.readline()
        while(keyword):
            results = api.search(keyword, num = expect_num)
            for r in results:
                r.printIt()
            keyword = keywords.readline()
        keywords.close()
    else:
        keyword = sys.argv[1]
        results = api.search(keyword, num = expect_num)
        for r in results:
            r.printIt()

if __name__ == '__main__':
    crawler()
