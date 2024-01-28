
# urls.py
from django.urls import path
from . import views 

urlpatterns = [
    path('submit_response/', views.submit_response, name='submit_response'),
    path('submit_questionnaire_section/', views.submit_questionnaire_section, name='submit_questionnaire_section'),
    path('tag-article/', views.submit_tagged_profiles, name='tag-article'),
]
