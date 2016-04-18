from django.views.decorators.cache import never_cache
from django.shortcuts import render
import urllib
import json
from .models import Profile
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from chat.models import Message
from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect
@csrf_exempt
def signup(request):
	if request.method=='POST':
		data_user = User()
		data_user.username=request.POST.get('username')
		data_user.set_password(request.POST.get('password'))
		data_user.save()
		
		urlForAPI = "https://randomuser.me/api/"
		response = urllib.urlopen(urlForAPI)
		data = json.loads(response.read())
		resultField = data["results"]
		personInfo = resultField[0]
		location = personInfo["location"]
		name = personInfo["name"]
		
		profile_user = Profile()
		profile_user.title=name["title"].title()
		profile_user.first_name=name["first"].title()
		profile_user.last_name=name["last"].title()
		profile_user.gender = personInfo["gender"].title()
		profile_user.city = location["city"]
		profile_user.state = location["state"]
		profile_user.image = (personInfo["picture"])["thumbnail"]
		profile_user.user_name=data_user
		profile_user.save()
		return HttpResponseRedirect("http://127.0.0.1:8000/chat/login/")
	else:
		response = render(request, 'signup.html', {})
		return response

@csrf_exempt
def log_in(request):
	if request.method=='POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(username=username, password=password)	
		if user is not None:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect("http://127.0.0.1:8000/chat/index/")
				# Redirect to a success page.
			else:
				return HttpResponseRedirect("http://127.0.0.1:8000/chat/login/")
				# Return a 'disabled account' error message
		else:
			return HttpResponseRedirect("http://127.0.0.1:8000/chat/login/")
			# Return an 'invalid login' error message.
	else:
		response = render(request, 'login.html', {})
		return response

@csrf_exempt
@login_required
def msgbox(request):
	if request.method=='POST':
		message=Message()
		message.message=request.POST.get('message')
		message.user_name= request.user.username
		message.image=request.user.profile.image
		message.save()
		return HttpResponseRedirect("http://127.0.0.1:8000/chat/index/")

@login_required	
@never_cache	
def viewmsg(request):
	if request.method=='GET':
		messages=Message.objects.all()
		response = render(request, 'index.html', {'messages':reversed(messages)})
        return response
		
def view_logout(request):
	logout(request)
	response = render(request, 'login.html', {})
	return response
