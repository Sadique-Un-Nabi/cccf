from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
)

app_name="post"
urlpatterns = [
    path('', PostListView.as_view(), name='home'),
    path('create/', PostCreateView.as_view(), name='create'),
    path('<int:pk>/', PostDetailView.as_view(), name='detail'),  # URL for post detail
    
]