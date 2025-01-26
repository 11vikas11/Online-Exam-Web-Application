from django.urls import path
from .import views

urlpatterns=[
    path('signup/',views.signup),
    path('login/',views.login),
    path('nextQuestion/',views.nextQuestion),
    path('previousQuestion/',views.previousQuestion),
    path('endExam/',views.endExam),
    path('startTest/',views.startTest)

]