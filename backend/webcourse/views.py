from cgitb import html
from unittest import result
from markupsafe import re
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import json

from .models import Career, Career_Program, Course, Framework, Knowledge, Level, Platform, Program, ProgramingLanguage, SearchCourseByName, SimilarCourse, Career_Course, Tool, User, Website
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated
#view for searchCourse
"""
if( request.type==Search)
    list_Course=SearchCourse(request.text)
    list_Course=list(list_Course)
    templateSearchCourse.list_Course=SortbyRating(list_Course)
    if(request.type=filter)
        list_Course=filterCourse(listCourse,request.field,request.value)
    if(request.type==sort)
        list_Course=
"""

class UpdateProfile(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        id = request.data['id']
        level = request.data["level"]
        username = request.data['username']
        hopeCareer = request.data['hopecareer']
        currentCareer = request.data['currentcareer']
        knowledge = request.data['knowledge']
        tool = request.data['tool']
        platform = request.data['platform']
        programinglanguage = request.data['programinglanguage']
        framework = request.data['framework']
        user = User.nodes.get(uid=int(id))
        if username != None and username != "":
            user.name = username
        user.level.disconnect_all()
        user.knowledge.disconnect_all()
        user.tool.disconnect_all()
        user.platform.disconnect_all()
        user.programinglanguage.disconnect_all()
        user.framework.disconnect_all()
        user.current_career.disconnect_all()
        if hopeCareer != None:
            user.hope_career.disconnect_all()
            user.hope_career.connect(Career.nodes.get(creTitle=hopeCareer))
        if currentCareer != None:
            user.current_career.disconnect_all()
            user.current_career.connect(Career.nodes.get(creTitle=currentCareer))
        if level != None:
            user.level.disconnect_all()
            user.level.connect(Level.nodes.get(levName=level))
        for skill in knowledge:
            user.knowledge.connect(Knowledge.nodes.get(value=skill))
        for skill in tool:
            user.tool.connect(Tool.nodes.get(value=skill))
        for skill in platform:
            user.platform.connect(Platform.nodes.get(value=skill))
        for skill in programinglanguage:
            user.programinglanguage.connect(ProgramingLanguage.nodes.get(value=skill))
        for skill in framework:
            user.framework.connect(Framework.nodes.get(value=skill))
        user.save()
        return Response([])
class EnrollCourse(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        user = request.user
        if user.isBasicUser:
            id = request.data['uid']
            courseId = request.data["course_id"]
            user = User.nodes.get(uid=int(id))
            course = Course.get_one(int(courseId))
            if course not in user.enroll:
                if course not in user.complete:
                    user.enroll.connect(course)
                    user.save()
                    return Response("OK",status=status.HTTP_200_OK)
            return Response("OK",status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response("You do not have right to use this function",status=status.HTTP_401_UNAUTHORIZED)

class UnenrollCourse(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        user = request.user
        if user.isBasicUser: 
            id = request.data['uid']
            courseId = request.data["course_id"]
            user = User.nodes.get(uid=int(id))
            course = Course.get_one(int(courseId))
            if course in user.enroll:
                user.enroll.disconnect(course)
            if course in user.complete:
                user.complete.disconnect(course)
            user.save()
            return Response("OK")
        else:
            return Response("You do not have right to use this function", status=status.HTTP_401_UNAUTHORIZED)
class GetEnrollCourses(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        if user.isBasicUser:
            id = request.GET['uid']
            return Response(User.nodes.get(uid=int(id)).get_enroll())
        else:
            return Response("You do not have right to use this function", status=status.HTTP_401_UNAUTHORIZED)

class GetCompleteCourses(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        if user.isBasicUser:
            id = request.GET['uid']
            return Response(User.nodes.get(uid=int(id)).get_complete())
        else:
            return Response("You do not have right to use this function", status=status.HTTP_401_UNAUTHORIZED)

class CompleteCourse(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        user = request.user
        if user.isBasicUser:
            id = request.data['uid']
            courseId = request.data["course_id"]
            user = User.nodes.get(uid=int(id))
            course = Course.get_one(int(courseId))
            if course in user.enroll:
                if course not in user.complete:
                    user.enroll.disconnect(course)
                    user.complete.connect(course)
                    user.save()
            return Response("OK")
        else:
            return Response("You do not have right to use this function", status=status.HTTP_401_UNAUTHORIZED)
class UnCompleteCourse(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        user = request.user
        if user.isBasicUser:
            id = request.data['uid']
            courseId = request.data["course_id"]
            user = User.nodes.get(uid=int(id))
            course = Course.get_one(int(courseId))
            if course not in user.enroll:
                if course in user.complete:
                    user.complete.disconnect(course)
                    user.enroll.connect(course)
                    user.save()
            return Response("OK")
        else:
            return Response("You do not have right to use this function",status=status.HTTP_401_UNAUTHORIZED)
class SearchCourse(APIView):
    def get(self, request, format=None):
        courses = []
        if(request.GET != {}):
            query = request.GET.getlist('query')
            courses = SearchCourseByName(query[0])
            
        else:
            courses = Course.nodes[0:7]
        return Response(map(lambda n:n.to_json(), courses))

class GetUserInformation(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        id = request.GET["id"]
        return Response(User.nodes.get(uid=int(id)).to_json())

class GetUserName(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        id = request.GET["id"]
        return Response(User.nodes.get(uid=int(id)).get_name())
class GetAllWeb(APIView):
    def get(self, request, format=None):
        web = list(map(lambda n:n.to_json(), Website.nodes))
        return Response(web)
class TopPopularCourse(APIView):
    def get(self, request, format=None):
        number = request.GET["number"]
        id = request.GET["uid"]
        courses = Course.nodes.filter(crsFee__gt=0.0).filter(crsEnroll__isnull = False).order_by('-crsEnroll')[0:30]
        count = 0
        index = 0
        array = []
        loop = 1
        if int(id) >= 0:
            user = User.nodes.get(uid=int(id))
            while count < int(number) and index < len(courses):
                if courses[index] not in user.enroll and courses[index] not in user.complete:
                    array.append(courses[index])
                    count = count + 1
                index=index+1
                if index == len(courses) and count < int(number) and len(courses) == 30:
                    start = 30* loop
                    loop = loop + 1
                    end = 30* loop
                    courses = Course.nodes.filter(crsEnroll__isnull = False).order_by('-crsEnroll')[start:end]
                    index = 0
        else:
            array = courses[0:int(number)]
        if(len(array) != 0):
            list_courses = list(map(lambda n:n.to_json(), array))
            return Response(list_courses)
        return Response([])
class TopPopularCourseWeb(APIView):
    def get(self, request, format=None):
        number = request.GET["number"]
        id = request.GET["uid"]
        web = request.GET["web"]
        courses = Course.nodes.filter(crsLink__icontains=web).filter(crsFee__gt=0.0).filter(crsEnroll__isnull = False).order_by('-crsEnroll')[0:30]
        count = 0
        index = 0
        array = []
        loop = 1
        if int(id) >= 0:
            user = User.nodes.get(uid=int(id))
            while count < int(number) and index < len(courses):
                if courses[index] not in user.enroll and courses[index] not in user.complete:
                    array.append(courses[index])
                    count = count + 1
                index=index+1
                if index == len(courses) and count < int(number) and len(courses) == 30:
                    start = 30* loop
                    loop = loop + 1
                    end = 30* loop
                    courses = Course.nodes.filter(crsLink__icontains=web).filter(crsEnroll__isnull = False).order_by('-crsEnroll')[start:end]
                    index = 0
        else:
            array = courses[0:int(number)]
        if(len(array) != 0):
            list_courses = list(map(lambda n:n.to_json(), array))
            return Response(list_courses)
        return Response([])

class TopPopularFromSkill(APIView):
    def get(self, request, format=None):
        value = request.GET["value"]
        type = request.GET["type"]
        number = request.GET["number"]
        courses = []
        short_list = []
        id = request.GET["uid"]
        list_course = []
        array = []
        loop = 1
        if type == "knowledge": 
            courses = Knowledge.nodes.get(value = value).course.filter(crsEnroll__isnull = False).order_by('-crsEnroll')[0:30]
        elif type == "platform":
            courses = Platform.nodes.get(value = value).course.filter(crsEnroll__isnull = False).order_by('-crsEnroll')[0:30]
        elif type == "programinglanguage":
            courses = ProgramingLanguage.nodes.get(value = value).course.filter(crsEnroll__isnull = False).order_by('-crsEnroll')[0:30]
        elif type == "tool":
            courses = Tool.nodes.get(value = value).course.filter(crsEnroll__isnull = False).order_by('-crsEnroll')[0:30]
        elif type == "framework":
            courses = Framework.nodes.get(value = value).course.filter(crsEnroll__isnull = False).order_by('-crsEnroll')[0:30]
        if int(id) >= 0:
            index = 0
            count = 0
            user = User.nodes.get(uid=int(id))
            while count < int(number) and index < len(courses):
                if courses[index] not in user.enroll and courses[index] not in user.complete:
                    array.append(courses[index])
                    count = count+1
                index = index+1
                if index == len(courses) and count < int(number) and len(courses) == 30:
                    start = 30* loop
                    loop = loop + 1
                    end = 30* loop
                    if type == "knowledge": 
                        courses = Knowledge.nodes.get(value = value).course.filter(crsEnroll__isnull = False).order_by('-crsEnroll')[start:end]
                    elif type == "platform":
                        courses = Platform.nodes.get(value = value).course.filter(crsEnroll__isnull = False).order_by('-crsEnroll')[start:end]
                    elif type == "programinglanguage":
                        courses = ProgramingLanguage.nodes.get(value = value).course.filter(crsEnroll__isnull = False).order_by('-crsEnroll')[start:end]
                    elif type == "tool":
                        courses = Tool.nodes.get(value = value).course.filter(crsEnroll__isnull = False).order_by('-crsEnroll')[start:end]
                    elif type == "framework":
                        courses = Framework.nodes.get(value = value).course.filter(crsEnroll__isnull = False).order_by('-crsEnroll')[start:end]
                    index = 0
        else:
            array = courses[0:int(number)]
        if len(array) > 0:
            list_course = list(map(lambda n:n.to_json(), array))
            return Response(list_course)
        return Response([])
        
class FilterCourseBySkill(APIView):
    def get(self, request, format=None):
        courses = []
        knowledge = request.GET.getlist("knowledge[]")
        tool = request.GET.getlist("tool[]")
        platform = request.GET.getlist("platform[]")
        programinglanguage = request.GET.getlist("programinglanguage[]")
        framework = request.GET.getlist("framework[]")
        
        for skill in knowledge:
            for course in Knowledge.nodes.get(value = skill).course:
                if course not in courses:
                    courses.append(course)
        
        for skill in tool:
            for course in Tool.nodes.get(value = skill).course:
                if course not in courses:
                    courses.append(course)

        for skill in platform:
            for course in Platform.nodes.get(value = skill).course:
                if course not in courses:
                    courses.append(course)

        for skill in programinglanguage:
            for course in ProgramingLanguage.nodes.get(value = skill).course:
                if course not in courses:
                    courses.append(course)

        for skill in framework:
            for course in Framework.nodes.get(value = skill).course:
                if course not in courses:
                    courses.append(course)
        result = []
        for course in courses:
            result.append(course.to_json())
        return Response(list(result))

class SpecificCourse(APIView):
    def get(self, request, format=None):
        courses = []
        knowledge = request.GET.getlist("knowledge[]")
        tool = request.GET.getlist("tool[]")
        platform = request.GET.getlist("platform[]")
        programinglanguage = request.GET.getlist("programinglanguage[]")
        framework = request.GET.getlist("framework[]")
        id = request.GET["uid"]
        
        user = User.nodes.get(uid=int(id))
        for skill in knowledge[0:7]:
            for course in Knowledge.nodes.get(value = skill).course:
                if course not in courses:
                    courses.append(course)
        
        for skill in tool[0:7]:
            for course in Tool.nodes.get(value = skill).course:
                if course not in courses:
                    courses.append(course)

        for skill in platform[0:7]:
            for course in Platform.nodes.get(value = skill).course:
                if course not in courses:
                    courses.append(course)

        for skill in programinglanguage[0:7]:
            for course in ProgramingLanguage.nodes.get(value = skill).course:
                if course not in courses:
                    courses.append(course)

        for skill in framework[0:7]:
            for course in Framework.nodes.get(value = skill).course:
                if course not in courses:
                    courses.append(course)
        result = []
        i = 0
        while len(result) <= 40 and i <len(courses):
            if courses[i] not in user.enroll and courses[i] not in user.complete:
                result.append(courses[i].to_json())
            i =i+1
        return Response(list(result))

class GetJobs(APIView):
    def get(self, request, format=None):
        return Response(map(lambda n:n.to_json(), Career.nodes))

class GetJobsHasProgram(APIView):
    def get(self, request, format=None):
        return Response(map(lambda n:n.to_json(), Career.nodes.has(program=True)))
class GetProgram(APIView):
    def get(self, request, format=None):
        id = request.GET["id"]
        program = Program.get_one(int(id))
        if program != None:
            return Response(program.to_json())
        return Response([]) 

class GetSkillByJob(APIView):
    def get(self, request, format=None):
        query = request.GET.getlist("career")
        career = Career.nodes.get(creTitle = query[0])
        knowledges = []
        platforms = []
        techniques = []
        tools = []
        programinglanguages = []
        frameworks = []
        for knowledge in career.knowledge:
            knowledges.append(knowledge)    
        for platform in career.platform:
            platforms.append(platform)           
        for technique in career.technique:
            techniques.append(technique)
        for tool in career.tool:
            tools.append(tool)
        for programinglanguage in career.programinglanguage:
            programinglanguages.append(programinglanguage)
        for framework in career.framework:
            frameworks.append(framework)

        return Response({"knowledges": map(lambda n: n.to_json(), knowledges),
            "platforms": map(lambda n: n.to_json(), platforms),
            "techniques": map(lambda n: n.to_json(), techniques),
            "tools": map(lambda n: n.to_json(), tools),
            "programinglanguages": map(lambda n: n.to_json(), programinglanguages),
            "frameworks": map(lambda n: n.to_json(), frameworks),
        })

class GetSkill(APIView):
    def get(self, request, format=None):
        
        return Response({"knowledges": map(lambda n: n.to_json(), Knowledge.nodes.filter(value__ne="").has(course=True)),
            "platforms": map(lambda n: n.to_json(), Platform.nodes.filter(value__ne="").has(course=True)),
            "tools": map(lambda n: n.to_json(), Tool.nodes.filter(value__ne="").has(course=True)),
            "programinglanguages": map(lambda n: n.to_json(), ProgramingLanguage.nodes.filter(value__ne="").has(course=True)),
            "frameworks": map(lambda n: n.to_json(), Framework.nodes.filter(value__ne="").has(course=True)),
        })

class GetTopFreeCourseOfWeb(APIView):
    def get(self, request, format=None):
        number = request.GET["number"]
        id = request.GET["uid"]
        web = request.GET["web"]
        courses = Course.nodes.filter(crsLink__icontains=web).filter(crsFee=0.0).filter(crsEnroll__isnull = False).order_by('-crsEnroll')[0:30]
        array = []
        loop = 1
        if int(id) >= 0:
            index = 0
            count = 0
            user = User.nodes.get(uid=int(id))
            while count < int(number) and index < len(courses):
                if courses[index] not in user.enroll and courses[index] not in user.complete:
                    array.append(courses[index])
                    count = count+1
                index = index+1

                if index == len(courses) and count < int(number) and len(courses) == 30:
                    start = 30* loop
                    loop = loop + 1
                    end = 30* loop
                    courses = Course.nodes.filter(crsLink__icontains=web).filter(crsFee=0).filter(crsEnroll__isnull = False).order_by('-crsEnroll')[start:end]
                    index = 0
        else:
            array = courses[0:int(number)]
        if len(array) > 0:
            list_course = list(map(lambda n:n.to_json(), array))
            return Response(list_course)
        return Response([])
class GetTopFreeCourse(APIView):
    def get(self, request, format=None):
        number = request.GET["number"]
        id = request.GET["uid"]
        courses = Course.nodes.filter(crsFee=0.0).filter(crsEnroll__isnull = False).order_by('-crsEnroll')[0:30]
        array = []
        loop = 1
        if int(id) >= 0:
            index = 0
            count = 0
            user = User.nodes.get(uid=int(id))
            while count < int(number) and index < len(courses):
                if courses[index] not in user.enroll and courses[index] not in user.complete:
                    array.append(courses[index])
                    count = count+1
                index = index+1

                if index == len(courses) and count < int(number) and len(courses) == 30:
                    start = 30* loop
                    loop = loop + 1
                    end = 30* loop
                    courses = Course.nodes.filter(crsFee=0).filter(crsEnroll__isnull = False).order_by('-crsEnroll')[start:end]
                    index = 0
        else:
            array = courses[0:int(number)]
        if len(array) > 0:
            list_course = list(map(lambda n:n.to_json(), array))
            return Response(list_course)
        return Response([])

class GetSimilarCourses(APIView):
    def get(self, request, format=None):
        id = request.GET["id"]
        reqCourse = Course.get_one(int(id))
        courses=SimilarCourse(reqCourse)
        result = []
        for course in courses[0:3]:
            result.append(Course.nodes.get(crsLink=course[1]).to_json())
        return Response(list(result))

class GetCourseFromCareer(APIView):
    def get(self, request, format=None):
        id = request.GET["id"]
        reqCareer = Career.get_one(int(id))
        courses=Career_Course(reqCareer)
        result = []
        for course in courses[0:10]:
            result.append(Course.nodes.get(crsLink=course[1]).to_json())
        return Response(list(result))

class GetProgramByCareer(APIView):
    def get(self, request, format=None):
        id = request.GET["id"]
        reqCareer = Career.get_one(int(id))
        programs=Career_Program(reqCareer)
        result = []
        for program in programs[0:10]:
            result.append(Program.nodes.get(proName = program[1]).to_json())    
        return Response(list(result))

class TestAPI(APIView):
    def get(self, request, format=None):
        return Response(["Success"])        



