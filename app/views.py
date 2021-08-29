from django.http.response import Http404, HttpResponse, HttpResponseBase, HttpResponseForbidden, JsonResponse
from django.shortcuts import redirect, render
from app.models import *
import json
import requests


def rootPage(request):
    if 'user' in request.session:
        return redirect('land')
    else:
        return redirect("register")


def registerPage(request):
    if request.method == "POST":
        url = "http://127.0.0.1:8000/student"
        student = {"name": request.POST["name"],
                   "rollNo": request.POST["rollno"]}
        response = requests.request("POST", url, headers={
                                    'Content-Type': 'application/json'}, data=json.dumps(student))
        if response.text == "success":
            request.session['user'] = request.POST["rollno"]
            return redirect("land")
        return render(request, "register.html", {})
    return render(request, "register.html", {})


def loginPage(request):
    if request.method == "POST":
        url = "http://127.0.0.1:8000/student/"+request.POST["rollno"]
        response = requests.request("GET", url, headers={'Content-Type': 'application/json'})
        print(response.text)
        if response.text != "failed":
            request.session['user'] = request.POST["rollno"]
            return redirect("land")
        return render(request, "login.html", {})
    return render(request, "login.html", {})


def landPage(request):
    student = Student.objects.get(rollNo=request.session.get('user'))
    return render(request, "land.html", {"student":student})


def mapPage(request):
    return render(request, "map.html", {})


def coursePage(request):
    classes = Class.objects.all()
    student = Student.objects.get(rollNo=request.session.get('user'))
    return render(request, "course.html", {'classes': classes, "student": student})


def timetablePage(request):
    student = Student.objects.get(rollNo=request.session.get('user'))
    return render(request, "timetable.html", {"student": student})


def getCourse(request):
    student = Student.objects.get(rollNo=request.session.get('user'))
    if request.POST["course"] != "" and request.POST["faculty"] != "":
        course = Course.objects.get(course_id=request.POST["course"])
        classes = Class.objects.filter(course=course, faculty_name=request.POST["faculty"])
        return render(request, "course.html", {'classes': classes, "student": student})
    elif request.POST["faculty"] != "":
        classes = Class.objects.filter(faculty_name=request.POST["faculty"])
        return render(request, "course.html", {'classes': classes, "student": student})
    elif request.POST["course"] != "":
        course = Course.objects.get(course_id=request.POST["course"])
        classes = Class.objects.filter(course=course)
        return render(request, "course.html", {'classes': classes, "student": student})



def getSuggestion(request):
    courses = Course.objects.all()
    classes = Class.objects.all()
    clist = [i.course_id for i in courses]
    flist = list(set([i.faculty_name for i in classes]))
    return JsonResponse({"clist": clist, "flist": flist})


def addStudent(request, studentId):
    student = Student.objects.get(rollNo=studentId)
    newClass = Class.objects.get(class_id=request.POST["classId"])
    student.classes.add(newClass)
    student.save()
    newClass.total_students+=1
    newClass.save()
    return HttpResponse("success")


def deleteClass(request, studentId, classId):
    print(studentId)
    student = Student.objects.get(rollNo=studentId)
    delClass = Class.objects.get(class_id=classId)
    student.classes.remove(delClass)
    student.save()
    delClass.total_students-=1
    delClass.save()
    return HttpResponse("success")



def createStudent(request):
    if request.method == "POST":
        try:
            my_json = request.body.decode('utf8').replace("'", '"')
            student_data = json.loads(my_json)
            new_student = Student(
                rollNo=student_data["rollNo"], name=student_data["name"])
            new_student.save()
            return HttpResponse("success")
        except Exception as e:
            return HttpResponse(e)


def getStudent(request, studentId):
    try:
        student = Student.objects.get(rollNo=studentId)
        return JsonResponse({"student": student.rollNo})
    except Exception as e:
        return HttpResponse("failed")


def getClasses(request, courseCode):
    try:
        course = Course.objects.get(course_id=courseCode)
        classes = Class.objects.filter(course=course).values()
        return JsonResponse({"classes": classes})
    except Exception as e:
        return HttpResponse(e)


def getStudentClasses(request, studentId):
    try:
        student = Student.objects.get(rollNo=studentId).values()
        return JsonResponse({"classes": student["classes"]})
    except Exception as e:
        return HttpResponse(e)


def getLocationInfo(request, courseCode):
    try:
        course = Course.objects.get(course_id=courseCode)
        classes = Class.objects.filter(course=course)
        data = [{"name": i.course.course_name,
                "building_name": i.building.building_name, "students": i.total_students, "lat": i.building.latitude, "lng": i.building.longitude} for i in classes]
        return JsonResponse({"data": data})
    except Exception as e:
        return HttpResponse("failed")


def logout(request):
    del request.session['user']
    return redirect('login')
