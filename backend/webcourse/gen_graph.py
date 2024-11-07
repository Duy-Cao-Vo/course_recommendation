import json
from msilib import knownbits
from django.db import models
from os import name
from django.db import models
from io import BytesIO
from PIL import Image
from neo4j import GraphDatabase
from django.core.files import File
from neomodel.properties import FloatProperty, IntegerProperty,DateTimeProperty
import pandas as pd
# from neomodel import config
from neomodel import Q, db
# config.DATABASE_URL ='bolt://neo4j:1@localhost:7687'
# Create your models here.
from neomodel import StructuredNode, StringProperty, DateProperty, RelationshipTo, RelationshipFrom,FloatProperty
from neomodel import StructuredRel
import random
db.set_connection("bolt://neo4j:1@localhost:7687")

class Infor(StructuredNode):
    Username=StringProperty()
    Pass=StringProperty()
    user=RelationshipFrom("User","HAS_INFOR")
class User(StructuredNode):
    Create_Date=DateTimeProperty()
    Update_Date=DateTimeProperty()
    Name=StringProperty()
    education=StringProperty()
    current_career=RelationshipTo("Career","HAS_CURRENT_CAREER")
    hope_career=RelationshipTo("Career","HAS_HOPE_CAREER")
    infor=RelationshipTo("Infor","Has_INFOR")
    enroll=RelationshipTo("Course","ENROLL")
    complete=RelationshipTo("Course","COMPLETE")
    knowledge=RelationshipTo("Knowledge","HAS_KNOWLEDGE")
    tool=RelationshipTo("Tool","HAS_TOOL")
    platform=RelationshipTo("Platform","HAS_PLATFORM")
    framework=RelationshipTo("Framework","HAS_FRAMEWORK")
    programinglanguage=RelationshipTo("ProgramingLanguage","HAS_PROGRAMINGLANGUAGE")


class Subject(StructuredNode):
    Name=StringProperty()
    Create_Date=DateTimeProperty()
    Update_Date=DateTimeProperty()
    careers=RelationshipFrom("Career","BELONG")
    def to_json(self):
        return {
         "id": self.id,
         "value": self.Name
        }

class Index(StructuredRel):
    Index=IntegerProperty()
class Website(StructuredNode):
    webName=StringProperty()
    course=RelationshipFrom("Course","IS_IN")
    def to_json(self):
        return {
         "id": self.id,
         "value": self.webName   
        }
    
class Organization(StructuredNode):
    orgName=StringProperty()
    instructor=RelationshipFrom("Instructor","WORK_AT")
    course=RelationshipFrom("Course","COLLABORATE_WITH")
    def to_json(self):
        return {
         "id": self.id,
         "value": self.orgName   
        }

class Instructor(StructuredNode):
    insName=StringProperty()
    organization=RelationshipTo("Organization","WORK_AT")
    course=RelationshipTo("Course","INSTRUCT_BY")
    def to_json(self):
        return {
         "id": self.id,
         "value": self.insName
        }

class SubTitle(StructuredNode):
    subLanguage=StringProperty()
    course=RelationshipFrom("Course","TEACH_IN")
    def to_json(self):
        return {
         "id": self.id,
         "value": self.subLanguage
        }

class Level(StructuredNode):
    levName=StringProperty()
    course=RelationshipFrom("Course","HAS_LEVEL")
    def to_json(self):
        return {
         "id": self.id,
         "value": self.levName
        }

class Course(StructuredNode):
    crsFee=FloatProperty()
    crsLink=StringProperty()
    crsRating=FloatProperty()
    crsEnroll=IntegerProperty()
    crsName = StringProperty()
    crsTime=StringProperty()
    subtitle=RelationshipTo("SubTitle","TEACH_IN")
    organization=RelationshipTo("Organization","COLLABORATE_WITH")
    instructor=RelationshipFrom("Instructor","INSTRUCT_BY")
    level=RelationshipTo("Level","HAS_LEVEL")
    website=RelationshipTo("Website","IS_IN")
    subject=RelationshipTo("Subject","BELONG")
    knowledge=RelationshipTo("Knowledge","TEACH_KNOWLEDGE")
    platform=RelationshipTo("Platform","TEACH_PLATFORM")
    tool = RelationshipTo("Tool", "TEACH_TOOL")
    programinglanguage = RelationshipTo("ProgramingLanguage", "TEACH_PROGRAMINGLANGUAGE")
    framework = RelationshipTo("Framework", "TEACH_FRAMEWORK")
    require_knowledge=RelationshipTo("Knowledge","NEED_KNOWLEDGE")
    require_platform=RelationshipTo("Platform","NEED_PLATFORM")
    require_tool = RelationshipTo("Tool", "NEED_TOOL")
    require_programinglanguage = RelationshipTo("ProgramingLanguage", "NEED_PROGRAMINGLANGUAGE")
    require_framework = RelationshipTo("Framework", "NEED_FRAMEWORK")
    enroll=RelationshipFrom("User","ENROLL")
    complete=RelationshipFrom("User","COMPLETE")
    program=RelationshipFrom("Program","INCLUDE_COURSE",model=Index)

    def to_json(self):
        return {
            "id": self.id,
            "crsEnroll": self.crsEnroll,
            "crsName": self.crsName,
            "crsTime": self.crsTime,
            "crsFee": self.crsFee,
            "crsLink": self.crsLink,
            "crsRating": self.crsRating,
            "crsEnroll": self.crsEnroll,
            "subtitle": list(map(lambda n: n.to_json(), self.subtitle)),
            "organization": list(map(lambda n: n.to_json(), self.organization)),
            "instructor": list(map(lambda n: n.to_json(), self.instructor)),
            "level": list(map(lambda n: n.to_json(), self.level)),
            "subject": list(map(lambda n: n.to_json(), self.subject)),
            "knowledge":list( map(lambda n: n.to_json(), self.knowledge)),
            "platform": list(map(lambda n: n.to_json(), self.platform)),
            "programinglanguage": list(map(lambda n: n.to_json(), self.programinglanguage)),
            "tool": list(map(lambda n: n.to_json(), self.tool)),
            "framework": list(map(lambda n: n.to_json(), self.framework)),
            "require_knowledge":list( map(lambda n: n.to_json(), self.require_knowledge)),
            "require_platform": list(map(lambda n: n.to_json(), self.require_platform)),
            "require_tool": list(map(lambda n: n.to_json(), self.require_tool)),
            "require_programinglanguage": list(map(lambda n: n.to_json(), self.require_programinglanguage)),
            "require_framework": list(map(lambda n: n.to_json(), self.require_framework)),
        }
    def get_one(id):
        try:
            model = Course(id=id)
            model.refresh()
            return model
        except:
            return None
    
class Career(StructuredNode):
    creCreate_Date=DateTimeProperty()
    creUpdate_Date=DateTimeProperty()
    creTitle = StringProperty()
    creMedianSalary=StringProperty()
    creDescription=StringProperty()
    knowledge=RelationshipTo("Knowledge","NEED_KNOWLEDGE")
    platform=RelationshipTo("Platform","NEED_PLATFORM")
    tool = RelationshipTo("Tool", "NEED_TOOL")
    programinglanguage = RelationshipTo("ProgramingLanguage", "NEED_PROGRAMINGLANGUAGE")
    framework = RelationshipTo("Framework", "NEED_FRAMEWORK")
    current=RelationshipFrom("User","HAS_CURRENT_CAREER")
    hope=RelationshipTo("User","HAS_HOPE_CAREER")
    program=RelationshipTo("Program","HAS_PROGRAM")
    def to_json(self):
        return {
        "id": self.id,
        "creTitle": self.creTitle,
        "knowledge": list(map(lambda n: n.to_json(), self.knowledge)),
        "platform": list(map(lambda n: n.to_json(), self.platform)),
        "programinglanguage": list(map(lambda n: n.to_json(), self.programinglanguage)),
        "tool": list(map(lambda n: n.to_json(), self.tool)),
        "framework": list(map(lambda n: n.to_json(), self.framework)), 
        }
    def get_one(id):
        try:
            model = Career(id=id)
            model.refresh()
            return model
        except:
            return None
class Program(StructuredNode):
    Create_Date=DateTimeProperty()
    Update_Date=DateTimeProperty()
    proName=StringProperty()
    course=RelationshipTo("Course","INCLUDE_COURSE",model=Index)
    career=RelationshipFrom("Career","HAS_PROGRAM")
    knowledge=RelationshipTo("Knowledge","HAS_KNOWLEDGE")
    platform=RelationshipTo("Platform","HAS_PLATFORM")
    tool = RelationshipTo("Tool", "HAS_TOOL")
    programinglanguage = RelationshipTo("ProgramingLanguage", "HAS_PROGRAMINGLANGUAGE")
    framework = RelationshipTo("Framework", "HAS_FRAMEWORK")
    def to_json(self):
        return {
         "id": self.id,
         "proName": self.proName,
         "course": map(lambda n: n.to_json(), self.course),
        }
    def get_one(id):
        try:
            model = Program(id=id)
            model.refresh()
            return model
        except:
            return None

class Knowledge(StructuredNode):
    Create_Date=DateTimeProperty()
    Update_Date=DateTimeProperty()
    value=StringProperty()
    course=RelationshipFrom("Course","TEACH_KNOWLEDGE")
    require_course=RelationshipFrom("Course","NEED_KNOWLEDGE")
    career=RelationshipFrom("Career","NEED_KNOWLEDGE")
    user=RelationshipFrom("User","HAS_KNOWLEDGE")
    tool=RelationshipTo("Tool","USE_TOOL")
    platform=RelationshipTo("Platform","USE_PLATFORM")
    framework=RelationshipTo("Framework","USE_FRAMEWORK")
    programinglanguage=RelationshipTo("ProgramingLanguage","USE_PROGRAMINGLANGUAGE")
    def to_json(self):
        return {
         "id": self.id,
         "value": self.value
        }
   
class Tool(StructuredNode):
    Create_Date=DateTimeProperty()
    Update_Date=DateTimeProperty()
    value=StringProperty()
    course=RelationshipFrom("Course","TEACH_TOOL")
    require_course=RelationshipFrom("Course","NEED_TOOL")
    career=RelationshipFrom("Career","NEED_TOOL")
    user=RelationshipFrom("User","HAS_TOOL")

    knowledge=RelationshipFrom("Knowledge","USE_TOOL")
    programinglanguage=RelationshipTo("ProgramingLanguage","INTERACT_LANG")
    def to_json(self):
        return {
         "id": self.id,
         "value": self.value
        }

class Platform(StructuredNode):
    Create_Date=DateTimeProperty()
    Update_Date=DateTimeProperty()
    value=StringProperty()
    course=RelationshipFrom("Course","TEACH_PLATFORM")
    require_course=RelationshipFrom("Course","NEED_COURSE")
    career=RelationshipFrom("Career","NEED_PLATFORM")
    user=RelationshipFrom("User","HAS_PLATFORM")
    knowledge=RelationshipFrom("Knowledge","USE_PLATFORM")
    framework=RelationshipFrom("Framework","DEPLOY_PLAT")
    def to_json(self):
        return {
         "id": self.id,
         "value": self.value
        }

class Framework(StructuredNode):
    Create_Date=DateTimeProperty()
    Update_Date=DateTimeProperty()
    value=StringProperty()
    course=RelationshipFrom("Course","TEACH_FRAMEWORK")
    require_course=RelationshipFrom("Course","NEED_COURSE")
    career=RelationshipFrom("Career","NEED_FRAMEWORK")
    user=RelationshipFrom("User","HAS_FRAMEWORK")
    knowledge=RelationshipFrom("Knowledge","USE_FRAMEWORK")
    platform=RelationshipTo("Platform","DEPLOY_PLAT")
    programinglanguage=RelationshipTo("ProgramingLanguage","NEED_LANG")
    def to_json(self):
        return {
         "id": self.id,
         "value": self.value
        }

class ProgramingLanguage(StructuredNode):
    Create_Date=DateTimeProperty()
    Update_Date=DateTimeProperty()
    value=StringProperty()
    course=RelationshipFrom("Course","TEACH_PROGRAMINGLANGUAGE")
    user=RelationshipFrom("User","HAS_PROGRAMINGLANGUAGE")
    require_course=RelationshipFrom("Course","NEED_PROGRAMINGLANGUAGE")
    career=RelationshipFrom("Career","NEED_PROGRAMINGLANGUAGE")
    knowledge=RelationshipFrom("Knowledge","USE_LANG")
    tool=RelationshipFrom("Tool","INTERACT_LANG")
    framework=RelationshipFrom("Framework","NEED_LANG")
    def to_json(self):
        return {
         "id": self.id,
         "value": self.value,
        }


def SortCoursebyEnroll(list_Course):
    def key_Enroll(course):
        b=course.__properties__
        return b['Enroll']
    list_Course.sort(reverse=True,key=key_Enroll)
def SearchCourseByName(text):
    return Course.nodes.filter(Q(crsName__contains=text))

def filterCourse(Courses,field,value):
    if (field=='Duration'):
       print('khi nao co duration thì tính sau')
    return Courses.filter(field=value)

def Program_Skill():
    program=Program.nodes.all()
    for p in program:
        courses=p.course
        for i in courses:
            if(i.tool !=None):
                for j in i.tool:
                    p.tool.connect(j)
            if(i.knowledge !=None):
                for j in i.knowledge:
                    p.knowledge.connect(j)
            if(i.platform !=None):
                for j in i.platform:
                    p.platform.connect(j)
            if(i.framework !=None):
                for j in i.framework:
                    p.framework.connect(j)
            if(i.programinglanguage !=None):
                for j in i.programinglanguage:
                    p.programinglanguage.connect(j)
    

def Create_Graph():
    querycareer="""CALL gds.graph.create('careergraph',['Career', 'Framework','ProgramingLanguage','Tool','Program','Knowledge'],
    {
        HAS_FRAMEWORK:{type:'HAS_FRAMEWORK'}
      ,HAS_PROGRAMINGLANGUAGE:{type:'HAS_PROGRAMINGLANGUAGE'}
        ,HAS_TOOL:{type:'HAS_TOOL'}
        ,HAS_PLATFORM:{type:'HAS_PLATFORM'}
        ,HAS_KNOWLEDGE:{type:'HAS_KNOWLEDGE'}
        ,NEED_FRAMEWORK:{type:'NEED_FRAMEWORK'}
        ,NEED_PROGRAMINGLANGUAGE:{type:'NEED_PROGRAMINGLANGUAGE'}
        ,NEED_TOOL:{type:'NEED_TOOL'}
        ,NEED_PLATFORM:{type:'NEED_PLATFORM'}
        ,NEED_KNOWLEDGE:{type:'NEED_KNOWLEDGE'}
    }
);
"""
    querycourse="""CALL gds.graph.create('coursegraph',['Course', 'Framework','ProgramingLanguage','Tool','Platform','Knowledge'],
    {
        
        ,TEACH_FRAMEWORK:{type:'TEACH_FRAMEWORK'}
        ,TEACH_PROGRAMINGLANGUAGE:{type:'TEACH_PROGRAMINGLANGUAGE'}
        ,TEACH_TOOL:{type:'TEACH_TOOL'}
        ,TEACH_PLATFORM:{type:'TEACH_PLATFORM'}
        ,TEACH_KNOWLEDGE:{type:'TEACH_KNOWLEDGE'}
    }
);
"""
    query="""CALL gds.graph.create('graph',['Course',"Career", 'Framework','ProgramingLanguage','Tool','Platform','Knowledge'],
    {
        
        ,TEACH_FRAMEWORK:{type:'TEACH_FRAMEWORK'}
        ,TEACH_PROGRAMINGLANGUAGE:{type:'TEACH_PROGRAMINGLANGUAGE'}
        ,TEACH_TOOL:{type:'TEACH_TOOL'}
        ,TEACH_PLATFORM:{type:'TEACH_PLATFORM'}
        ,TEACH_KNOWLEDGE:{type:'TEACH_KNOWLEDGE'}
        ,NEED_FRAMEWORK:{type:'NEED_FRAMEWORK'}
        ,NEED_PROGRAMINGLANGUAGE:{type:'NEED_PROGRAMINGLANGUAGE'}
        ,NEED_TOOL:{type:'NEED_TOOL'}
        ,NEED_PLATFORM:{type:'NEED_PLATFORM'}
        ,NEED_KNOWLEDGE:{type:'NEED_KNOWLEDGE'}
    }
    );"""

    Career.nodes.first_or_none().cypher(querycareer)
    Career.nodes.first_or_none().cypher(query)
    Course.nodes.first_or_none().cypher(querycourse)

def Career_Program(career):
    similar=career.cypher("CALL gds.nodeSimilarity.stream('careergraph') YIELD node1, node2, similarity  where gds.util.asNode(node1).creTitle='"+career.creTitle+"' and gds.util.asNode(node2).creTitle is  null  RETURN gds.util.asNode(node1).creTitle AS Career, gds.util.asNode(node2).proName AS Program, similarity")
    return similar[0]

def SimilarCourse(course):
    similar=course.cypher("CALL gds.nodeSimilarity.stream('coursegraph') YIELD node1, node2, similarity  where gds.util.asNode(node1).crsLink='"+course.crsLink+"'  RETURN gds.util.asNode(node1).crsLink AS Course1, gds.util.asNode(node2).crsLink AS Course2, similarity")
    return similar[0]
def Career_Course(career):
    similar=career.cypher("CALL gds.nodeSimilarity.stream('graph') YIELD node1, node2, similarity  where gds.util.asNode(node1).creTitle='"+career.creTitle+"' and gds.util.asNode(node2).creTitle is  null  RETURN gds.util.asNode(node1).creTitle AS Career, gds.util.asNode(node2).crsName as Course, similarity")
    return similar[0]
def Program_Skill():
    program=Program.nodes.all()
    for p in program:
        courses=p.course
        for i in courses:
            if(i.tool !=None):
                for j in i.tool:
                    p.tool.connect(j)
            if(i.knowledge !=None):
                for j in i.knowledge:
                    p.knowledge.connect(j)
            if(i.platform !=None):
                for j in i.platform:
                    p.platform.connect(j)
            if(i.framework !=None):
                for j in i.framework:
                    p.framework.connect(j)
            if(i.programinglanguage !=None):
                for j in i.programinglanguage:
                    p.programinglanguage.connect(j)

def ReCareerProgramWithFitler(career,list_skill):
    subcareer=Career(creTitle='subcareer').save()
    for i in career.tool:
        if(i.value not in list_skill):
            subcareer.tool.connect(i)
    for i in career.programinglanguage:
        if(i.value not in list_skill):
            subcareer.programinglanguage.connect(i)
    for i in career.knowledge:
        if(i.value not in list_skill):
            subcareer.knowledge.connect(i)
    for i in career.platform:
        if(i.value not in list_skill):
            subcareer.platform.connect(i)
    for i in career.framework:
        if(i.value not in list_skill):
            subcareer.framework.connect(i)
    subcareer.save()
    query="""CALL gds.graph.create('subgraph',['Career', 'Framework','ProgramingLanguage','Tool','Program','Knowledge'],
    {
        HAS_FRAMEWORK:{type:'HAS_FRAMEWORK'}
        ,HAS_PROGRAMINGLANGUAGE:{type:'HAS_PROGAMINGLANGUAGE'}
        ,HAS_TOOL:{type:'HAS_TOOL'}
        ,HAS_PLATFORM:{type:'HAS_PLATFORM'}
        ,HAS_KNOWLEDGE:{type:'HAS_KNOWLEDGE'}
        ,NEED_FRAMEWORK:{type:'NEED_FRAMEWORK'}
        ,NEED_PROGRAMINGLANGUAGE:{type:'NEED_PROGRAMINGLANGUAGE'}
        ,NEED_TOOL:{type:'NEED_TOOL'}
        ,NEED_PLATFORM:{type:'NEED_PLATFORM'}
        ,NEED_KNOWLEDGE:{type:'NEED_KNOWLEDGE'}
    }
);
"""
    subcareer.cypher(query)
    similar=subcareer.cypher("CALL gds.nodeSimilarity.stream('subgraph') YIELD node1, node2, similarity  where gds.util.asNode(node1).creTitle='"+subcareer.creTitle+"' and gds.util.asNode(node2).creTitle is  null  RETURN gds.util.asNode(node1).creTitle AS Career, gds.util.asNode(node2).proName AS Program, similarity")
    subcareer.cypher("CALL gds.graph.drop('subgraph')")
    subcareer.delete()
    return similar[0]


Create_Graph()