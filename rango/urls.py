from django.conf.urls import url
from rango import views

urlpatterns = [
    url(r'^about/$', views.about, name = 'about'),
    url(r'^$', views.index, name='index'),
    url(r'^category/(?P<category_name_url>[\w\-]+)/$', views.show_category, name ='show_category'), 
    url(r'^index/$', views.index, name = 'index'),
   ]