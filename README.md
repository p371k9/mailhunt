# mailhunt

This is a very simple Scrapy crawler and is used to scrape off emails. It does not extract JavaScript-generated content and only searches until the first result.


If we are only searching on one website:
```
scrapy crawl hunter -a url=https://bieler-lang.de/
```

If on multiple sites:
```
scrapy crawl hunter -a list=path/to/list.lll -o list.csv
```
Where **list.lll** is a list file containing URLs. Example list file:
```
http://www.hotelbenczur.hu
https://bieler-lang.de/
https://www.thetravelshopabingdon.com
```

The script only searches web pages that match the strings specified in the **settings.py** **RLS** variable. But the **RLS** list can be changed from the command line just like any Scrapy global. E.g.: 
```
scrapy crawl hunter -a url=https://bieler-lang.de/ -s RLS="['contact', 'about', 'kontakt', 'über']"
```
or:
```
scrapy crawl hunter -a list=path/to/list.de -s RLS="['contact', 'about', 'kontakt', 'über']" -o de.csv
```

