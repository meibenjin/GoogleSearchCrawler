Google Search Crawler
======================

This is a simple google search results crawler. Before use this tool, please read these tips below.

Requirements
----------------------
You may find requirements in `requirements.txt` which can be installed using `pip install -r requirements.txt`

**More info:**

1. Python
    
    python should be installed in your computer. here is the official website: http://www.python.org

2. BeautifulSoup
    
    A html parser to extract search results from Google. BeautifulSoup(version 4) is better. 
    
    For more information about BeautifuleSoup, please visit: http://www.crummy.com/software/BeautifulSoup/

3. dotenv (python-dotenv)

How to Use?
----------------------
1. Rename or copy `.env.example` into `.env`. Apply your own config in this file only.

2. single key word
    
    >python gsearch.py 'your query key words'
    
    It will return about 10 extracted results by default. if you need more results, just change the expect_num value.
3. list of key words
    >python gsearch.py
    
    First create a file named keywords, put your key words list into this file, one key word per line.

If there are any problems or bugs about this tool, please open an issue.
