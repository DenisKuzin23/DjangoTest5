from django.urls import path
from . import views


urlpatterns = [
    path('', views.news, name='newsindex'),
    path('<int:id>/page', views.newspaged, name='npaged'),
    path('<int:id>', views.new, name='newnew'),
    path('create/', views.addnew, name='addnew'),
    path('<int:pk>/edit', views.editnew, name='editnew'),
    path('<int:pk>/delete', views.deletenew, name='deletenew'),
    path('<int:pk>/editnew', views.do_editnew),
    path('create/createnew', views.createnew),
    path('search/', views.searchnews, name='newssearch'),
    path('search/do_search', views.do_search)
]