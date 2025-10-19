from django.urls import path

from . import views
urlpatterns = [
 path('', views.index, name='movies.index'),
 path('<int:pk>/', views.movie_detail, name='movie_detail'),
 path('<int:id>/review/create/', views.create_review, name='movies.create_review'),
 path('<int:id>/review/<int:review_id>/edit/', views.edit_review, name='movies.edit_review'),
 path('<int:id>/review/<int:review_id>/delete/', views.delete_review, name='movies.delete_review'),
 path('movies/<int:pk>/', views.movie_detail, name='movie_detail'),
 path("petitions/", views.petition_list, name= "petition_list"),
 path("petitions/new", views.petition_create, name= "petition_create"),
 path("petitions/<int:petition_id>/vote/<str:value>/", views.petition_vote, name="petition_vote"), 
 path('local_popularity_map/', views.local_popularity_map, name= 'local_popularity_map'),
]
