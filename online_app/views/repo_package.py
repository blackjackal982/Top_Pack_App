from django.views import View,generic

from django.urls import resolve,reverse_lazy
from django.http import HttpResponseRedirect,HttpRequest
from django.shortcuts import render, get_object_or_404, redirect
import requests
import json
from base64 import b64decode
from django.utils.safestring import mark_safe
from online_app.models import *

class GetPackageView(View):
    def get(self,request,*args,**kwargs):
        owner = kwargs['owner']
        reponame =kwargs['repo_name']
        url = "https://api.github.com/repos/"+owner+"/"+reponame+"/contents/package.json"
        response = requests.get(url)

        result = None
        if response.status_code == 200:
            result = response.json()
            result['decoded_content'] = json.loads(b64decode(result['content']).decode('utf-8'))

            try:
                if 'dependencies' in result['decoded_content']:
                    for dependency in result['decoded_content']['dependencies']:

                        package,created = Package.objects.get_or_create(
                        name=dependency,
                        defaults={'count':0},
                        )
                        if created == True:
                            package.save()

                        reponame, repo_created = Repo.objects.get_or_create(dep= package,
                                                                       owner= kwargs['owner'],
                                                                       name= kwargs['repo_name'],
                                                                       defaults={
                                                                                 'stars': kwargs['stars'],
                                                                                 })
                        if repo_created == True:
                            package.count+=1
                            package.save()

                    result['dependencies'] = result['decoded_content']['dependencies']
            except Exception as e:
                print(e)
                pass

            try:
                if 'devDependencies' in result['decoded_content']:
                    for dependency in result['decoded_content']['devDependencies']:
                        package,created = Package.objects.get_or_create(
                            name=dependency,
                            defaults={'count': 0},
                        )
                        if created == True:
                            package.save()

                        reponame,repo_created = Repo.objects.get_or_create(dep= package,
                                                                       owner= kwargs['owner'],
                                                                       name= kwargs['repo_name'],
                                                                       defaults={
                                                                                 'stars': kwargs['stars'],
                                                                       })
                        if repo_created == True and True == repo_created:
                            package.count +=1
                            package.save()

                    result['devDependencies'] = result['decoded_content']['devDependencies']
            except Exception as e:
                print(e,package)
                pass


        return render(request,template_name='import.html',
                      context={'result':result
                               })
    def post(self,request,args,kwargs):
        pass

class GetTopPackageView(View):
    def get(self,request,*args,**kwargs):
        top_packages = Package.objects.all().order_by('-count')[0:10]
        search_packages = [i.name for i in top_packages]
        return render(request,template_name='packages.html',
                      context={'package':top_packages,
                               'search':mark_safe(search_packages)
                               })


class GetTopRepoView(View):
    def get(self,request,*args,**kwargs):
        top_repos = Repo.objects.filter(dep_id=kwargs['pk']).all()
        top_repos = [(repo.name,repo.stars) for repo in top_repos]
        top_repos.sort(key = lambda x:x[0])
        top_repos.sort(key = lambda x:x[1],reverse=True)
        return render(request,template_name='top_repos.html',
                      context={'repositories':top_repos[0:3]
                               }
                      )
