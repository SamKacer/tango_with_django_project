# encoding: utf-8
import os
os.environ.setdefault('django_settings_module', 'tango_with_django_project.settings')

import django
django.setup()
from rango.models import Category, Page

def populate():
    # first create lists of dictionaries containing pages 
    python_pages = [
        { "title" : "Official Python Tutorial",
        "url" : "http://docs.python.org/2/tutorial/",
        "views" : 123},
        {"title":"How to Think like a Computer Scientist",
        "url":"http://www.greenteapress.com/thinkpython/",
        "views" : 321},
        {"title":"Learn Python in 10 Minutes",
        "url":"http://www.korokithakis.net/tutorials/python/",  
        "views" : 35} ]
    
    django_pages = [
        {"title":"Official Django Tutorial",        "url":"https://docs.djangoproject.com/en/1.9/intro/tutorial01/",
        "views" : 55},        
        {"title":"Django Rocks",
        "url":"http://www.djangorocks.com/",
        "views" : 23},
                {"title":"How to Tango with Django",        "url":"http://www.tangowithdjango.com/",
        "views" : 23} ]
    
    other_pages = [
        {"title":"Bottle",        "url":"http://bottlepy.org/docs/dev/",
        "views" : 3},
        {"title":"Flask",
        "url":"http://flask.pocoo.org",
        "views" : 23} ]
        
    cats= { 
    "Python" :{
            "pages" : python_pages,
            "views" : 128,
            "likes" : 64},
        "Django" : {
            "pages" : django_pages,
            "views" : 64,
            "likes" : 32},
        "Other Frameworks" : {
            "pages" : other_pages,
            "views" : 32,
            "likes" : 16}
     }
    
    for cat, cat_data in cats.items():
        c = add_cat(cat, views = cat_data["views"], likes = cat_data["likes"])
        for p in cat_data["pages"]:
            add_page(c, p["title"], p["url"], p["views"])
    
    # print out categories that were added
    for c in Category.objects.all():
        for p in Page.objects.filter(category = c):
            print("- {0} - {1}".format(str(c), str(p)))

# method for adding page 
def add_page(cat, title, url, views = 0):
    p = Page.objects.get_or_create(category = cat, title = title)[0]
    p.url = url
    p.views = views
    p.save()
    return p

def add_cat(name, views = 0, likes = 0):
    c = Category.objects.get_or_create(name = name)[0]
    c.views = views
    c.likes = likes
    c.save()
    return c

# start execution here!
if __name__ == '__main__':
    print("starting Rango population script")
    populate()
    