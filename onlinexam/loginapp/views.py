from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from .models import Question,Result
from django.contrib import messages
# Create your views here.
def signup(request):
    if request.method=="POST":
        username=request.POST["username"]
        password=request.POST["password"]
        password2=request.POST.get("confirm_password")
        email=request.POST.get("email")

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
            return redirect("/loginapp/signup/")

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
            
            return render(request,'subject.html')
            
        else:
            messages.error(request,'invalid credential')
            return redirect('/loginapp/login/')
    return render(request,'login.html')

def startTest(request):
    subjcectname=request.GET.get("subject",None)
    request.session['subject']=subjcectname
    queryset=Question.objects.filter(subject=subjcectname).values()  # we cant convert queryset into session hence convert them into list
    questionlist=list(queryset)
    print(questionlist)
    request.session['questionlist']=questionlist
    print(questionlist)
    if not questionlist:
        return HttpResponse("No questions available for the selected subject.")
    question = questionlist[0]

    question=questionlist[0]
    return render(request,'question.html',{'question':question})


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
        
    # allquestion=Question.objects.all()
    queryset=Question.objects.filter(subject=request.session.get('subject')).values()  # we cant convert queryset into session hence convert them into list
    allquestion=list(queryset)

    if request.session['questionindex']<len(allquestion) - 1:
        request.session['questionindex']=request.session['questionindex']+1
        question=allquestion[request.session['questionindex']]
        isdisabled = request.session['questionindex'] == len(allquestion) - 1
        return render(request,'question.html',{'question':question,'isdisabled':isdisabled})
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
    
    # allquestion=Question.objects.all()
    queryset = Question.objects.filter(subject=request.session.get('subject'))
  # we cant convert queryset into session hence convert them into list
    allquestion=list(queryset)

    if request.session['questionindex']>0:
        request.session['questionindex']=request.session['questionindex']-1
        question=allquestion[request.session['questionindex']]
        qno=question.qno
        submitteddetails=request.session['answer']

        if str(qno) in submitteddetails:
            questiondetails=submitteddetails[str(qno)]
            previousanswer=questiondetails[3]
            print(f"previousanser={previousanswer}")
        else:
            previousanswer=""

        if question.qno==1:
            isdisabled1=True
        else:
            isdisabled1=False
        return render(request,'question.html',{'question':question,'isdisabled1':isdisabled1,'previousanswer':previousanswer})
    else:
        return render(request,'question.html',{'question':allquestion[0]})

def endExam(request):
   
    if 'answer' in request.session:
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

        finalscore=request.session['score']
        
       
        auth.logout(request)
        
        return render(request,'score.html',{"score":finalscore,'listoflist':listoflist})
    else:
        return render(request,'login.html')
    
