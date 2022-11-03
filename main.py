from spider import Spider
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='find your interest projects!')
    parser.add_argument('-confs', default="cgo, compiler construction", type=str,
                        help='Which conference would you like to check? '
                             'Please input "conf1, conf2"')
    parser.add_argument('-years', default="2021, 2022", type=str,
                        help='Which years would you like to check? '
                             'Please input "from, to"')
    args = parser.parse_args()
    confs = args.confs
    # confs = confs.replace(' ', '')
    conf_list = confs.split(',')
    years = args.years
    years = years.replace(' ', '')
    year_list = years.split(',')
    if len(year_list) == 1:
        year_list.append(year_list[0])
    # url = 'https://conf.researchr.org/track/cgo-2021/cgo-2021-papers?#event-overview'
    for conf in conf_list:
        conf_name = conf.split(' ')
        url_pre = 'https://scholar.google.com/scholar?as_q=&as_epq=&as_oq=&as_eq=&as_occt=any&as_sauthors' \
                  '=&as_publication='
        url_year = '&as_ylo='+year_list[0]+'&as_yhi='+year_list[1]+'&hl=en&as_sdt=0%2C5'
        url_name = ''
        for c_name in conf_name:
            if c_name != '':
                url_name += '+'+c_name
        url = url_pre + url_name[1:] + url_year
        spider = Spider()
        paper_info = spider.collect_paper(url)
        # paper_lists = spider.crawl_page(url)
        author_info_map = {'paper title': ['name',
                                           'affiliation',
                                           'personal_page',
                                           'research_interest']}
        # file = 'author_info.txt'
        # open(file, "w").close()
        for link in paper_info:
            author_info = spider.collect_info(link)
            author_info = list(filter(None, author_info))
            if not author_info:
                print(link, '\t', paper_info[link])
                continue
            # if author_info[0] in author_info_map:
            author_info_map[author_info[0]] = author_info[1:]
            # if len(author_info_map) > 3:
            #     with open(file, 'a') as f:
            #         for info in author_info_map:
            #             f.write(f"{info}\n")
            #         f.write(f"\n")
            print(author_info_map)
