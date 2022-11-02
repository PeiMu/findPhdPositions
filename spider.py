from urllib.request import Request, urlopen
from link_finder import LinkFinder
from bs4 import BeautifulSoup
import re


class Spider:
    queue = set()

    # Updates user display, fills queue and updates files
    @staticmethod
    def crawl_page(page_url):
        print('now crawling ' + page_url)
        Spider.add_links_to_queue(Spider.gather_links(page_url))
        return Spider.queue

    # Collect author information
    @staticmethod
    def collect_info(page_url):
        req = Request(page_url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urlopen(req)
        content = response.read()
        soup = BeautifulSoup(content, 'html.parser')
        name = ''
        affiliation = ''
        personal_page = ''
        research_interest = ''
        for links in soup.findAll('span'):
            links.unwrap()
        soup_content = str(soup)
        if soup_content.find('Name') != -1:
            name = re.search('Name:(.*?)</div>', soup_content).group(1)
        if soup_content.find('Affiliation') != -1:
            affiliation = re.search('Affiliation:(.*?)</div>', soup_content).group(1)
        if soup_content.find('Personal website') != -1:
            personal_page = re.search('Personal website:<a class="navigate" href="(.*?)">', soup_content).group(1)
        if soup_content.find('Research interests') != -1:
            research_interest = re.search('Research interests:(.*?)</div>', soup_content).group(1)

        return [name, affiliation, personal_page, research_interest]

    # Converts raw response data into readable information and checks for proper html formatting
    @staticmethod
    def gather_links(page_url):
        html_string = ''
        try:
            req = Request(page_url, headers={'User-Agent': 'Mozilla/5.0'})
            response = urlopen(req)
            if 'text/html' in response.getheader('Content-Type'):
                html_bytes = response.read()
                html_string = html_bytes.decode("utf-8")
            finder = LinkFinder(page_url)
            finder.feed(html_string)
        except Exception as e:
            print(str(e))
            return set()
        return finder.page_links()

    @staticmethod
    def add_links_to_queue(links):
        for url in links:
            Spider.queue.add(url)
