from django.urls import path
from posts.views import PostView, PostlistView

urlpatterns = [
    path('', PostView.as_view()),
    path('/<int:post_id>', PostView.as_view()),
    path('/list', PostlistView.as_view()),

]