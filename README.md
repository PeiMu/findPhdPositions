# findPhdPositions
Hope this could be helpful when you're struggling with finding a suitable PhD/postDoc position.

## How to use
1. Signup to [Scraper API](https://www.scraperapi.com/signup) to avoid URL protection
   If you really don't want to signup, this tool will also work without pass "key".
2. Run python command in the command line
```python
pip install -r requirements.txt
python main.py -h
python main.py -confs "cgo, compiler construction" -years "2021, 2022" -key "your_key"
```
3. Information will show in the console/terminal and save in "author_info.txt". Enjoy it!

## References
https://github.com/buckyroberts/Spider
https://github.com/sucv/paperCrawler
https://github.com/ian-kerins/google-scholar-scrapy-spider
https://dashboard.scraperapi.com/
