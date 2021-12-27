from django.urls import path

from analysis.views import AnalysisView, KeyWordView

urlpatterns = [
    path('', AnalysisView.as_view(), name = 'analysis'),
    path('keyword/', KeyWordView.as_view(), name = 'keyword')
]