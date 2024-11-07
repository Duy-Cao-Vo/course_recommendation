from django.urls import path
from . import views
urlpatterns = [
   path('crawl/', views.Crawl.as_view()),
   path("crawl_train/", views.CrawlTrain),
   path("crawl_train_import/", views.CrawlTrainImport),
   path("get_result_train/", views.GetResultTrain),
   path("get_sumarydb/", views.GetSumaryDB),
   path("insert_course_skill/", views.InsertSkillObject),
   path("get_data_export/", views.GetDataForExport),
   path("get_data_course/", views.getAllCourse.as_view()),
   path("get_data_career/", views.getAllCareer.as_view()),
]