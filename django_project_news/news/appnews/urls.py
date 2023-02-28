from django.urls import path
from .views import PostNewsList, PostNewsDetail, PostSearch, PostUpdate, PostDelete, PostCreate


urlpatterns = [
   path('', PostNewsList.as_view(),name='start_new'),
   path('<int:pk>', PostNewsDetail.as_view(), name='post_detail'),

   path('search/', PostSearch.as_view(), name='post_search'),

   path('create/', PostCreate.as_view(), name='post_create'),
   path('<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
]

