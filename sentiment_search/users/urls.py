from django.conf.urls import url
from sentiment_search.users import views

urlpatterns = [
    url(r'^dashboard$', views.profile),
    url(r'^notification$',views.report),
    url(r'^login$',views.login),
    url(r'^register$',views.register),
    url(r'^logout$',views.logout),
    url(r'^session$',views.get_session),
     #url(r'^business/submit/$', views.submit_dashboard),
]
