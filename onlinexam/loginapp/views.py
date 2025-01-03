from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from .models import Question
from django.contrib import messages
# Create your views here.
def signup(request):
    if request.method=="POST":
        username=request.POST["username"]
        password=request.POST["password"]
        password2=request.POST["confirm_password"]
        email=request.POST["email"]

        if password2==password:
            if User.objects.filter(username=username).exists():
                messages.error(request,"user already exist")
                return redirect('/loginapp/signup/')
            
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request,'email already exist')
                    return redirect('/loginapp/signup/')

                else:
                    user=User.objects.create_user(username=username,password=password,email=email)
                    user.save()
                    return render(request,'login.html')

        else:
            messages.error(request,'password not match')
            return redirct("/loginapp/signup/")

    return render(request,'signup.html')

def login(request):
    if request.method=='POST':
        un=request.POST.get('username')
        password=request.POST.get('password')
        print(un,password)
        user=auth.authenticate(username=un,password=password)

        if user is not None:
            auth.login(request,user)
            request.session['questionindex']=0
            request.session['answer']={}
            request.session['score']=0
            messages.success(request,'login successfully')
            questionlist=Question.objects.all()
            question=questionlist[0]
            return render(request,'question.html',{'question':question})
            
        else:
            messages.error(request,'invalid credential')
            return redirect('/loginapp/login/')
    return render(request,'login.html')

def nextQuestion(request):
    if 'op' in request.GET:
        allanswer=request.session['answer']
        allanswer[request.GET.get('qno')]=[
            request.GET['qno'],
            request.GET['qtext'],
            request.GET['answer'],
            request.GET['op']
            ]
        print(f"aaaaaaaaa:{allanswer}")
        
    allquestion=Question.objects.all()

    if request.session['questionindex']<len(allquestion)-1:
        request.session['questionindex']=request.session['questionindex']+1
        question=allquestion[request.session['questionindex']]
        return render(request,'question.html',{'question':question})
    else:
        return render(request,'question.html',{'question':allquestion[len(allquestion)-1]})

def previousQuestion(request):
    if 'op' in request.GET:
        allanswer=request.session['answer']
        allanswer[request.GET['qno']]=[
            request.GET['qno'],
            request.GET['qtext'],
            request.GET['answer'],
            request.GET['op']
        ]
    
    allquestion=Question.objects.all()
    if request.session['questionindex']>0:
        request.session['questionindex']=request.session['questionindex']-1
        question=allquestion[request.session['questionindex']]
        return render(request,'question.html',{'question':question})
    else:
        return render(request,'question.html',{'question':allquestion[0]})

def endExam(request):
    if 'op' in request.GET:
        allanswer=request.session['answer']
        allanswer[request.GET['qno']]=[request.GET['qno'],request.GET['qtext'],request.GET['answer'],request.GET['op']]
        print(allanswer)
    allanswer=request.session['answer']
    listoflist=allanswer.values()
    print(listoflist)

    for list in listoflist:
        if list[2]==list[3]:
            request.session['score']=request.session['score']+1
    
    return render(request,'score.html',{"score":request.session['score']})
