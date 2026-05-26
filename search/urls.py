from django.urls import path
from . import views

app_name = 'search'

urlpatterns = [
    path('',                      views.index,           name='index'),
    path('search/',               views.search_view,     name='search'),
    path('document/<int:doc_id>/',views.document_detail, name='document'),
    path('upload/',               views.upload_view,     name='upload'),
    path('documents/',            views.documents_view,  name='documents'),
    path('delete/<int:doc_id>/',  views.delete_document, name='delete'),
    path('stats/',                views.stats_view,      name='stats'),
    path('login/',                views.login_view,      name='login'),
    path('logout/',               views.logout_view,     name='logout'),
]
