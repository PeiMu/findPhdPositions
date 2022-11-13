# Find the best scholar by the top conferences!
Hope this could be helpful when you're struggling with finding a suitable PhD/postDoc position.

## Ideas
Usually, we read papers from top conferences in our interest area. Then we know which scholars have great works on our interest topics. Thus, we searched their name on google to check out the best scholar's personal page, to find out what they're doing recently and to see if they're looking for a PhD or Post Doc.

This tool gets inspiration from this process. It uses web spider by python to get responses from **google scholar** or a specific conference page (e.g. **code generation and optimization** and **compiler construction**). This tool detects the paper's name and author's name (and the author's other information if it exists), show this information in the console and saves it in a stand-alone file.

## How to use
1. Signup to [Scraper API](https://www.scraperapi.com/signup) to avoid URL protection
   * If you really don't want to signup, this tool will also work without pass "key".
2. Run python command in the command line
```python
pip install -r requirements.txt
python main.py -h
# '-confs': use the full name of conferences or journals
# '-years': list all years instead of ranges
python main.py -confs="code generation and optimization, compiler construction" -years="2020, 2021, 2022" -key="your_key"
```
3. Information will show in the console/terminal and save in "author_info.txt". Enjoy it!

## References
https://github.com/buckyroberts/Spider

https://github.com/sucv/paperCrawler

https://github.com/ian-kerins/google-scholar-scrapy-spider

https://dashboard.scraperapi.com/
