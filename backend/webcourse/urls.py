from django.urls import path
from . import views
urlpatterns = [
   path('search_course/', views.SearchCourse.as_view()),
   path('filter_course_by_skill/', views.FilterCourseBySkill.as_view()),
   path('get_career/', views.GetJobs.as_view()),
   path('get_skill_by_job/', views.GetSkillByJob.as_view()),
   path('get_skill/', views.GetSkill.as_view()),
   path('popular_course/', views.TopPopularCourse.as_view()),
   path('popular_course_web/', views.TopPopularCourseWeb.as_view()),
   path('popular_course_by_type/', views.TopPopularFromSkill.as_view()),
   path('similar_courses/', views.GetSimilarCourses.as_view()),
   path('get_career_has_program/', views.GetJobsHasProgram.as_view()),
   path("get_program/", views.GetProgram.as_view()),
   path("get_program_by_career/", views.GetProgramByCareer.as_view()),
   path("update_profile/", views.UpdateProfile.as_view()),
   path("user_information/", views.GetUserInformation.as_view()),
   path("enroll_course/", views.EnrollCourse.as_view()),
   path("complete_course/", views.CompleteCourse.as_view()),
   path("get_enroll_courses/", views.GetEnrollCourses.as_view()),
   path("get_complete_courses/", views.GetCompleteCourses.as_view()),
   path("unenroll_courses/", views.UnenrollCourse.as_view()),
   path("uncomplete_courses/", views.UnCompleteCourse.as_view()),
   path("get_free_course/", views.GetTopFreeCourse.as_view()),
   path("get_free_course_web/", views.GetTopFreeCourseOfWeb.as_view()),
   path("get_username/", views.GetUserName.as_view()),
   path("get_all_web/", views.GetAllWeb.as_view()),
   path("get_course_from_career/", views.GetCourseFromCareer.as_view()),
   path("specific_course/", views.SpecificCourse.as_view())
]