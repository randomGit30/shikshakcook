from django.urls import path
from . import views

urlpatterns = [
    path('landing/', views.landing, name='landing-page'),
    path('publish/', views.publish_recipe, name='publish_recipe'),
    path('read/', views.read_recipes, name='read_recipes'),
    path('cure/', views.cure_recipes, name='cure_recipes'),

]
