# Django
from django.urls import path
# Views
from . import views
app_name = 'historias_app'

urlpatterns = [
    path(
        'new-story/',
        views.RegisterNewStoryAPIView.as_view(),
        name = 'new-story'
    ),
]