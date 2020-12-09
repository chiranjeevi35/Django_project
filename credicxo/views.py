from django.shortcuts import render
from rest_framework.decorators import api_view
import json
import jwt 
from django.http import JsonResponse
import re
from .forms import signup_infoform
from .models import signup_info
from .services import generate_jwttoken,validatejwttoken,getownership
# Create your views here.

@api_view(['POST'])
#Signup users  
def signup_view(request):
    #converting request body to json
    user_details = json.loads(request.body)
    mob=user_details.get('mob_no')
    #validation for mobile_no wheather it contains digit
    if not mob.isdigit():
        return JsonResponse({"msg":"Please enter valid Mobile Number"},status=201)
    #print(temp)
    if len(mob) != 10:
        return JsonResponse({'msg':'mobile number must contains 10 digits'},status=201)

    passd=user_details.get('pwd')

    
    reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,18}$"

    # compiling regex
    match_re = re.compile(reg)

    # searching regex
    # re is regularexpression
    temp = re.search(match_re, passd)
    if not temp:
        return JsonResponse({'msg':'please enter atleast one number,one spl character and one capital letter.Min password length is 8 and max is 18'})

    name=user_details.get('name')
    #validation for name wheather it contains alphabet
    if  not name.isalpha():
        return JsonResponse({"msg":"Please enter valid name"},status=201)
   # print(temp)

    example = user_details.get('email')
    reg = "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    ma = re.compile(reg)
    temp = re.search(ma,example)
   # print(temp)
    if  temp == None:
        return JsonResponse({'msg':'please enter valid mail address'},status=201)
    user_details["email"] = example.lower()
    try:
        user=signup_info.objects.get(email=str(example))
        return JsonResponse({'msg':'User Already Exist'},status=201)
    except Exception as e:
        form = signup_infoform(user_details)

        print(form.errors)
        if  form.is_valid():
            form.save()
            return JsonResponse({'msg':'success'})
    return JsonResponse({'msg':'error by adding the data'},status=201)  

@api_view(['GET'])      
def login_view(request):
    #User Login
    userdetails = json.loads(request.body)
    email = userdetails.get("email")
    pwd = userdetails.get("pwd")
    try:
        user = signup_info.objects.get(email=str(email))
    except Exception as e:
        return JsonResponse({'msg':'User Doesnot Exist'},status=201)
    if str(pwd) != str(user.pwd):
        return JsonResponse({'msg':'Please enter correct Password'},status=201)
    accesstoken=generate_jwttoken(email)
    return JsonResponse({'accesstoken':accesstoken})

@api_view(['PUT'])
def forget_view(request):
    #Forget Password
    userdetails = json.loads(request.body)
    emial = userdetails.get("email")
    pwd = userdetails.get("pwd")
    try:
        user = signup_info.objects.get(email=str(emial))
    except Exception as e:
        return JsonResponse({'msg':'User Doesnot Exist'},status=201)
    reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,18}$"
    # compiling regex
    match_re = re.compile(reg)
    # searching regex
    # re is regularexpression
    temp = re.search(match_re, pwd)
    if not temp:
        return JsonResponse({'msg':'please enter atleast one number,one spl character and one capital letter.Min password length is 8 and max is 18'})
    print(user.pwd)
    user.pwd=str(pwd)
    print(user.pwd)
    user.save()
    return JsonResponse({'msg':'pwd updated successfully'})

@api_view(['GET'])
def validate_token(request):
    #Token validation
    username,role=validatejwttoken(request)
    return JsonResponse({'msg':'successfully validated'})

@api_view(['POST'])
def addteacher_view(request):
    #adding Teacher or student by admin
    username,role=validatejwttoken(request)
    if str(role) != "admin":
        return JsonResponse({'msg':'Sorry, only admin can add teachers'},status=201)
    teacherdata = json.loads(request.body)
    email = teacherdata.get("email")
    try:
        user = signup_info.objects.get(email=str(email))
    except Exception as e:
        return JsonResponse({'msg':'User Doesnot Exist'},status=201)    
    role = teacherdata.get("role")
    user.role = role
    user.save()

    return JsonResponse({'msg':'success'})

@api_view(['GET'])
def getallusers_view(request):
    #Admin Viewing all users
    username,role=validatejwttoken(request)

    if str(role) != "admin":
        return JsonResponse({'msg':'Sorry, only admin can see all users'},status=201)
    users = signup_info.objects.all()
    arr = []
    for user in users:
        data = {"email":user.email,"mobile number":user.mob_no,"password":user.pwd,"name":user.name,"role":user.role}
        arr.append(data)
    jsondata = {'users':arr}
    return JsonResponse(jsondata)

@api_view(['GET'])
def listteacher_view(request):
    #Admin Listing all Teachers
    username,role=validatejwttoken(request)
    if str(role) != "admin":
        return JsonResponse({'msg':'Sorry, only admin can see all users'},status=201)
    role="teacher"
    try:
        users = signup_info.objects.filter(role=role)
    except Exception as e:
        print(e)
        
    arr = []
    for user in users:
        data = {"email":user.email,"mobile number":user.mob_no,"password":user.pwd,"name":user.name,"role":user.role}
        arr.append(data)
    jsondata = {'users':arr}
    
    return JsonResponse(jsondata)
        #return JsonResponse({'msg':'success'})

@api_view(['GET'])
def liststudent_view(request):
    #Listing all Students
    username,role=validatejwttoken(request)
    if str(role) != "admin":
        return JsonResponse({'msg':'Sorry, only admin can see all users'},status=201)
    role="student"
    try:
        users = signup_info.objects.filter(role=role)
    except Exception as e:
        print(e)
        
    arr = []
    for user in users:
        data = {"email":user.email,"mobile number":user.mob_no,"password":user.pwd,"name":user.name,"role":user.role}
        arr.append(data)
    jsondata = {'users':arr}
    
    return JsonResponse(jsondata)        

@api_view(['POST'])    
def addstudentby_teacher(request):
    # Teacher adding Student
    username,role=validatejwttoken(request)
    if str(role) != "teacher":
        return JsonResponse({'msg':'Sorry, only teacher can add students'},status=201)
    teacherdata = json.loads(request.body)
    email = teacherdata.get("email")
    try:
        user = signup_info.objects.get(email=str(email))
    except Exception as e:
        return JsonResponse({'msg':'User Doesnot Exist'},status=201)    
    role = 'student'
    user.role = role
    user.save()
    return JsonResponse({'msg':"student details added successfully"})

@api_view(['GET'])
def getindividualdetails(request):
    #Any user view details
    username,role=validatejwttoken(request)
    try:
        users = signup_info.objects.filter(email=str(username))
    except Exception as e:
        return JsonResponse({'msg':'User Doesnot Exist'},status=201) 
    arr = []
    for user in users:
        data = {"email":user.email,"mobile number":user.mob_no,"password":user.pwd,"name":user.name,"role":user.role}
        arr.append(data)
    jsondata = {'users':arr}
    return JsonResponse(jsondata)
