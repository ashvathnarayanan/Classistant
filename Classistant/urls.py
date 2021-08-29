from django.contrib import admin
from django.urls import path
from app import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    # Key API Endpoints
    path('student', csrf_exempt(views.createStudent)),
    path('student/<studentId>', csrf_exempt(views.getStudent)),
    path('classes/<courseCode>', csrf_exempt(views.getClasses)),
    path('class/<studentId>', csrf_exempt(views.addStudent)),
    path('class/<studentId>/<classId>', csrf_exempt(views.deleteClass)),
    path('class/<studentId>', csrf_exempt(views.getStudentClasses)),
    path('classes-on-map/<courseCode>', csrf_exempt(views.getLocationInfo)),
    # Key Http Endpoints
    path("register", views.registerPage, name="register"),
    path("map", views.mapPage, name="map"),
    path("courses", views.coursePage, name="courses"),
    path("timetable", views.timetablePage, name="timetable"),
    # other urls and APIs
    path('', views.rootPage),
    path('home', views.landPage, name="land"),
    path('login', views.loginPage, name="login"),
    path('logout', views.logout, name="logout"),
    path('admin/', admin.site.urls),
    path('course', views.getCourse, name="course"),
    path('suggestions', csrf_exempt(views.getSuggestion), name="suggestions"),
]
