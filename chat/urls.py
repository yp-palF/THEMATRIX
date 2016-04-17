from django.conf.urls import url,include
from . import views

urlpatterns = [
    url(r'^signup/', views.signup),
    url(r'^login/', views.log_in),
	url(r'^sendmsg/',views.msgbox),
	#url(r'^index/',views.index
]