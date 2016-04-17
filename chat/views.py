from django.shortcuts import render
import urllib
import json
from .models import Profile
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from chat.models import Message
from django.contrib.auth.decorators import login_required
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
	return HttpResponse("Success: true")
	
@csrf_exempt
def log_in(request):
	if request.method=='POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(username=username, password=password)	
		if user is not None:
			if user.is_active:
				login(request, user)
				return HttpResponse("Success: true")
				# Redirect to a success page.
			else:
				return HttpResponse("User Inactive")
				# Return a 'disabled account' error message
		else:
			return HttpResponse("Success: false")
			# Return an 'invalid login' error message.
			
@csrf_exempt
@login_required
def msgbox(request):
	if request.method=='POST':
		message=Message()
		message.message=request.POST.get('message')
		message.user_name= request.user.username
		message.image=request.user.profile.image
		return HttpResponse("Success: true")
		#return render(request.'index.html',{'message':message,'image'=image,'username'=username})
	else:
		return HttpResponse('please enter the message again!')
'''@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_scholarships(request):
	scholarship_list = scholarship.objects.all()
	serializer=ScholarshipSerializer(scholarship_list,many=True)
	return Response(serializer.data)'''