from django.views import View
from online_app.models import *
from django.urls import resolve
from django.http import HttpResponseRedirect,HttpRequest
from django.shortcuts import render, get_object_or_404, redirect
import requests

class SearchBarView(View):
    def get(self, request, *args, **kwargs):

        if kwargs:
            try:
                search_query = request.session['search_query']
                url = 'https://api.github.com/search/repositories?q=' + search_query
                results = requests.get(url).json()['items']

                for repo in results:
                    if Repo.objects.filter(name = repo['name']).exists():
                        repo['imported']=True
                    else:
                        repo['imported']=False

                return render(request,template_name='results.html',context = {'results':results})
            except:
                return render(request,template_name='searchbar.html')
        return render(request,template_name='searchbar.html')

    def post(self,request,*args,**kwargs):
        search_query = None

        if search_query in request.session:
            search_query = "+".join(list(request.session['search_query']))
        else:
            search_query = "+".join(list(request.POST['term'].split(" ")))
            request.session['search_query'] = search_query

        url = 'https://api.github.com/search/repositories?q='+search_query
        results = requests.get(url).json()['items']
        for repo in results:
            if Repo.objects.filter(name=repo['name']).exists():
                repo['imported'] = True
            else:
                repo['imported'] = False

        return render(request,template_name='results.html',context={'results':results})

