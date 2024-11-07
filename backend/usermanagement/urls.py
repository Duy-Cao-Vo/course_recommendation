from django.urls import path
from . import views
urlpatterns = [
   path('register/', views.Register.as_view()),
   path('register_data_admin/', views.RegisterDataAdmin.as_view()),
   path('register_account_admin/', views.RegisterAccountAdmin.as_view()),
]