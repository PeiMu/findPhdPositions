from urllib.request import Request, urlopen
from link_finder import LinkFinder
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse
from urllib.parse import urlencode
import requests


class Spider:
    def __init__(self, api_key, url):
        self.api_key = api_key
        self.queue = set()
        self.url = url

    def get_url(self, url):
        proxy_url = ''
        if self.api_key:
            payload = {'api_key': self.api_key, 'url': url, 'country_code': 'us'}
            proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload)
        else:
            proxy_url = url
        return proxy_url

    # Collect paper information
    def collect_paper(self):
        try:
            r = requests.get(url=self.get_url(self.url))
            content = r.text
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
                paper_link_re = re.search('href="(.*?)"', paper_link)
                if paper_link_re is not None:
                    paper_link = paper_link_re.group(1)
                else:
                    paper_link = paper_link[-1]
                paper_name = paper_re[3]
                paper_map.update({paper_link: paper_name})
        return paper_map

    # Collect author information interface
    def collect_info(self, page_url):
        if page_url.find('ieee') != -1:
            return self.collect_ieee_info(page_url)
        elif page_url.find('acm') != -1:
            return self.collect_acm_info(page_url)
        else:
            print("don't support such conference with ", page_url, "yet")
            return []

    # Collect author information of ieee format
    def collect_ieee_info(self, page_url):
        req = Request(self.get_url(page_url), headers={'User-Agent': 'Mozilla/5.0'})
        response = urlopen(req)
        content = response.read()
        soup = BeautifulSoup(content, 'html.parser')
        name = []
        affiliation = []
        for links in soup.findAll('span'):
            links.unwrap()
        soup_content = str(soup)
        author_re = re.search('"authors":(.*?),"isbn"', soup_content)
        if author_re is not None:
            author_info = author_re.group(1)
            name_re_list = re.findall('"name":"(.*?)",', author_info)
            for name_re in name_re_list:
                if name_re is not None:
                    name.append(name_re)
            affiliation_re_list = re.findall('"affiliation":\["(.*?)"\],', author_info)
            for affiliation_re in affiliation_re_list:
                if affiliation_re is not None:
                    affiliation.append(affiliation_re)
            author_id_re_list = re.findall('"id":"(.*?)"', author_info)
            for author_id_re in author_id_re_list:
                if author_id_re is not None:
                    author_page_link = 'https://' + urlparse(page_url).netloc + '/author/' + author_id_re
                    author_page_req = Request(author_page_link, headers={'User-Agent': 'Mozilla/5.0'})
                    author_page_response = urlopen(author_page_req)
                    author_page_content = author_page_response.read()
                    author_page_soup = BeautifulSoup(author_page_content, 'html.parser')
                    for links in author_page_soup.findAll('span'):
                        links.unwrap()
                    author_page_soup_content = str(author_page_soup)
        assert len(name) == len(affiliation)
        return list(zip(*[name, affiliation]))

    # Collect author information of acm format
    def collect_acm_info(self, page_url):
        req = Request(self.get_url(page_url), headers={'User-Agent': 'Mozilla/5.0'})
        response = urlopen(req)
        content = response.read()
        soup = BeautifulSoup(content, 'html.parser')
        name = []
        affiliation = []
        for links in soup.findAll('span'):
            links.unwrap()
        soup_content = str(soup)
        author_re_list = re.findall('class="author-name"(.*?)View Profile', soup_content)
        for author_re in author_re_list:
            if author_re is not None:
                author_info = author_re
                name_re = re.search('title=(.*?)">(.*?)'
                                    'data-pill-inst="(.*?)>(.*?)</p>(.*?)'
                                    'href="(.*?)"', author_info)
                if name_re is not None:
                    name.append(name_re.group(1))
                    affiliation.append(name_re.group(4))
                    author_profile = name_re.group(6)
                    author_page_link = ''
                    if author_profile.find('https') != -1:
                        author_page_link = author_profile
                    else:
                        author_page_link = 'https://' + urlparse(page_url).netloc + author_profile
                    author_page_req = Request(author_page_link, headers={'User-Agent': 'Mozilla/5.0'})
                    author_page_response = urlopen(author_page_req)
                    author_page_content = author_page_response.read()
                    author_page_soup = BeautifulSoup(author_page_content, 'html.parser')
                    for links in author_page_soup.findAll('span'):
                        links.unwrap()
                    author_page_soup_content = str(author_page_soup)
        assert len(name) == len(affiliation)
        return list(zip(*[name, affiliation]))

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

    def add_links_to_queue(self, links):
        for url in links:
            self.queue.add(url)
