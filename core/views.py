from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import Course
from django.db.models import Q


# Create your views here.
@login_required(login_url = 'core:login_data')
def index(request):
    return render(request, 'index.html')

def login_data(request):
    if request.method == 'POST':
        username=request.POST['username']
        password = request.POST['password']

       
        user = authenticate(username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('core:index')
        else:
            return HttpResponse("user does not exist")
    else:
        return render(request,'login.html')
    
def logout_user(request):
    logout(request)
    return redirect('core:login_data')


def view_course(request):
    course = Course.objects.all()
    paginator = Paginator(course,5)
    page = request.GET.get('page')
    paged_product = paginator.get_page(page)
    context = {'course':paged_product}
    return render(request,'viewcourse.html',context)

def profile(request):
    return render(request,'profile.html')

def add_course(request):
    if request.method == 'POST' and 'course_image' in request.FILES:
        title = request.POST['title']
        subtitle = request.POST['subtitle']
        image = request.FILES['course_image']
        amount = request.POST['amount']
        amounttext = request.POST['amounttext']
        description = request.POST['description']
        status = request.POST['status']

        if status == 'Enable':
            status_value = True
        else:
            status_value = False

        
        course = Course(title=title,subtitle=subtitle,image=image,amount=float(amount),amount_text=amounttext,description=description,status=status_value)
        course.save()
        return redirect('core:view_course')


        
    else:

        return render(request,'addcourse.html')
    
def delete_course(request,id):
    course_id = id
    try:
        course = Course.objects.filter(id=course_id).first()
        course.delete()
        return redirect('core:view_course')
    except:
        return HttpResponse("failed to delete data")



def course_active(request,id):
    try:
        course = Course.objects.filter(id=id).first()
        course.status = True
        course.save()
        return redirect('core:view_course')

    except:
        return HttpResponse("no course available")
    
def course_inactive(request,id):
    try:
        course = Course.objects.filter(id=id).first()
        course.status = False
        course.save()
        return redirect('core:view_course')
    except:
        return HttpResponse("no course available")

def change_password(request):
    username = request.user.username
    if request.method == 'POST':
        cpassword = request.POST['cpassword']
        npassword = request.POST['npassword']
        confirm_npassword = request.POST['confirm_npassword']

        if npassword == confirm_npassword:
            
            user = authenticate(username=username,password=cpassword)
            if user is not None:

                user.set_password(npassword)
                user.save()
                return redirect('core:login_data')
            else:
                return HttpResponse('user not found')

            
        else:
            return HttpResponse('password does not match')
    

def search(request):
    if request.method == 'POST':
        key = request.POST['key']
    
        try:
            course = Course.objects.filter(Q(title__icontains = key) | Q(description__icontains = key) )
            paginator = Paginator(course,5)
            page = request.GET.get('page')
            paged_product = paginator.get_page(page)
            context = {'course':paged_product}
            
            return render(request,'viewcourse.html',context)
        except:
            
            return redirect('core:view_course')
    else:
        return redirect('core:view_course')


def edit_course(request,id):
    if request.method == 'POST':
        title=request.POST['title']
        subtitle=request.POST['subtitle']
        description=request.POST['description']
        amount=request.POST['amount']
        amounttext=request.POST['amounttext']
        status=request.POST['status']

        course = Course.objects.filter(id=id).first()
        course.title = title
        course.subtitle = subtitle
        course.description = description
        course.amount = amount
        course.amount_text = amounttext
        
        if 'course_image' in request.FILES:
            image = request.FILES['course_image']
            print(image)
            course.image = image
        

        if status == 'Enable':
            status_value = True
        else:
            status_value = False
        course.status = status_value

        course.save()
        return redirect('core:view_course')
    else:

        try:
            course = Course.objects.filter(id=id).first()
            context = {'course':course}
        except:
            return redirect('core:view_course')
        return render(request,'editcourse.html',context)


    