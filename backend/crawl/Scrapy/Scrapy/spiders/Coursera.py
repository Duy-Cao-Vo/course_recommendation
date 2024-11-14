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
    # If input is a list, join it into a single string
    if isinstance(text, list):
        text = ' '.join(text)

    # Rest of the normalization code remains the same
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
    #scrapy crawl CourseraSpider -a type=1 -a link=https://www.coursera.org/professional-certificates/google-data-analytics
    #scrapy crawl CourseraSpider -a type=2 -a category=critical%20thinking -a depth=5
    #scrapy crawl CourseraSpider
    #scrapy crawl CourseraSpider -o coursera_datascience.csv -t csv
    def start_requests(self):
        if self.type == '1':
            return [scrapy.Request(url=self.link, callback=self.parse)]
        if self.type == '2':
            link = []
            for i in range(1, int(self.depth) + 1):
                url = 'https://www.coursera.org/courses?query='+ self.category +'&page='+ str(i) +'&index=prod_all_launched_products_term_optimization'
                print("DEBUG url", url)
                html = urlopen(url)
                bs = BeautifulSoup(html, 'html.parser')
                links = [a['href'] for a in bs.find_all('a', {'class': 'cds-119 cds-113 cds-115 cds-CommonCard-titleLink css-si869u cds-142'})]

                print("DEBUG cate links", links)
                if links is not None:
                    for item in links:
                        if '/learn' in item:
                            link.append('https://www.coursera.org' + item)
                else:
                    break
            print("DEBUG all link", link)
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
        with open(
                '/Users/duy.vo/PycharmProjects/course_recommendation/backend/crawl/Scrapy/Scrapy/spiders/response.html',
                'w') as file:
            file.write(response.text)
        print("DEBUG 123")
        Category = response.xpath(
            "//a[@class='cds-119 cds-113 cds-115 cds-breadcrumbs-link css-1lcpylw cds-142']/text()").extract()
        print("DEBUG Category: ", Category)
        if Category:
            Category = Category[-1]
        Course_name = response.xpath(
            "//h1[@class='cds-119 cds-Typography-base css-1xy8ceb cds-121']/text()"
        ).extract_first()
        Link = str(response.url)
        print("DEBUG Link: ", Link)
        Rating = response.xpath("//div[@class='css-139h6xi']//div[@class='cds-119 cds-Typography-base css-h1jogs cds-121']/text()").extract_first()
        TotalEnrolled = response.xpath("//div[@class='css-1qi3xup']//span/strong/span/text()").extract_first()
        Instructor = response.xpath("//div[@class='css-guxf6x']//p[@class=' css-4s48ix']//span[@class=' css-4s48ix']/text()").extract_first()
        print("DEBUG Instructor: ", Instructor)
        Fee = response.xpath(
            "//button[@data-e2e='enroll-button']//span[@data-test='enroll-button-label']/text()").extract_first()

        Program = response.xpath("//div[@data-track='true']//a[@class='cds-119 cds-113 cds-115 css-y0doir cds-142']/text()").extract_first()

        BaseLink = response.xpath("//div[@data-track-component='kim_view_syllabus']/a/@href").extract_first()
        print("DEBUG BaseLink: ", BaseLink)
        print("DEBUG type(BaseLink)", type(BaseLink))
        print("DEBUG type(Link)", type(Link))
        LinkProgram = Link + BaseLink

        OfferBy = response.xpath("//div[@class='css-15g7tpu']//span[@class='css-6ecy9b']/text()").extract()

        LinkInstructors = response.xpath("//div[@class='css-guxf6x']//p[@class=' css-4s48ix']/span/a/@href").extract()
        print("DEBUG LinkInstructors: ", LinkInstructors)
        Subtitle = response.xpath("//span[contains(., 'Subtitles')]/text()").extract_first()
        checkLinkProject = "projects" in str(response.url)
        print("DEBUG checkLinkProject: ", response.url)

        if True:
            Total_Studytime = response.xpath(
                "//div[@class='css-86zyin']//div[@class='css-fw9ih3']//div/text()"
            ).extract_first()
            # Total_Studytime = Total_Studytime.replace('Approx. ', '')
            print("DEBUG Total_Studytime: ", Total_Studytime)
            Level_Requirement = response.xpath("//div[@class='css-7bag3v']//div[@class=' css-fk6qfz']/text()").extract_first()
            print("DEBUG Level_Requirement: ", Level_Requirement)

            Skill_Requirement = response.xpath("//div[@class='css-7bag3v']//p[@class=' css-vac8rf']/text()").extract()
            print("DEBUG Skill_Requirement: ", Skill_Requirement)
            if len(Skill_Requirement)>=2:
                Skill_Requirement = Skill_Requirement[1]
            print("DEBUG Skill_Requirement: ", Skill_Requirement)

            Skill_Learn = response.xpath("//div[@class='css-1m3kxpf']//div[@class='rc-CML unified-CML']//p/span/span/text()").extract()
            print("DEBUG Skill_Learn: ", Skill_Learn)

            Skill_Gain = response.xpath("//ul[@class='css-yk0mzy']//a/text()").extract()
            print("DEBUG Skill_Gain: ", Skill_Gain)
        else:
            checkContent = response.xpath("//h3[contains(., 'What you 'll learn')]/text()").extract_first()
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
            print("DEBUG Skill_Learn2", Skill_Learn)
        if Skill_Gain is not None:
            Skill_Gain = normalizeText(Skill_Gain)
            print("DEBUG Skill_Gain2", Skill_Gain)
        if Subtitle is not None:
            Subtitle = Subtitle.replace("Subtitles: ", "")

        relationIns_Org = []
        for item in LinkInstructors:
            relationIns_Org.append(getInfoInstructor('https://www.coursera.org' + item))

        if Skill_Learn and detect(Skill_Learn) == 'en':
            yield {'name': Course_name, 'link': Link, 'rating': Rating, 'enroll': TotalEnrolled,
                   'instructor': Instructor, 'time': Total_Studytime,
                   'levelrequirement': Level_Requirement, 'skillrequirement': Skill_Requirement,
                   'SkillWillLearn': Skill_Learn, 'Description': '', 'SkillGain': Skill_Gain,
                   'Subject': Category, 'organization': OfferBy, 'fee': Fee, 'program': Program,
                   'linkprogram': LinkProgram, 'RelationInsOrg': relationIns_Org, 'Subtitle': Subtitle}
