from django.conf.urls import url,include
from . import views

urlpatterns = [
    url(r'^signup/', views.signup),
    url(r'^login/', views.log_in),
	url(r'^msgbox/',views.msgbox),
]
