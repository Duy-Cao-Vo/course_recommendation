import re
from unicodedata import category
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import string
import json
from scrapy_splash import SplashRequest
import dpath.util
import ast



class CourseraCategoryCrawler(CrawlSpider):
    name = 'CourseraCategorySpider'

    allowed_domains = ['coursera.org', 'udemy.com']

    render_script = """
        function main(splash, args)
          assert(splash:go(args.url))
          assert(splash:wait(10))
          return splash:html()
        end
        """
    '''
    https://www.udemy.com/api-2.0/users/9685726/taught-courses/
    ?context=landing-page&subcontext=morefrominstructor&organizationCoursesOnly=
    false&fields[course]=@default,discount,num_published_lectures,headline,
    instructional_level_simple,avg_rating,
    num_reviews,buyable_object_type,content_info,is_wishlisted,rating,image_100x100,
    is_recently_published,caption_locales,caption_languages,
    locale,is_in_user_subscription&filter_hq_courses=true&ordering=lang,
    -ds_course_feature__revenue_30days&page=1&page_size=4

    https://www.udemy.com/api-2.0/users/9685726/taught-courses/
    ?context=landing-page&subcontext=morefrominstructor&organizationCoursesOnly=
    false&fields[course]=@default,discount,num_published_lectures,headline,
    instructional_level_simple,avg_rating,
    num_reviews,buyable_object_type,content_info,is_wishlisted,rating,
    image_100x100,is_recently_published,caption_locales,caption_languages,locale,
    is_in_user_subscription&filter_hq_courses=true&ordering=lang,
    -ds_course_feature__revenue_30days&page=1&page_size=4
    '''
    
    def start_requests(self):
        domains = [#'https://www.coursera.org/browse/data-science', 
        #'https://www.udemy.com/sitemap/category.xml',
         'https://www.udemy.com/featured-topics/'
        ]
        for domain in domains:
            html = urlopen(domain)
            bs = BeautifulSoup(html, 'html.parser')
            if 'coursera' in domain:
                links = bs.find('div', {'class': 'cds-9 css-0 cds-10'}).find_all('a', href=True)
                link = ['https://www.coursera.org/browse/data-science']
                for item in links:
                    link.append('https://www.coursera.org' + item['href'])
                return [scrapy.Request(url=item, callback=self.parseCoursera)
                        for item in link]
            if 'udemy' in domain:
                # linkUdemy = bs.find_all('loc')
                # link = []
                # for item in linkUdemy:
                #     link.append(item.text)
                # return [scrapy.Request(url = 'https://www.udemy.com/api-2.0/discovery-units/all_courses/?page_size=16&subcategory=&instructional_level=&lang=&price=&duration=&closed_captions=&subs_filter_type=&category_id=288&source_page=category_page&locale=en_US&currency=usd&navigation_locale=en_US&skip_price=true&sos=pc&fl=cat',
                #      method='GET',
                #      body='{"filters": []}',
                #      headers={'X-Requested-With': 'XMLHttpRequest',
                #               'Content-Type': 'application/json; charset=UTF-8'},
                #      callback=self.parseUdemy)]
                return [scrapy.Request(url=domain, callback=self.getCategoryIDUdemy)]

#scrapy crawl CourseraCategorySpider
    #scrapy crawl CourseraSpider -o coursera_datascience.csv -t csv
    def getCategoryIDUdemy(self, response):
        SubCategory = response.xpath("//script[contains(., 'UD.browse')]/text()").extract_first()
        SubCategory = SubCategory.replace('UD.browse = ', '')
        SubCategory = SubCategory.replace('navigation_categories', '"navigation_categories"')
        SubCategory = SubCategory.replace('popular_subcategory_topics', '"popular_subcategory_topics"')
        SubCategory = SubCategory.replace('};', '}')
        data = json.loads(json.dumps(SubCategory))
        print(data)
        SubCategory = SubCategory.replace('}]},            }', '}')
        
        # data = ast.literal_eval(data)
        
        # print(dpath.util.values(json.loads(data), '/navigation_categories/*'))


    def parseCoursera(self, response):
        SubCategory = response.xpath("//div[@class ='_8jjx8os domainSkillsColumn']//span[@class ='_1q9sh65']/text()").extract()
        Category = response.xpath("//h1[@class='cds-113 domain-name css-58nnv2 cds-115']/text()").extract_first()
        
        print(Category, SubCategory)

    def parseUdemy(self, response):
        # print(response.body)
        data = json.loads(json.dumps((response.body).decode()))
        print(dpath.util.values(json.loads(data), '/unit/aggregations/0/options/*'))
        #SubCategory = response.xpath("//div[@class ='panel--panel--3uDOH' and contains(., 'Subcategory')]//label/text()").extract()
        #Category = response.xpath("//h1[@class='udlite-heading-serif-xxl category--heading-primary--2uO95']/text()").extract_first()
        
        # print(Category, SubCategory)
