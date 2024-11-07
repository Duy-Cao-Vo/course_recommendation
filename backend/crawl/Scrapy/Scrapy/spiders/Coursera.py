import re
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import string
import json
from langdetect import detect


def getInfoInstructor(url):
    html = urlopen(url)
    bs = BeautifulSoup(html, 'html.parser')
    organizations = bs.find('ul', {'class': 'rc-PartnerLinksV2 list-style-none p-a-0'}).find_all('a')
    instructor_name = bs.find('title').text
    instructor_name = instructor_name.replace(", Instructor | Coursera", "")
    relation = instructor_name + ' work for '
    for item in organizations:
        relation = relation + item.text + ', '
    relation = relation[0:-2]
    return relation


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


class CourseraCrawler(CrawlSpider):
    name = 'CourseraSpider'

    allowed_domains = ['coursera.org']
    #scrapy crawl CourseraSpider -a type=1 -a link=https://www.coursera.org/learn/international-migrations
    #scrapy crawl CourseraSpider -a type=2 -a category=critical%20thinking -a depth=5
    #scrapy crawl CourseraSpider
    #scrapy crawl CourseraSpider -o coursera_datascience.csv -t csv
    def start_requests(self):
        if self.type == '1':
            return [scrapy.Request(url=self.link, callback=self.parse)]
        if self.type == '2':
            link = []
            for i in range(1, int(self.depth) + 1):
                html = urlopen('https://www.coursera.org/courses?query='+ self.category +'&page='+ str(i) +'&index=prod_all_launched_products_term_optimization')
                bs = BeautifulSoup(html, 'html.parser')
                links = bs.find('ul', {'class': 'ais-InfiniteHits-list'})
                if links is not None:
                    tmp = links.find_all('a', href=True)
                    for item in tmp:
                        if '/learn/' in item['href']:
                            link.append('https://www.coursera.org' + item['href'])
                else:
                    break
                print(link)
            return [scrapy.Request(url=item, callback=self.parse)
                    for item in link]
        if self.type == '3':
            link = []
            f = open('C:/Users/Macbook/PycharmProjects/crawldata/Coursera/Coursera/spiders/coursera_IT.json', 'r')
            data = json.load(f)
            for i in data:
                link.append(i['url'])
            # Closing file
            f.close()
            return [scrapy.Request(url=item, callback=self.parse) for item in link]


    def parse(self, response):
        Category = response.xpath("//div[@class ='_exc94g9']//div[@class ='_1ruggxy'][2]//a/text()").extract_first()
        Course_name = response.xpath(
            "//div[@class ='_1bjlpa11 BannerTitle text-xs-left banner-title-container--without-subtitle'"
            "or @class ='_1bjlpa11 BannerTitle text-xs-left banner-title-container--without-subtitle exp-banner-title-container'"
            "or @class ='_1bjlpa11 BannerTitle text-xs-left'"
            "or @class ='_kfriz5q']"
            "/h1/text()").extract_first()
        Link = response.url
        Rating = response.xpath("//div[@class ='_1srkxe1s XDPRating']/span/text()").extract_first()
        TotalEnrolled = response.xpath(
            "//div[@class ='_1fpiay2' or @class ='_1b2af1e']/span/strong/span/text()").extract_first()
        Instructor = response.xpath("//h3[@class ='instructor-name headline-3-text bold']/text()").extract()
        Fee = response.xpath("//div[@class='BannerEnroll']//span[@class='_1lutnh9y']"
                       "//div/text()").extract_first()
        Program = response.xpath("//p[@class ='d-block color-white']/span/a/text()").extract_first()
        LinkProgram = response.xpath("//p[@class ='d-block color-white']/span/a/@href").extract_first()
        OfferBy = response.xpath("//div[@class='PartnerList']//h3[@class='headline-4-text bold rc-Partner__title']"
                       "/text()").extract()
        LinkInstructors = response.xpath("//div[@class='_1vl6vh3k p-y-1 p-r-1']/a/@href").extract()
        Subtitle = response.xpath("//span[contains(., 'Subtitles')]/text()").extract_first()
        checkLinkProject = "projects" in str(response.url)
        if checkLinkProject is True:
            Total_Studytime = response.xpath(
                "//div[@class ='_pu0m129 _b4xh8r'][1]//div[@class ='_8m7gipb _1f096on'][1]//"
                "span/text()").extract_first()
            Level_Requirement = response.xpath(
                "//div[@class ='_pu0m129 _b4xh8r'][1]//div[@class ='_8m7gipb _1f096on'][2]//"
                "span/text()").extract_first()
            Skill_Requirement = response.xpath(
                "//div[@class ='ProductGlance']//div[@class ='_y1d9czk m-b-2 p-t-1s '][4]//"
                "div[@class ='rc-CML show-soft-breaks']//p/text()").extract_first()
            Skill_Learn = response.xpath("//div[@class ='_znrg0e']//p/text()").extract()
            Skill_Gain = response.xpath("//div[@class ='Skills _14ced0o']//div[@class ='_t6niqc3']"
                                        "//span[@class ='_1q9sh65']/text()").extract()
        else:
            checkContent = response.xpath("//h3[contains(., 'What you will learn')]/text()").extract_first()
            checkContent1 = response.xpath("//div[@class='AboutCourse']//h2/text()").extract_first()
            if checkContent is not None:
                Skill_Learn = response.xpath(
                    "//div[@class ='CmlLearningObjectives border-a p-x-2 p-t-1']").get()
            elif checkContent1 is not None:
                Skill_Learn = response.css(
                    "div.m-t-1.description div.rc-TogglableContent.about-section.collapsed "
                    "div.content").get()
            else:
                Skill_Learn = response.css("div.m-t-1 description").get()


            Total_Studytime = response.xpath(
                "//span[contains(., 'Approx')]/text()").extract_first()
            Level_Requirement = response.xpath(
                "//div[contains(., 'Level')]/text()").extract_first()
            Skill_Requirement = response.xpath(
                "//div[@class ='ProductGlance']//div[@class ='_y1d9czk m-b-2 p-t-1s '][5]//"
                "div[@class ='rc-CML show-soft-breaks']//p/text()").extract_first()
            Skill_Gain = response.xpath(
                "//div[@class = 'Skills m-y-2 p-x-2 p-t-1 p-b-2 border-a css-1rj0z6b' or @class='Skills p-x-2 p-t-1 p-b-2 skills-combined-with-learning-objs border-a css-1rj0z6b' and contains(., 'Skills you will gain')]").extract_first()
       
        if Level_Requirement is not None:
            Level_Requirement = Level_Requirement.split(" ")[0]
        if Total_Studytime is not None: 
            Total_Studytime = re.search(r'\d+.?(hours|months|month|hour)', Total_Studytime)
            Total_Studytime = Total_Studytime.group()
        if Skill_Learn is not None:
            Skill_Learn = normalizeText(Skill_Learn)
            Skill_Learn = re.sub("(\['|(\n)+?|']|\[|\]|(\u200b)+?)+?", '', Skill_Learn)
        if Skill_Gain is not None:
            Skill_Gain = Skill_Gain.replace("  Skills you will gain        ", "")
            Skill_Gain = normalizeText(Skill_Gain)
        if Subtitle is not None:
            Subtitle = Subtitle.replace("Subtitles: ", "")
        if LinkProgram is not None:
            LinkProgram = 'https://www.coursera.org' + LinkProgram

        relationIns_Org = []
        for item in LinkInstructors:
            relationIns_Org.append(getInfoInstructor('https://www.coursera.org' + item))

        if detect(Skill_Learn) == 'en':
            yield {'name': Course_name, 'link': Link, 'rating': Rating, 'enroll': TotalEnrolled,
               'instructor': Instructor, 'time': Total_Studytime,
               'levelrequirement': Level_Requirement, 'skillrequirement': Skill_Requirement,
               'SkillWillLearn': Skill_Learn, 'Description': '',  'SkillGain': Skill_Gain,
               'Subject': Category, 'organization': OfferBy, 'fee': Fee, 'program': Program,
               'linkprogram': LinkProgram, 'RelationInsOrg': relationIns_Org, 'Subtitle': Subtitle}
