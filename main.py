from spider import Spider
from util import get_link
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='find your interest projects!')
    parser.add_argument('-confs', default="code generation and optimization, compiler construction", type=str,
                        help='Which conference would you like to check? '
                             'Please input "conf1, conf2"')
    parser.add_argument('-years', default="2021, 2022", type=str,
                        help='Which years would you like to check? '
                             'Please input "from, to"')
    parser.add_argument('-key', default="", type=str,
                        help='Please input your scraper api key')
    args = parser.parse_args()
    confs = args.confs
    conf_list = confs.lower().split(',')
    years = args.years
    years = years.replace(' ', '')
    year_list = years.split(',')
    key = args.key
    author_info_map = {'paper title': ['name, affiliation, personal_page, research_interest']}
    for conf in conf_list:
        for year in year_list:
            url, is_specific = get_link(conf, year)
            spider = Spider(key, url)
            if is_specific:
                author_info_map.update(spider.collect_conf_researcher_org())
            else:
                author_info_map.update(spider.collect_paper())
    file = 'author_info.txt'
    open(file, "w").close()
    with open(file, 'a') as f:
        for info_key in author_info_map:
            f.write(f"{info_key}\n")
            for info_v in author_info_map[info_key]:
                f.write(f"{info_v}\n")
            f.write(f"\n")
        f.write(f"\n")
    print(author_info_map)
