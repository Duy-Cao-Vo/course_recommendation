from neo4j.api import READ_ACCESS
from neomodel import RelationshipManager
from numpy import datetime64, mod
from django.core.files import File
from neomodel.properties import DateTimeProperty, FloatProperty, IntegerProperty,DateTimeProperty
import pandas as pd
from neomodel import config
import ast


config.DATABASE_URL ='bolt://neo4j:Caoduy123@localhost:7687'
from neomodel import db
# Create your models here.
import webcourse.models as models
db.set_connection('bolt://neo4j:Caoduy123@localhost:7687')

def importCareer(filename):
    data = pd.read_csv(filename,encoding='latin-1')
    for i in data.index:
        career=models.Career(creTitle=str(data[i:i+1]['Career'].values[0])).save()
        if(str(data[i:i+1]['Knowledge'].values[0])!='nan'):
            know=data[i:i+1]['Knowledge'].values[0].split(',')
            for j in know:
                t=j.strip(' ')
                if(models.Knowledge.nodes.first_or_none(value=t) is None):
                    models.Knowledge(value=t).save()
                career.knowledge.connect(models.Knowledge.nodes.first_or_none(value=t))
        if(str(data[i:i+1]['Tool'].values[0])!='nan'):
            tool=data[i:i+1]['Tool'].values[0].split(',')
            for j in tool:
                t=j.strip(' ')
                if(models.Tool.nodes.first_or_none(value=t) is None):
                    models.Tool(value=t).save()
                career.tool.connect(models.Tool.nodes.first_or_none(value=t))
        if(str(data[i:i+1]['Programing Language'].values[0])!='nan'):
            lang=data[i:i+1]['Programing Language'].values[0].split(',')
            for j in lang:
                t=j.strip(' ')
                if(models.ProgramingLanguage.nodes.first_or_none(value=t) is None):
                    models.ProgramingLanguage(value=t).save()
                career.programinglanguage.connect(models.ProgramingLanguage.nodes.first_or_none(value=t))
        if(str(data[i:i+1]['Platform'].values[0])!='nan'):
            platform=data[i:i+1]['Platform'].values[0].split(',')
            for j in platform:
                t=j.strip(' ')
                if(models.Platform.nodes.first_or_none(value=t) is None):
                    models.Platform(value=t).save()
                career.platform.connect(models.Platform.nodes.first_or_none(value=t))
        if(str(data[i:i+1]['Framework'].values[0])!='nan'):
            framework=data[i:i+1]['Framework'].values[0].split(',')
            for j in framework:
                t=j.strip(' ')
                if(models.Framework.nodes.first_or_none(value=t) is None):
                    models.Framework(value=t).save()
                career.framework.connect(models.Framework.nodes.first_or_none(value=t))

def importCourse(filename, minscore, time):
    data = pd.read_csv(filename,encoding='latin-1')
    for i in data.index:
        print("DEBUG import data index", i)
        name=str(data[i:i+1]['name'].values[0])
        link=str(data[i:i+1]['link'].values[0])
        fee=str(data[i:i+1]['fee'].values[0]).replace("$","")
        if(models.Course.nodes.first_or_none(crsLink=link) is None):
            website=link.replace("https://","").replace("http://","").split('/')[0]
            if('free' in fee.lower() or fee.find("Enroll")!=-1 ):
                fee="0"
            fee=float(fee)
            time=str(data[i:i+1]['time'].values[0])
            course=models.Course(crsName=name,crsLink=link,crsTime=time,crsFee=fee).save()
            course=models.Course(crsName=name,crsLink=link,crsTime=time,crsFee=fee,crsCreateDate=time,crsUpdateDate=time).save()
            if(models.Website.nodes.first_or_none(webName=website) is None):
                models.Website(webName=website).save()
            course.website.connect(models.Website.nodes.first_or_none(webName=website))
            if(str(data[i:i+1]['rating'].values[0])!='nan'):
                course.crsRating=float(str(data[i:i+1]['rating'].values[0]))
                course.save()
            if(str(data[i:i+1]['enroll'].values[0])!='nan'):
                course.crsEnroll=int(str(data[i:i+1]['enroll'].values[0]).replace(".0","").replace(".","").replace(",",""))
                course.save()
        
            if(str(data[i:i+1]['instructor'].values[0])!='nan'):
                ins=data[i:i+1]['instructor'].values[0].split(',')
                for j in ins:
                    t=j.strip(' ')
                    if(models.Instructor.nodes.first_or_none(insName=str(data[i:i+1]['instructor'].values[0])) is None):
                        models.Instructor(insName=str(data[i:i+1]['instructor'].values[0])).save()
                    course.instructor.connect(models.Instructor.nodes.first_or_none(insName=str(data[i:i+1]['instructor'].values[0])))
            if(str(data[i:i+1]['levelrequirement'].values[0])!='nan'):
                if(models.Level.nodes.first_or_none(levName=str(data[i:i+1]['levelrequirement'].values[0])) is None):
                    models.Level(levName=str(data[i:i+1]['levelrequirement'].values[0])).save()
                course.level.connect(models.Level.nodes.first_or_none(levName=str(data[i:i+1]['levelrequirement'].values[0])))
            if(str(data[i:i+1]['knowledge'].values[0])!='nan'):
                know=ast.literal_eval(data[i:i+1]['knowledge'].values[0])
                for j in know:
                    skill_name, score = j.split(' %% ')
                    if float(score) < minscore:
                        continue
                    if(models.Knowledge.nodes.first_or_none(value=skill_name) is None):
                        models.Knowledge(value=skill_name).save()
                    course.knowledge.connect(models.Knowledge.nodes.first_or_none(value=skill_name))
            if(str(data[i:i+1]['tool'].values[0])!='nan'):
                tool=ast.literal_eval(data[i:i+1]['tool'].values[0])
                for j in tool:
                    skill_name, score = j.split(' %% ')
                    if float(score) < minscore:
                        continue
                    if(models.Tool.nodes.first_or_none(value=skill_name) is None):
                        models.Tool(value=skill_name).save()
                    course.tool.connect(models.Tool.nodes.first_or_none(value=skill_name))
            if(str(data[i:i+1]['language'].values[0])!='nan'):
                lang=ast.literal_eval(data[i:i+1]['language'].values[0])
                for j in lang:
                    skill_name, score = j.split(' %% ')
                    if float(score) < minscore:
                        continue
                    if(models.ProgramingLanguage.nodes.first_or_none(value=skill_name) is None):
                        models.ProgramingLanguage(value=skill_name).save()
                    course.programinglanguage.connect(models.ProgramingLanguage.nodes.first_or_none(value=skill_name))
            if(str(data[i:i+1]['platform'].values[0])!='nan'):
                platform=ast.literal_eval(data[i:i+1]['platform'].values[0])
                for j in platform:
                    skill_name, score = j.split(' %% ')
                    if float(score) < minscore:
                        continue
                    if(models.Platform.nodes.first_or_none(value=skill_name) is None):
                        models.Platform(value=skill_name).save()
                    course.platform.connect(models.Platform.nodes.first_or_none(value=skill_name))
            if(str(data[i:i+1]['framework'].values[0])!='nan'):
                framework=ast.literal_eval(data[i:i+1]['framework'].values[0])
                for j in framework:
                    skill_name, score = j.split(' %% ')
                    if float(score) < minscore:
                        continue
                    if(models.Framework.nodes.first_or_none(value=skill_name) is None):
                        models.Framework(value=skill_name).save()
                    course.framework.connect(models.Framework.nodes.first_or_none(value=skill_name))
            if(str(data[i:i+1]['program'].values[0])!='nan'):
                program=data[i:i+1]['program'].values[0].split(',')
                for j in program:
                    t=j.strip(' ')
                    if(models.Program.nodes.first_or_none(proName=t) is None):
                        models.Program(proName=t).save()
                    course.program.connect(models.Program.nodes.first_or_none(proName=t))
            if(str(data[i:i+1]['Subtitle'].values[0])!='nan'):
                subtitle=data[i:i+1]['Subtitle'].values[0].split(',')
                for j in subtitle:
                    t=j.strip(' ')
                    if(models.SubTitle.nodes.first_or_none(subLanguage=t) is None):
                        models.SubTitle(subLanguage=t).save()
                    course.subtitle.connect(models.SubTitle.nodes.first_or_none(subLanguage=t))
            if(str(data[i:i+1]['Subject'].values[0])!='nan'):
                if(models.Subject.nodes.first_or_none(Name=str(data[i:i+1]['Subject'].values[0])) is None):
                    models.Subject(Name=str(data[i:i+1]['Subject'].values[0])).save()
                course.subject.connect(models.Subject.nodes.first_or_none(Name=str(data[i:i+1]['Subject'].values[0])))
            if(str(data[i:i+1]['organization'].values[0])!='nan'):
                organization=data[i:i+1]['organization'].values[0].split(',')
                for j in organization:
                    t=j.strip(' ')
                    if(models.Organization.nodes.first_or_none(orgName=t) is None):
                        models.Organization(orgName=t).save()
                    course.organization.connect(models.Organization.nodes.first_or_none(orgName=t))
        else:
            course=models.Course.nodes.first_or_none(crsLink=link)
            if(str(data[i:i+1]['enroll'].values[0])!='nan'):
                course.crsEnroll=int(str(data[i:i+1]['enroll'].values[0]).replace(".0","").replace(".","").replace(",",""))
                course.save()
            if(str(data[i:i+1]['knowledge'].values[0])!='nan'):
                know=ast.literal_eval(data[i:i+1]['knowledge'].values[0])
                for j in know:
                    skill_name, score = j.split(' %% ')
                    if float(score) < minscore:
                        continue
                    if(models.Knowledge.nodes.first_or_none(value=skill_name) is None):
                        models.Knowledge(value=skill_name).save()
                    if(models.Knowledge.nodes.first_or_none(value=skill_name) not in course.knowledge):
                        course.knowledge.connect(models.Knowledge.nodes.first_or_none(value=skill_name))
            if(str(data[i:i+1]['tool'].values[0])!='nan'):
                tool=ast.literal_eval(data[i:i+1]['tool'].values[0])
                for j in tool:
                    skill_name, score = j.split(' %% ')
                    if float(score) < minscore:
                        continue
                    if(models.Tool.nodes.first_or_none(value=skill_name) is None):
                        models.Tool(value=skill_name).save()
                    if(models.Tool.nodes.first_or_none(value=skill_name) not in course.tool):
                        course.tool.connect(models.Tool.nodes.first_or_none(value=skill_name))
            if(str(data[i:i+1]['language'].values[0])!='nan'):
                lang=ast.literal_eval(data[i:i+1]['language'].values[0])
                for j in lang:
                    skill_name, score = j.split(' %% ')
                    if float(score) < minscore:
                        continue
                    if(models.ProgramingLanguage.nodes.first_or_none(value=skill_name) is None):
                        models.ProgramingLanguage(value=skill_name).save()
                    if(models.ProgramingLanguage.nodes.first_or_none(value=skill_name) not in course.programinglanguage):
                        course.programinglanguage.connect(models.ProgramingLanguage.nodes.first_or_none(value=skill_name))
            if(str(data[i:i+1]['platform'].values[0])!='nan'):
                platform=ast.literal_eval(data[i:i+1]['platform'].values[0])
                for j in platform:
                    skill_name, score = j.split(' %% ')
                    if float(score) < minscore:
                        continue
                    if(models.Platform.nodes.first_or_none(value=skill_name) is None):
                        models.Platform(value=skill_name).save()
                    if(models.Platform.nodes.first_or_none(value=skill_name) not in course.platform):
                        course.platform.connect(models.Platform.nodes.first_or_none(value=skill_name))
            if(str(data[i:i+1]['framework'].values[0])!='nan'):
                framework=ast.literal_eval(data[i:i+1]['framework'].values[0])
                for j in framework:
                    skill_name, score = j.split(' %% ')
                    if float(score) < minscore:
                        continue
                    if(models.Framework.nodes.first_or_none(value=skill_name) is None):
                        models.Framework(value=skill_name).save()
                    if(models.Framework.nodes.first_or_none(value=skill_name) not in course.framework):
                        course.framework.connect(models.Framework.nodes.first_or_none(value=skill_name))

def importCourse_Skill(filename, skills):
    data = pd.read_csv(filename,encoding='latin-1')
    for i in data.index:
        name=str(data[i:i+1]['name'].values[0])
        link=str(data[i:i+1]['link'].values[0])
        fee=str(data[i:i+1]['fee'].values[0]).replace("$","")
        if(models.Course.nodes.first_or_none(crsLink=link) is None):
            website=link.replace("https://","").replace("http://","").split('/')[0]
            if('free' in fee.lower() or fee.find("Enroll")!=-1 ):
                fee="0"
            fee=float(fee)
            time=str(data[i:i+1]['time'].values[0])
            course=models.Course(crsName=name,crsLink=link,crsTime=time,crsFee=fee).save()
            if(models.Website.nodes.first_or_none(webName=website) is None):
                models.Website(webName=website).save()
            course.website.connect(models.Website.nodes.first_or_none(webName=website))
            if(str(data[i:i+1]['rating'].values[0])!='nan'):
                course.crsRating=float(str(data[i:i+1]['rating'].values[0]))
                course.save()
            if(str(data[i:i+1]['enroll'].values[0])!='nan'):
                course.crsEnroll=int(str(data[i:i+1]['enroll'].values[0]).replace(".0","").replace(".","").replace(",",""))
                course.save()
        
            if(str(data[i:i+1]['instructor'].values[0])!='nan'):
                ins=data[i:i+1]['instructor'].values[0].split(',')
                for j in ins:
                    t=j.strip(' ')
                    if(models.Instructor.nodes.first_or_none(insName=str(data[i:i+1]['instructor'].values[0])) is None):
                        models.Instructor(insName=str(data[i:i+1]['instructor'].values[0])).save()
                    course.instructor.connect(models.Instructor.nodes.first_or_none(insName=str(data[i:i+1]['instructor'].values[0])))
            if(str(data[i:i+1]['levelrequirement'].values[0])!='nan'):
                if(models.Level.nodes.first_or_none(levName=str(data[i:i+1]['levelrequirement'].values[0])) is None):
                    models.Level(levName=str(data[i:i+1]['levelrequirement'].values[0])).save()
                course.level.connect(models.Level.nodes.first_or_none(levName=str(data[i:i+1]['levelrequirement'].values[0])))
            for n in skills:
                if n["link"]==link and n["type"]=="Knowledge":
                    if(models.Knowledge.nodes.first_or_none(value=n["skill_name"]) is None):
                        models.Knowledge(value=n["skill_name"]).save()
                    course.knowledge.connect(models.Knowledge.nodes.first_or_none(value=n["skill_name"]))
                if n["link"]==link and n["type"]=="Tool":
                    if(models.Tool.nodes.first_or_none(value=n["skill_name"]) is None):
                        models.Tool(value=n["skill_name"]).save()
                    course.Tool.connect(models.Tool.nodes.first_or_none(value=n["skill_name"]))
                if n["link"]==link and n["type"]=="Programing Language":
                    if(models.ProgramingLanguage.nodes.first_or_none(value=n["skill_name"]) is None):
                        models.ProgramingLanguage(value=n["skill_name"]).save()
                    course.programinglanguage.connect(models.ProgramingLanguage.nodes.first_or_none(value=n["skill_name"]))
                if n["link"]==link and n["type"]=="Platform":
                    if(models.Platform.nodes.first_or_none(value=n["skill_name"]) is None):
                        models.Platform(value=n["skill_name"]).save()
                    course.platform.connect(models.Platform.nodes.first_or_none(value=n["skill_name"]))
                if n["link"]==link and n["type"]=="Framework":
                    if(models.Framework.nodes.first_or_none(value=n["skill_name"]) is None):
                        models.Framework(value=n["skill_name"]).save()
                    course.framework.connect(models.Framework.nodes.first_or_none(value=n["skill_name"]))
            if(str(data[i:i+1]['program'].values[0])!='nan'):
                program=data[i:i+1]['program'].values[0].split(',')
                for j in program:
                    t=j.strip(' ')
                    if(models.Program.nodes.first_or_none(proName=t) is None):
                        models.Program(proName=t).save()
                    course.program.connect(models.Program.nodes.first_or_none(proName=t))
            if(str(data[i:i+1]['Subtitle'].values[0])!='nan'):
                subtitle=data[i:i+1]['Subtitle'].values[0].split(',')
                for j in subtitle:
                    t=j.strip(' ')
                    if(models.SubTitle.nodes.first_or_none(subLanguage=t) is None):
                        models.SubTitle(subLanguage=t).save()
                    course.subtitle.connect(models.SubTitle.nodes.first_or_none(subLanguage=t))
            if(str(data[i:i+1]['Subject'].values[0])!='nan'):
                if(models.Subject.nodes.first_or_none(Name=str(data[i:i+1]['Subject'].values[0])) is None):
                    models.Subject(Name=str(data[i:i+1]['Subject'].values[0])).save()
                course.subject.connect(models.Subject.nodes.first_or_none(Name=str(data[i:i+1]['Subject'].values[0])))
            if(str(data[i:i+1]['organization'].values[0])!='nan'):
                organization=data[i:i+1]['organization'].values[0].split(',')
                for j in organization:
                    t=j.strip(' ')
                    if(models.Organization.nodes.first_or_none(orgName=t) is None):
                        models.Organization(orgName=t).save()
                    course.organization.connect(models.Organization.nodes.first_or_none(orgName=t))
        else:
            course=models.Course.nodes.first_or_none(crsLink=link)
            if(str(data[i:i+1]['enroll'].values[0])!='nan'):
                course.crsEnroll=int(str(data[i:i+1]['enroll'].values[0]).replace(".0","").replace(".","").replace(",",""))
                course.save()
            for n in skills:
                if n["link"]==link and n["type"]=="Knowledge":
                    if(models.Knowledge.nodes.first_or_none(value=n["skill_name"]) is None):
                        models.Knowledge(value=n["skill_name"]).save()
                    course.knowledge.connect(models.Knowledge.nodes.first_or_none(value=n["skill_name"]))
                if n["link"]==link and n["type"]=="Tool":
                    if(models.Tool.nodes.first_or_none(value=n["skill_name"]) is None):
                        models.Tool(value=n["skill_name"]).save()
                    course.Tool.connect(models.Tool.nodes.first_or_none(value=n["skill_name"]))
                if n["link"]==link and n["type"]=="Programing Language":
                    if(models.ProgramingLanguage.nodes.first_or_none(value=n["skill_name"]) is None):
                        models.ProgramingLanguage(value=n["skill_name"]).save()
                    course.programinglanguage.connect(models.ProgramingLanguage.nodes.first_or_none(value=n["skill_name"]))
                if n["link"]==link and n["type"]=="Platform":
                    if(models.Platform.nodes.first_or_none(value=n["skill_name"]) is None):
                        models.Platform(value=n["skill_name"]).save()
                    course.platform.connect(models.Platform.nodes.first_or_none(value=n["skill_name"]))
                if n["link"]==link and n["type"]=="Framework":
                    if(models.Framework.nodes.first_or_none(value=n["skill_name"]) is None):
                        models.Framework(value=n["skill_name"]).save()
                    course.framework.connect(models.Framework.nodes.first_or_none(value=n["skill_name"]))
            


