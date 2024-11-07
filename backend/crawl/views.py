import re
from unittest import result
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
import json
from webcourse.models import Career, Course, Framework, Instructor, Knowledge, Level, Platform, Program, ProgramingLanguage, Subject, SearchCourseByName, SimilarCourse, Tool, Website
from django.http import HttpResponse
import pandas as pd
from subprocess import call
import time
import os
from os import abort
from crawl.crawl_spiders import crawl_spiders
import calendar
from crawl.NER import train
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework import status
import ast
from crawl.database import importCourse, importCourse_Skill, importCareer
from datetime import datetime

#view for searchCourse
def get_scrapy_dir():
    return('crawl/Scrapy/Scrapy/spiders/')

def get_input_file(input_file):
    return('crawl/Scrapy/Scrapy/spiders/inputs/' + input_file)


def ResponseBody(pos, result):
    file_path = result['crawl_output']
    csv_file = pd.DataFrame(pd.read_csv(file_path, sep=",", header=0, index_col=False))
    json_list = json.loads(csv_file.to_json(orient="records"))
    return json_list

class TestAPI(APIView):
    def get(self, request, format=None):
        return Response(["Success"])   

class Crawl(APIView):
    def post(self, request, format=None):
        request_body = request.GET['link']
        crawl_output = request_body['output_file']
        crawl_type = request_body['type']
        spider = crawl_spiders[crawl_type]
        if spider is None:
            abort(486, 'Not suppot yet')
        crawl_output = get_input_file(crawl_output)
        start_time = time.time()
        call(['scrapy', 'crawl', spider, '-o', os.path.join('inputs', crawl_output)], cwd=get_scrapy_dir())
        end_time = time.time() - start_time

        result = {
            'crawl_time': end_time,
            'crawl_output': crawl_output,
        }

        body = ResponseBody(0, result).to_json()
        response = Response(body, status=200, mimetype='application/json')
        return response

@api_view(['POST'])
def CrawlTrain(request):
    request_body = JSONParser().parse(request)

    crawl_type = request_body['type']
    domain = ''
    category='a'
    depth='1'
    link='a'
    if crawl_type == 1:
        link = request_body['linkcrawl']
        domain = (re.search(r'www\..+?\.', link))
        domain = domain.group()
        domain = re.sub('www\.|\.', '', domain)
    if crawl_type == 2:
        domain = (request_body['category'].split('_')[0]).lower()
        category = request_body['category'].split('_')[1]
        category = (category.lower()).replace(' ', '%20')
        depth = request_body['depth']
    if crawl_type == 3:
        domain = request_body['domain']

    spider = crawl_spiders[domain]
    if spider is None:
        abort(486, 'Not suppot yet')

    timestamp = calendar.timegm(time.gmtime())
    input_file = domain + '_' + str(timestamp) + '.csv'
    crawl_output = get_input_file(input_file)

    crawl_start_time = time.time()
    call(['scrapy', 'crawl', spider, '-a', 'type='+str(crawl_type), '-a','category='+category, '-a','link='+link, '-a','depth='+str(depth), '-o', os.path.join('inputs', input_file)], cwd=get_scrapy_dir())
    crawl_end_time = time.time() - crawl_start_time
    train_start_time = time.time()
    train_output = train.predict(input_file=crawl_output, timestamp = timestamp)
    train_end_time = time.time() - train_start_time

    result = {
        'timestamp': timestamp,
        'crawl_time': crawl_end_time,
        'train_time': train_end_time,
        'crawl_output': crawl_output,
        'train_output':train_output
    }

    return Response(
            json.dumps(result, indent = 5)
        , status=status.HTTP_201_CREATED)

@api_view(['POST'])
def CrawlTrainImport(request):
    request_body = JSONParser().parse(request)

    crawl_type = request_body['type']
    score = request_body['score']
    domain = ''
    category='a'
    depth='1'
    link='a'
    if crawl_type == 1:
        link = request_body['linkcrawl']
        domain = (re.search(r'www\..+?\.', link))
        domain = domain.group()
        domain = re.sub('www\.|\.', '', domain)
    if crawl_type == 2:
        domain = (request_body['category'].split('_')[0]).lower()
        category = request_body['category'].split('_')[1]
        category = (category.lower()).replace(' ', '%20')
        depth = request_body['depth']
    if crawl_type == 3:
        domain = request_body['domain']

    spider = crawl_spiders[domain]
    if spider is None:
        abort(486, 'Not suppot yet')

    timestamp = calendar.timegm(time.gmtime())
    input_file = domain + '_' + str(timestamp) + '.csv'
    crawl_output = get_input_file(input_file)

    crawl_start_time = time.time()
    call(['scrapy', 'crawl', spider, '-a', 'type='+str(crawl_type), '-a','category='+category, '-a','link='+link, '-a','depth='+str(depth), '-o', os.path.join('inputs', input_file)], cwd=get_scrapy_dir())
    crawl_end_time = time.time() - crawl_start_time
    train_start_time = time.time()
    train_output = train.predict(input_file=crawl_output, timestamp = timestamp)
    train_end_time = time.time() - train_start_time

    result = {
        'timestamp': timestamp,
        'crawl_time': crawl_end_time,
        'train_time': train_end_time,
        'crawl_output': crawl_output,
        'train_output':train_output
    }
    importCourse(train_output,float(score),datetime.now)
    return Response(
            json.dumps(result, indent = 5)
        , status=status.HTTP_201_CREATED)

@api_view(['POST'])
def GetResultTrain(request):
    request_body = JSONParser().parse(request)
    input_path = request_body['input_path']
    df = pd.read_csv(input_path)
    listResult = []
    for i in range(len(df)):
        know = ast.literal_eval(df['knowledge'][i])
        tool = ast.literal_eval(df['tool'][i])
        framework = ast.literal_eval(df['framework'][i])
        language = ast.literal_eval(df['language'][i])
        soft = ast.literal_eval(df['soft'][i])
        platform = ast.literal_eval(df['platform'][i])
        for j in range(len(know)):
            skill_name, score = know[j].split(' %% ')
            listResult.append({'crs_name': df['name'][i],
                        'link': df['link'][i],
                         'type': 'KNOW',
                        'descriptionNER': df['descriptionNER'][i],
                         'skill_name': skill_name,
                         'score': float(score)})
        for j in range(len(tool)):
            skill_name, score = tool[j].split(' %% ')
            listResult.append({'crs_name': df['name'][i],
                            'link': df['link'][i],
                         'type': 'TOOL',
                         'descriptionNER': df['descriptionNER'][i],
                         'skill_name': skill_name,
                         'score': float(score)})
        for j in range(len(language)):
            skill_name, score = language[j].split(' %% ')
            listResult.append({'crs_name': df['name'][i],
                            'link': df['link'][i],
                         'type': 'LANG',
                         'descriptionNER': df['descriptionNER'][i],
                         'skill_name': skill_name,
                         'score': float(score)})
        for j in range(len(framework)):
            skill_name, score = framework[j].split(' %% ')
            listResult.append({'crs_name': df['name'][i],
                            'link': df['link'][i],
                         'type': 'FRAM',
                         'descriptionNER': df['descriptionNER'][i],
                         'skill_name': skill_name,
                         'score': float(score)})
        for j in range(len(platform)):
            skill_name, score = platform[j].split(' %% ')
            listResult.append({'crs_name': df['name'][i],
                            'link': df['link'][i],
                         'type': 'PLAT',
                         'descriptionNER': df['descriptionNER'][i],
                         'skill_name': skill_name,
                         'score': float(score)})
        for j in range(len(soft)):
            skill_name, score = soft[j].split(' %% ')
            listResult.append({'crs_name': df['name'][i],
                            'link': df['link'][i],
                         'type': 'Softskill',
                         'descriptionNER': df['descriptionNER'][i],
                         'skill_name': skill_name,
                         'score': float(score)})  

    return Response(
            json.dumps(listResult)
        , status=status.HTTP_201_CREATED)

@api_view(['POST'])
def InsertSkillObject(request):
    request_body = JSONParser().parse(request)
    input_path = request_body['input_path']
    skills = request_body['skill']
    importCourse_Skill(input_path, skills)
    return Response(["Success"]) 

@api_view(['GET'])
def GetSumaryDB(request):
    totalNode = Course.nodes.first_or_none().cypher("match(n) return count(n)")
    totalNode = (re.search(r'\d+', str(totalNode)))
    totalNode = totalNode.group()
    totalRelation = Course.nodes.first_or_none().cypher("match(n)-[r]->(m) return count(r)")
    totalRelation = (re.search(r'\d+', str(totalRelation)))
    totalRelation = totalRelation.group()
    totalCourse = len(Course.nodes)
    totalCareer = len(Career.nodes)
    totalKnowledge = len(Knowledge.nodes)
    totalTool = len(Tool.nodes)
    totalTask = len(Career.nodes)
    totalLanguage = len(ProgramingLanguage.nodes)
    totalFramework = len(Framework.nodes)
    totalPlatform = len(Platform.nodes)
    totalInstructor = len(Instructor.nodes)
    totalWeb = len(Website.nodes)
    totalLevel = len(Level.nodes)
    allWebsite = Website.nodes.all()
    totalWebsiteCourse = []
    for item in allWebsite:
        totalWebsiteCourse.append(
            {"webName": item.webName, "numberCrs": len(Website.nodes.get(webName=item.webName).course)})

    allSubject = Subject.nodes.all()
    topSubject = []
    topskill = {}
    for subject in allSubject:
        tmp = []
        topskill = {}
        course_subject = item.course
        for crs in course_subject:
            know = crs.knowledge
            lang = crs.programinglanguage
            plat = crs.platform
            fram = crs.framework
            tool = crs.tool
            for item in know:
                if item.value not in topskill:
                    topskill[item.value] = 1
                else:
                    topskill[item.value] += 1
            for item in lang:
                if item.value not in topskill:
                    topskill[item.value] = 1
                else:
                    topskill[item.value] += 1
            for item in plat:
                if item.value not in topskill:
                    topskill[item.value] = 1
                else:
                    topskill[item.value] += 1
            for item in tool:
                if item.value not in topskill:
                    topskill[item.value] = 1
                else:
                    topskill[item.value] += 1
            for item in fram:
                if item.value not in topskill:
                    topskill[item.value] = 1
                else:
                    topskill[item.value] +=1
        topskill = dict(sorted(topskill.items(), key=lambda item: item[1], reverse=True))
        top = 0
        for key, value in topskill.items():
            if top < 5:
                tmp.append({"name": key})
            else:
                break
            top += 1
        topSubject.append({"subject": subject.Name, "topskill": tmp})
    result = {
            'total_node': totalNode,
            'total_relation': totalRelation,
            'total_course': totalCourse,
            'total_career': totalCareer,
            'total_knowledge': totalKnowledge,
            'total_plaform': totalPlatform,
            'total_framework': totalFramework,
            'total_language': totalLanguage,
            'total_tool': totalTool,
            'total_task': totalTask,
            'total_level': totalLevel,
            'total_web': totalWeb,
            'total_instructor': totalInstructor,
            'web_course': totalWebsiteCourse,
            'subject_topskill': topSubject
        }

    return Response(
            json.dumps(result)
        , status=status.HTTP_201_CREATED)

@api_view(['GET'])
def GetDataForExport(request):
    allCourse = Course.nodes.all()
    allCareer = Career.nodes.all()
    infoCourse = []
    infoCareer = []
    for item in allCourse:
        ins = item.instructor
        level = item.level
        sub = item.subtitle
        provide_lang = item.programinglanguage
        provide_frame = item.framework
        provide_know = item.knowledge
        provide_tool = item.tool
        provide_plat = item.platform
        org = item.organization
        subject = item.subject
        require_lang = item.require_programinglanguage
        require_knowledge = item.require_knowledge
        require_tool = item.require_tool
        require_platform = item.require_platform
        require_framework = item.require_framework
        web = item.website
        program = item.program
        item = item.to_json()
        item['instructor'] = ''
        item['level'] = ''
        item['platform'] = []
        item['tool'] = []
        item['knowledge'] = []
        item['framework'] = []
        item['programinglanguage'] = []
        item['subtitle'] = ''
        item['organization'] = ''
        item['subject'] = ''
        item['require_platform'] = []
        item['require_tool'] = []
        item['require_knowledge'] = []
        item['require_framework'] = []
        item['require_programinglanguage'] = []
        item['website'] = ''
        item['program'] = ''
        for i in ins:
            item['instructor']=item['instructor']+(i.insName)+', '
        item['instructor'] = item['instructor'][:-2]
        for i in sub:
            item['subtitle']=item['subtitle']+(i.subLanguage)+', '
        item['subtitle'] = item['subtitle'][:-2]
        for i in level:
            item['level'] = i.levName
        for i in org:
            item['organization']=item['organization']+(i.orgName)+', '
        item['organization']=item['organization'][:-2]
        for i in subject:
            item['subject'] = i.Name
        for i in web:
            item['website'] = i.webName
        for i in program:
            item['program'] = i.proName
        for i in provide_lang:
            item['programinglanguage'].append(i.value)
        for i in provide_plat:
            item['platform'].append(i.value)
        for i in provide_tool:
            item['tool'].append(i.value)
        for i in provide_know:
            item['knowledge'].append(i.value)
        for i in provide_frame:
            item['framework'].append(i.value)
        for i in require_lang:
            item['require_programinglanguage'].append(i.value)
        for i in require_platform:
            item['require_platform'].append(i.value)
        for i in require_tool:
            item['require_tool'].append(i.value)
        for i in require_knowledge:
            item['require_knowledge'].append(i.value)
        for i in require_framework:
            item['require_framework'].append(i.value)
        infoCourse.append(item)
    for item in allCareer:
        provide_lang = item.programinglanguage
        provide_frame = item.framework
        provide_know = item.knowledge
        provide_tool = item.tool
        provide_plat = item.platform
        item = item.to_json()
        item['platform'] = []
        item['tool'] = []
        item['knowledge'] = []
        item['framework'] = []
        item['programinglanguage'] = []
        for i in provide_lang:
            item['programinglanguage'].append(i.value)
        for i in provide_plat:
            item['platform'].append(i.value)
        for i in provide_tool:
            item['tool'].append(i.value)
        for i in provide_know:
            item['knowledge'].append(i.value)
        for i in provide_frame:
            item['framework'].append(i.value)
        infoCareer.append(item)

    result = {
            'infoCourse': infoCourse,
            'infoCareer': infoCareer
        }
    return Response(
        
            json.dumps(result)
        , status=status.HTTP_201_CREATED)

class getAllCourse(APIView):
    def get(self, request, format=None):
        return Response(list(map(lambda n:n.export(), Course.nodes)))
class getAllCareer(APIView):
    def get(self, request, format=None):
        return Response(list(map(lambda n:n.export(), Career.nodes)))
class NumberCourseInOOP(APIView):
    def get(self, request, format=None):
        return Response(len(Knowledge.nodes.get(vulue="oop").course))