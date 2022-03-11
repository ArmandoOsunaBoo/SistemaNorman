from django.urls import path
from nursing import views

urlpatterns = [
    path(route='consulta/',view = views.consulta,name="consulta"),
    path(route='history/',view = views.history,name="history"),
    path(route='dictionary/',view = views.dictionary,name="dictionary"),
    path(route='search/',view = views.search_cause,name="search"),
]