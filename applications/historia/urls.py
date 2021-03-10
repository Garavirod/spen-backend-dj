# Django
from django.urls import path
# Views
from . import views
app_name = 'historias_app'

urlpatterns = [
    # POST
    path(
        'new-story/',
        views.RegisterNewStoryAPIView.as_view(),
        name = 'new-story'
    ),
    # GET
    path(
        'all-stoires/',
        views.AllPublishedStoriesAPIView.as_view(),
        name = 'all-stories'
    ),    
    path(
        'stories-by-autor/<pk>/',
        views.AuthorStoriesAPIView.as_view(),
        name = 'stories-by--autor' 
    ),
    path(
        'my-stories/<pk>/',
        views.MyStoriesAPIView.as_view(),
        name = 'my-stories' 
    )
]