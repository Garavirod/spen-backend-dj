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
    path(
        'values/',
        views.AddValoracionView.as_view(),
        name = 'new-value'
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
    ),
    path(
        'reading/<pk>/',
        views.ReadingModeStoryAPIView.as_view(),
        name = 'reading' 
    ),
    path(
        'story-comments/<storyPk>/',
        views.StoryCommentsView.as_view(),
        name = 'story-comments' 
    ),
    path(
        'is-valued/',
        views.AlreadyValuedView.as_view(),
        name = 'is-valued' 
    ),
    # PUT
    path(
        'writting/<pk>/',
        views.WrittingModeStoryView.as_view(),
        name = 'writting' 
    ),
]