# mailhunt

This is a very simple Scrapy crawler and is used to scrape off emails. It does not extract JavaScript-generated content and only searches until the first result.


If we are only searching on one website:
```
scrapy crawl hunter -a url=https://bieler-lang.de/
```

If on multiple sites:
```
scrapy crawl hunter -a list=path/to/list.de -o de.csv
```
Where **list.de** is a list file containing URLs. Example list file:
```
https://bieler-lang.de/
http://www.hotelbenczur.hu
http://amiidonk.hu
http://nincsilyen.hu
http://www.konyveles-miskolcon.hu/
```

The script only searches web pages that match the strings specified in the **settings.py** **RLS** variable. But the **RLS** list can be changed from the command line just like any Scrapy global. E.g.: 
```
scrapy crawl hunter -a url=https://bieler-lang.de/ -s RLS="['contact', 'about']"
```
or:
```
scrapy crawl hunter -a list=path/to/list.de -s RLS="['contact', 'about']" -o de.csv
```

