from django.views import View,generic

from django.urls import resolve,reverse_lazy
from django.http import HttpResponseRedirect,HttpRequest
from django.utils.safestring import mark_safe
from django.shortcuts import render, get_object_or_404, redirect
from online_app.models import *

class GetBarChartView(View):
    def get(self,request,*args,**kwargs):
        repos = Repo.objects.values('owner','name','stars').distinct().order_by('-stars')[0:10]
        repo_name = []
        for repo in repos:
            new_dict = {}
            new_dict['x']=repo['owner']+'/'+repo['name']
            new_dict['y']=repo['stars']
            repo_name.append(new_dict)
        return render(request,template_name='barchart.html',
                      context={'repo_names':mark_safe(repo_name)
                               })