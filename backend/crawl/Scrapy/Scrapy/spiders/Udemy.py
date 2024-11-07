import scrapy
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from http.cookies import SimpleCookie
import json
import string
from scrapy_splash import SplashRequest
import re
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
        link = ['https://www.udemy.com/course/introduction-to-oracle-database-backup-and-security/',]
        '''
        f = open('C:/Users/Macbook/PycharmProjects/crawldata/Coursera/Coursera/spiders/urluiuxnetwork.json', 'r')
        data = json.load(f)
        linecount = 0
        for i in data:
            link.append(i['url'])
        #Closing file
        f.close()
        '''
        return [SplashRequest(url=item, callback=self.parse,
                            endpoint='render.html',
                            args={
                                'wait': 5,
                                'lua_source': self.render_script,
                            }
                            )
                for item in link]


    # cd Coursera/Coursera/spiders
    # scrapy runspider Udemy.py
    # scrapy runspider Udemy.py -o udemy_web_software_BI_android.csv -t csv
    def parse(self, response):
        #print(response.body)
        course_item = [
            # Course_name
            (response.xpath("//title/text()").extract_first()).replace(" | Udemy", ""),
            # link
            response.url,
            # Rating
            response.xpath(
                "//span[@class = 'udlite-heading-sm star-rating--rating-number--2o8YM']/text()").extract_first(),
            # So hoc vien
            response.xpath("//div[@data-purpose ='enrollment']/text()").extract_first(),
            # Giang vien
            response.xpath("//div[@class ='instructor--instructor--1wSOF']"
                           "//div[@class = 'udlite-heading-lg udlite-link-underline instructor--instructor__title--34ItB']/a/text()").extract(),
            # Total studytime of course
            response.xpath("//span[@data-purpose='video-content-length']/text()").extract_first(),
            # Level Requirement
            response.xpath("//div[@class ='ProductGlance']//div[@class ='_y1d9czk m-b-2 p-t-1s '][4]//"
                           "div[@class ='_16ni8zai m-b-0']/text()").extract_first(),
            # Skill Requirement
            response.xpath("//div[@class='ud-component--course-landing-page-udlite--requirements']/@data-component-props").extract_first(),
            # Skill will learn
            response.xpath("//ul[@class ='unstyled-list udlite-block-list what-you-will-learn--objectives-list--2cWZN']").extract_first(),
            # Skill gain
            response.xpath("//div[@class ='Skills p-x-2 p-t-1 p-b-2 skills-combined-with-learning-objs border-a'"
                           "or @class ='Skills p-x-2 p-t-1 p-b-2 skills-sdp-content-exp border-a']"
                           "//span[@class ='_1q9sh65']/text()").extract(),
            #Fee
            response.xpath("//div[@data-purpose='buy-box']//div[@data-purpose='price-text-container']"
                           "//div[@data-purpose='course-price-text']/span[2]/span/text()").extract_first(),
            # Category
            response.xpath("//div[@class ='topic-menu udlite-breadcrumb']//a[2]/text()").extract_first(),
            # SubCourse
            response.xpath("//li[@class ='list-inline-item'][5]/a/text()").extract_first(),
            # Description
            response.xpath("//div[@class ='udlite-text-sm  styles--description--3y4KY']//"
                           "div[@data-purpose='safely-set-inner-html:description:description']").get(),
            # Subtitle
            response.xpath("//div[@class ='ud-component--course-landing-page-udlite--caption']"
                           "/@data-component-props").get(),
        ]
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
            course_item[5] = response.xpath("//div[@class='ud-component--course-landing-page-udlite--course-content-length']//span/text()").extract_first()
        if course_item[7] is not None:
            course_item[7] = re.search(r"\[.+?]", course_item[7])
            course_item[7] = course_item[7].group()
            course_item[7] = re.sub(r'\["|"]', '', course_item[7])
            course_item[7] = re.sub(r'(\.)+', '.', course_item[7])
            course_item[7] = re.sub(r'(\\u0026)+', 'and', course_item[7])
            course_item[7] = re.sub(r'","', '. ', course_item[7])
        if course_item[14] is not None:
            course_item[14] = re.sub(r'{"captioned_languages":\[|"|]}| \[Auto]','',course_item[14])

        # yield course_item
        yield {'name': course_item[0], 'link': course_item[1],'rating': course_item[2], 'enroll': course_item[3],
               'instructor': course_item[4], 'time': course_item[5],
               'levelrequirement': "", 'skillrequirement': course_item[7], 'SkillWillLearn': course_item[8],
               'Description': course_item[13], 'Subject': course_item[11], 'organization': '',
               'fee': course_item[10], 'program': '',
               'RelationInsOrg': "", 'Subtitle': course_item[14]}
