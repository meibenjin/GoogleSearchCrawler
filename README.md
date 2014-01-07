Google Search Crawler
======================

This is a simple google search results crawler. Before use this tool, please read these tips below.

Requirements
----------------------
1. Python
    
    python should be installed in your computer. here is the official website: http://www.python.org
2. BeautifulSoup
    
    In order to extract search results from google, you would need a html parser, I have used BeautifulSoup. therefore, you need install BeautifulSoup in your python. For more information about BeautifuleSoup, please visit: http://www.crummy.com/software/BeautifulSoup/

Use
----------------------
1. single key word
    
    >python gsearch.py 'your query key words'
    
    It will return about 10 extracted results by default. if you need more results, just change the expect_num value.
2. list of key words
    
    First create a file named keywords, put your key words list into this file, one key word per line. then type the command blow:
    
    >python gsearch.py

3. If there are any problems or bugs about this tool, please contact me.
