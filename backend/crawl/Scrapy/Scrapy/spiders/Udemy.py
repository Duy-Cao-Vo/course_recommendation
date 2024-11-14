import scrapy
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from http.cookies import SimpleCookie
import json
import string
from scrapy_splash import SplashRequest
import re
from lxml import etree

import dpath.util

script = """
function main(splash)
  --User_Agent = 'Mozilla/5.0'
  --splash:set_user_agent(User_Agent)
  --splash.private_mode_enabled = false
  --splash.images_enabled = false

  assert(splash:go(args.url))
  assert(splash:wait(0.5))
  return splash:html()
end
"""

script = """
function main(splash)
    assert(splash:go(splash.args.url))
    local get_dimensions = splash:jsfunc([[
        function () {
            var rect = document.getElementById('button').getClientRects()[0];
            return {"x": rect.left, "y": rect.top}
        }
    ]])
    splash:set_viewport_full()
    splash:wait(0.1)
    local dimensions = get_dimensions()
    splash:mouse_click(dimensions.x, dimensions.y)
    -- Wait split second to allow event to propagate.
    splash:wait(0.1)
    return splash:html()
end
"""
'''
session = requests.Session()
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)'
                         'AppleWebKit 537.36 (KHTML, like Gecko) Chrome',
           'Accept': 'text/html,application/xhtml+xml,application/xml;'
                     'q=0.9,image/webp,*/*;q=0.8'}
url = 'https://www.coursera.org/specializations/boulder-data-structures-algorithms?authMode=login'
req = session.get(url, headers=headers)
params = {'email': '18120158@student.hcmus.edu.vn', 'password': '123ngocbinh'}
s = session.post('https://www.coursera.org/specializations/boulder-data-structures-algorithms?authMode=login',
                 params)
print('Cookie is set to:')
print(s.cookies.get_dict())
print('Going to profile page...')
s = session.get('https://www.coursera.org/specializations/boulder-data-structures-algorithms')
'''


def normalizeText(text):
    text = re.sub(r"(\t)+?|(\\t)+?|(\r)+?|(\\r)+?|(\n)+?|(\\n)+?|(<[^\/].*?>)|(\\xa0)+?|(\xa0)+?|(&nbsp;)|(- )+"
                  r"|(&lt;\/p&gt)+|( &lt;\/p&gt.)+", "", text)
    text = re.sub(r"<\/strong> ", " ", text)
    text = re.sub(r"(<\/.*?>)", "\n", text)
    text = re.sub(r"\n+", "\n", text)
    text = re.sub(r"\\.(\n)|(\n)|[^A-z0-9:?!)]+\n", "\n", text)
    text = re.sub(r"\n+", "\n", text)
    text = re.sub(r"&amp;", "and ", text)
    temp = text.split('\n')
    document = ''
    for i in temp:
        if i == '\n':
            continue
        elif len(i) > 1 and ((i[-1].lower()).isalpha() is True or i[-1] == ')' or i[-1].isnumeric() is True) \
                and i[0] != '\n':
            document = document + i + '. '
        else:
            document = document + i + ' '
    document = document.strip()
    for i in range(2):
        document = re.sub(r"(, )+", ", ", document)
        document = re.sub(r"(\. )+", ". ", document)
        document = re.sub(r"(  )+", " ", document)

    document = re.sub(r"(\. -+)+|\.+[^(\.\.\.) ]", ". ", document)
    document = re.sub(r"(\. ,)+", ",", document)
    document = re.sub(r"(\. :)+|(:\.)", ":", document)
    document = re.sub(r"(\. !)+", "!", document)
    document = re.sub(r"(\. \?)+", "?", document)
    document = re.sub(r"(\. \.)+", ". ", document)
    document = re.sub(r"( • | \. )+", ". ", document)
    document = re.sub(r"( \d.|·|\* |\*|_)+", "", document)
    document = re.sub(r"(  )+", " ", document)
    temp = ''
    x = 0
    y = 0
    for m in re.finditer(r'\. [a-z]|\.[a-z]', text):
        temp = temp + ' ' + document[x:m.start(0)]
        x = m.end(0) - 2
        y = m.start(0) + 1
    temp = temp + ' ' + document[x:]
    temp = re.sub(r"(  )+", " ", temp)
    temp = temp.strip()
    return temp


class UdemyCrawler(scrapy.Spider):
    name = 'UdemySpider'

    allowed_domains = ['udemy.com']

    render_script = """
        function main(splash, args)
          assert(splash:go(args.url))
          assert(splash:wait(10))
          return splash:html()
        end
        """

    def start_requests(self):
        '''
        f = open('C:/Users/Macbook/PycharmProjects/crawldata/Coursera/Coursera/spiders/urluiuxnetwork.json', 'r')
        data = json.load(f)
        linecount = 0
        for i in data:
            link.append(i['url'])
        #Closing file
        f.close()
        '''
        print("DEBUG self.link", self.link)
        if self.type == '1':
            return [SplashRequest(url=item, callback=self.parse,
                                  endpoint='render.html',
                                  args={
                                      'wait': 5,
                                      'lua_source': self.render_script,
                                  }
                                  ) for item in [self.link]]
        # elìf self.type == '2':
        #     return [SplashRequest(url=item, callback=self.parse,
        #                           endpoint='render.html',
        #                           args={
        #                               'wait': 5,
        #                               'lua_source': self.render_script,
        #                           }
        #                           ) for item in [self.link]]

        # scrapy crawl UdemySpider -a type=1 -a link=https://www.udemy.com/course/fearless-public-speaker-bootcamp-by-ricky-mendoza/
    # cd Coursera/Coursera/spiders
    # scrapy runspider Udemy.py
    # scrapy runspider Udemy.py -o udemy_web_software_BI_android.csv -t csv
    def parse(self, response):
        # cur = response.xpath("//div[@class ='component-margin']").extract()
        # print(cur)
        # next_element = etree.HTML(response.xpath("//h2[@class ='ud-heading-xl what-you-will-learn--title--f4aWS']").xpath("following-sibling::*[1]").get()).xpath("//div[@data-purpose ='objective']/div/span/text()")

        # print(next_element)
        with open(
                '/Users/duy.vo/PycharmProjects/course_recommendation/backend/crawl/Scrapy/Scrapy/spiders/response_udemy.html',
                'w') as file:
            file.write(response.text)

        script_content = response.xpath(
            "//script[@data-purpose='safely-set-inner-html:course-landing-page/seo-info']/text()").get()
        json_data = json.loads(script_content)
        print("DEBUG json_data", json_data)

        price = 'Free'
        offers = json_data.get('@graph', [{}])[0].get('offers', [])
        if offers:
            price = offers[0].get('price', 'Free')
        print("DEBUG price", price)

        course_item = [
            # Course_name
            (response.xpath("//title/text()").extract_first()).replace(" | Udemy", ""),
            # link
            response.url,
            # Rating
            response.xpath(
                "//span[@class = 'ud-heading-sm star-rating-module--rating-number--2-qA2']/text()").extract_first(),

            # So hoc vien
            response.xpath("//div[@data-purpose ='enrollment']/text()").extract_first().split(" ")[0],
            # Giang vien
            response.xpath(
                "//a[@class ='ud-btn ud-btn-large ud-btn-link ud-heading-md ud-text-sm ud-instructor-links']/span[@class ='ud-btn-label']/text()").extract()[
                0],
            # Total studytime of course
            response.xpath("//span[@data-purpose='course-content-length--course-content-length--J-A-b']/span/text()").extract_first(),

            # Level Requirement
            # response.xpath("//div[@class ='ProductGlance']//div[@class ='_y1d9czk m-b-2 p-t-1s '][4]//"
            #    "div[@class ='_16ni8zai m-b-0']/text()").extract_first(),
            response.xpath("//div[@data-purpose ='target-audience']/ul/li/text()").extract_first(),
            # Skill Requirement
            ". ".join(etree.HTML(response.xpath("//h2[@data-purpose ='requirements-title']").xpath(
                "following-sibling::*[1]").get()).xpath("//div[@class ='ud-block-list-item-content']/text()") if \
                          len(response.xpath("//h2[@data-purpose ='requirements-title']")) != 0 else [""]),
            # response.xpath("//div[@class='ud-component--course-landing-page-udlite--requirements']/@data-component-props").extract_first(),
            # Skill will learn
            ". ".join(etree.HTML(
                response.xpath("//h2[@class ='ud-heading-xl what-you-will-learn--title--f4aWS']").xpath(
                    "following-sibling::*[1]").get()).xpath("//div[@data-purpose ='objective']/div/span/text()")),
            # response.xpath("//ul[@class ='unstyled-list udlite-block-list what-you-will-learn--objectives-list--2cWZN']").extract_first(),
            # Skill gain
            response.xpath("//div[@class ='Skills p-x-2 p-t-1 p-b-2 skills-combined-with-learning-objs border-a'"
                           "or @class ='Skills p-x-2 p-t-1 p-b-2 skills-sdp-content-exp border-a']"
                           "//span[@class ='_1q9sh65']/text()").extract(),
            # Fee
            price,
            # response.xpath('//div[@class="base-price-text-module--price-part---xQlz ud-clp-discount-price ud-heading-xxl"]').extract_first(),
            # Category
            response.xpath(
                "//div[@class ='topic-menu topic-menu--topic-menu--Cgol5 topic-menu-condensed ud-breadcrumb']/a/text()").extract()[
                -1],
            # response.xpath("//div[@class ='topic-menu udlite-breadcrumb']//a[2]/text()").extract_first(),
            # SubCourse
            response.xpath("//li[@class ='list-inline-item'][5]/a/text()").extract_first(),
            # Description
            response.xpath("//div[@class ='udlite-text-sm  styles--description--3y4KY']//"
                           "div[@data-purpose='safely-set-inner-html:description:description']").get(),
            # Subtitle
            response.xpath("//div[@data-purpose ='lead-headline']/text()").extract_first(),
            # response.xpath("//div[@class ='ud-component--course-landing-page-udlite--caption']"
            #                "/@data-component-props").get(),
        ]
        # print(course_item)
        course_item[3] = re.search(r"\d+.?,*\d+.?,*\d+.?", course_item[3])
        if course_item[13] is not None:
            course_item[13] = normalizeText(course_item[13])
        if course_item[8] is not None:
            course_item[8] = normalizeText(course_item[8])
        if course_item[3] is not None:
            course_item[3] = course_item[3].group()
        if course_item[10] is None:
            course_item[10] = response.xpath("//div[@data-purpose='buy-box']//div[@data-purpose='price-text-container']"
                                             "//div[@data-purpose='course-price-text']/span[2]/text()").extract_first()
        if course_item[5] is None:
            course_item[5] = response.xpath(
                "//div[@class='ud-component--course-landing-page-udlite--course-content-length']//span/text()").extract_first()
        # if course_item[7] is not None:
        #     course_item[7] = re.search(r"\[.+?]", course_item[7])
        #     course_item[7] = course_item[7].group()
        #     course_item[7] = re.sub(r'\["|"]', '', course_item[7])
        #     course_item[7] = re.sub(r'(\.)+', '.', course_item[7])
        #     course_item[7] = re.sub(r'(\\u0026)+', 'and', course_item[7])
        #     course_item[7] = re.sub(r'","', '. ', course_item[7])
        if course_item[14] is not None:
            course_item[14] = re.sub(r'{"captioned_languages":\[|"|]}| \[Auto]', '', course_item[14])

        # yield course_item
        yield {'name': course_item[0], 'link': course_item[1], 'rating': course_item[2], 'enroll': course_item[3],
               'instructor': course_item[4], 'time': course_item[5],
               'levelrequirement': course_item[6], 'skillrequirement': course_item[7], 'SkillWillLearn': course_item[8],
               'Description': course_item[13], 'Subject': course_item[11], 'organization': '',
               'fee': course_item[10], 'program': '',
               'RelationInsOrg': "", 'Subtitle': course_item[14]}
