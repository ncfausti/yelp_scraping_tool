"""
Yelp scraper.

Return all reviews for a given set of yelp URLs
"""


import scrapy
import re
import json
from tutorial.items import YelpItem


class YelpSpider(scrapy.Spider):
    """Main class: return yelp reviews."""
    name = "yelp"
    start_urls = []
    allowed_domains = ["yelp.com", "www.yelp.com"]

    def parse(self, response):
        filename = make_file_name(response.url)

        # Specify a new destination directory here, I'm
        # using CHILDRENS/. This is where the downloaded html
        # files will go
        with open('CHILDRENS/%s' % filename, 'wb') as f:
            print "Writing %s" % filename
            f.write(response.body)

        try:
            match = re.findall(r'ld\+json\">( )(.*)', response.body)
            j = json.loads(match[0][1])
            reviews = j["review"]
            print "Length of Reviews Obj: ", str(len(reviews))
        except IndexError as ie:
            print ie

        for i, review in enumerate(reviews):
            item = YelpItem()
            """
            print "TRYING %s" % response.url
            item["hospital_id"] = response.url.split('biz/')[1].split('?')[0]
            item["url"]         = response.url
            item["review"]      = review
            item["rating"]      = float(ratings[i].extract())
            item["review_date"] = dates[i].extract()
            """
            print "TRYING %s" % response.url

            try:
                item["hospital_id"] = response.url.split('biz/')[1].split('?')[0]
                item["url"] = response.url
                item["review"] = review[u'description']
                item["rating"] = float(review[u'reviewRating'][u'ratingValue'])
                item["review_date"] = review[u'datePublished']
                yield item
            except Exception as e:
                print "ERROR: %s" % e
                print review

    def get_pagination_urls(self, start_url, number_of_reviews):
        """
        INPUT:  starting url and number of reviews for the hospital
        OUTPUT: list of paginated urls
        """
        review_count = 0
        urls = [start_url]

        while review_count < number_of_reviews - 20:
            review_count += 20
            urls.append("%s?start=%d" % (start_url, review_count))
        return urls

    def start_requests(self):
        with open('children_urls_and_counts.csv', 'r') as f:
            for hospital_info in f.readlines():
                url, count = hospital_info.split()
                urls = self.get_pagination_urls(url, int(count))

                for u in urls:
                    yield scrapy.Request(u, callback=self.parse)

def make_file_name(url):
    filename = url.replace('https://www.yelp.com/biz/', '')
    if 'start=' not in filename:
        return filename.split('?')[0] + ".html"
    else:
        page_num = filename.split('start=')[-1]
        filename = filename.split('?')[0]
        return "%s_%s.html" % (filename, page_num)
