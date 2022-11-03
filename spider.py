from urllib.request import Request, urlopen
from link_finder import LinkFinder
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse


class Spider:
    queue = set()

    # Updates user display, fills queue and updates files
    @staticmethod
    def crawl_page(page_url):
        print('now crawling ' + page_url)
        Spider.add_links_to_queue(Spider.gather_links(page_url))
        return Spider.queue

    # Collect paper information
    @staticmethod
    def collect_paper(page_url):
        try:
            req = Request(page_url, headers={'User-Agent': 'Mozilla/5.0'})
            response = urlopen(req)
            content = response.read()
            soup = BeautifulSoup(content, 'html.parser')
        except Exception as e:
            print(str(e))
            return set()
        for links in soup.findAll('span'):
            links.unwrap()
        soup_content = str(soup)
        paper_map = {}
        paper_re_list = re.findall('data-clk-atid="(.*?)" href="(.*?) id=(.*?)">(.*?)</a>',
                                   soup_content)
        for paper_re in paper_re_list:
            if paper_re is not None:
                paper_link = paper_re[1]
                paper_link_re = re.search('href="(.*?)/"', paper_link)
                if paper_link_re is not None:
                    paper_link = paper_link_re.group(1)
                else:
                    paper_link = paper_link[-1]
                paper_name = paper_re[3]
                paper_map.update({paper_link: paper_name})
        return paper_map

    # Collect author information interface
    @staticmethod
    def collect_info(page_url):
        if page_url.find('ieee') != -1:
            return Spider.collect_ieee_info(page_url)
        else:
            print("don't support such conference with ", page_url, "yet")
            return []

    # Collect author information of ieee format
    @staticmethod
    def collect_ieee_info(page_url):
        req = Request(page_url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urlopen(req)
        content = response.read()
        soup = BeautifulSoup(content, 'html.parser')
        name = ''
        affiliation = ''
        author_id = ''
        for links in soup.findAll('span'):
            links.unwrap()
        soup_content = str(soup)
        author_re = re.search('"authors":(.*?),"isbn"', soup_content)
        if author_re is not None:
            author_info = author_re.group(1)
            name_re = re.search('"name":"(.*?)",', author_info)
            if name_re is not None:
                name = name_re.group(1)
            affiliation_re = re.search('"affiliation":\["(.*?)"\],', author_info)
            if affiliation_re is not None:
                affiliation = affiliation_re.group(1)
            author_id_re = re.search('"id":"(.*?)"', author_info)
            if author_id_re is not None:
                author_id = author_id_re.group(1)
                author_page_link = 'https://' + urlparse(page_url).netloc + '/author/' + author_id
                author_page_req = Request(author_page_link, headers={'User-Agent': 'Mozilla/5.0'})
                author_page_response = urlopen(author_page_req)
                author_page_content = author_page_response.read()
                author_page_soup = BeautifulSoup(author_page_content, 'html.parser')
                for links in author_page_soup.findAll('span'):
                    links.unwrap()
                author_page_soup_content = str(author_page_soup)
        return [name, affiliation, author_id]

    # Collect author information of cgo format
    @staticmethod
    def collect_cgo_info(page_url):
        req = Request(page_url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urlopen(req)
        content = response.read()
        soup = BeautifulSoup(content, 'html.parser')
        name = ''
        affiliation = ''
        personal_page = ''
        research_interest = ''
        contributed_item = ''
        for links in soup.findAll('span'):
            links.unwrap()
        soup_content = str(soup)
        if soup_content.find('Name') != -1:
            name_re = re.search('Name:(.*?)</div>', soup_content)
            if name_re is not None:
                name = name_re.group(1)
        if soup_content.find('Affiliation') != -1:
            affiliation_re = re.search('Affiliation:(.*?)</div>', soup_content)
            if affiliation_re is not None:
                affiliation = affiliation_re.group(1)
        if soup_content.find('Personal website') != -1:
            personal_page_re = re.search('Personal website:<a class="navigate" href="(.*?)">', soup_content)
            if personal_page_re is not None:
                personal_page = personal_page_re.group(1)
        if soup_content.find('Research interests') != -1:
            research_interest_re = re.search('Research interests:(.*?)</div>', soup_content)
            if research_interest_re is not None:
                research_interest = research_interest_re.group(1)
        if soup_content.find('Contributed Item') != -1:
            soup_content_re = re.search('Contributed Item(.*?)" href="#">(.*?)</a>', soup_content)
            if soup_content_re is not None:
                contributed_item = soup_content_re.group(2)

        return [contributed_item, name, affiliation, personal_page, research_interest]

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
