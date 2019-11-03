from django.urls import include, path
from online_app.views import *

urlpatterns = [
    path(r'searchbar/',SearchBarView.as_view(),name='searchbar'),
    path(r'searchbar/<str:reload>',SearchBarView.as_view(),name='home'),
    path(r'import/<str:owner>/<str:repo_name>/<str:stars>',GetPackageView.as_view(),name='import_repo'),
    path(r'toppacks/',GetTopPackageView.as_view(),name='top_packs'),
    path(r'toprepos/<int:pk>',GetTopRepoView.as_view(),name='top_repos'),
    path(r'barchart/',GetBarChartView.as_view(),name='barchart'),
]