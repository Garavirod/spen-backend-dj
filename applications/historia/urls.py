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
]