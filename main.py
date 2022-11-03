from spider import Spider

# url = 'https://conf.researchr.org/track/cgo-2021/cgo-2021-papers?#event-overview'
# url = 'https://conf.researchr.org/track/cgo-2022/cgo-2022-main-conference#event-overview'
# url = 'https://conf.researchr.org/track/CC-2021/cc-research-papers?#event-overview'
url = 'https://conf.researchr.org/track/CC-2022/CC-2022-research-papers#event-overview'
spider = Spider()
paper_lists = spider.crawl_page(url)
author_info_lists = []
file = 'author_info.txt'
open(file, "w").close()
for link in paper_lists:
    if link.find('/profile/') != -1:
        author_info_lists = spider.collect_info(link)
        author_info_lists = list(filter(None, author_info_lists))
        if len(author_info_lists) > 2:
            with open(file, 'a') as f:
                for info in author_info_lists:
                    f.write(f"{info}\n")
                f.write(f"\n")
        print(author_info_lists)
