from django.conf.urls import url
from sentiment_search.business import views

urlpatterns = [
    url(r'^dashboard$', views.profile),
    url(r'^report$',views.report),
    url(r'^data$',views.data_day),
    url(r'^login$',views.login),
    url(r'^register$',views.register),
    url(r'^logout$',views.logout),
     #url(r'^business/submit/$', views.submit_dashboard),
]
