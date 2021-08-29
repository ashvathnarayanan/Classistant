from django import template
from .. import models
register = template.Library()


@register.filter(name='checkClash')
def checkClash(classlist, thisclass):
    for i in classlist:
        if thisclass.time == i.time and i != thisclass:
            return True
    return False


@register.filter(name='getClash')
def getClash(classlist, thisclass):
    for i in classlist:
        if thisclass.time == i.time and i != thisclass:
            return "Clashed with "+i.course.course_name+" on "+i.time
    return False


@register.filter(name='getSlots')
def getSlots(classlist):
    try:
        slots=classlist[0].slot
        for i in range(1,len(classlist)):slots+=","+classlist[i].slot
        return slots
    except Exception:
        return ""