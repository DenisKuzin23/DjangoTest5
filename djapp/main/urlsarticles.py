from django.urls import path
from . import views


urlpatterns = [
    path('', views.articles, name='articlesindex'),
    path('<int:id>/page', views.articlespaged, name='apaged'),
    path('<int:id>', views.article, name='article'),
    path('create/', views.addarticle, name='addarticle'),
    path('<int:pk>/edit', views.editarticle, name='editarticle'),
    path('<int:pk>/delete', views.deletearticle, name='deletearticle'),
    path('<int:pk>/editarticle', views.do_editarticle),
    path('create/createarticle', views.createarticle)
]