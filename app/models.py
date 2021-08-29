from django.db import models


class Course(models.Model):
    course_id = models.CharField(
        primary_key=True, null=False, unique=True, max_length=10)
    course_name = models.CharField(null=False, blank=False, max_length=50)


class Building(models.Model):
    building_name = models.CharField(
        primary_key=True, null=False, unique=True, max_length=10)
    latitude = models.FloatField()
    longitude = models.FloatField()


class Class(models.Model):
    class_id = models.PositiveIntegerField(
        primary_key=True, null=False, unique=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    faculty_name = models.CharField(null=False, blank=False, max_length=50)
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    time = models.CharField(null=False, blank=False, max_length=30)
    total_students = models.PositiveIntegerField(
        null=False, blank=False, default=0)
    slot = models.CharField(null=False, blank=False, max_length=5)


class Student(models.Model):
    rollNo = models.CharField(null=False, blank=False, max_length=10)
    name = models.CharField(null=False, blank=False, max_length=50)
    classes = models.ManyToManyField(Class, related_name="students")
