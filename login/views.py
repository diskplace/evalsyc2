from django.shortcuts import render,redirect,get_object_or_404
from .models import Number
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
import pyotp
from django.http import JsonResponse
from django.utils import timezone

from webinar.models import Webinar
# Create your views here.


def index(request):
    webinar=Webinar.objects.all()
    upcoming_webinars = Webinar.objects.filter(
        start_date__gte=timezone.now()  
    ).order_by('start_date')[:3]

    if request.user.is_authenticated:
        
        if request.user.is_superuser:
            return redirect('admin_events')
        else:
            return render(request, 'login/user_dashboard.html', {
            'webinars':webinar
        })

            
    
    return render(request, 'login/index.html',{
        'webinars':upcoming_webinars
    })

def login_view(request):
    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")

        user=authenticate(username=username,password=password)

        if user is not None:
            request.session['username']=username
        
            return redirect(generate_otp)
    return render(request, 'login/login.html')

def logout_view(request):
    logout(request)
    return redirect(login_view)

def register(request):
    if request.method=="POST":
        username=request.POST.get("username")
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        email=request.POST.get("gmail")
        number=request.POST.get("number")
        password=request.POST.get("password")

        if User.objects.filter(username=username).exists():
            messages.error(request,"username Already Exist")
        elif User.objects.filter(email=email).exists():
            messages.error(request,"Email Already Exist")
        else:
            user= User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
            user.save()

            number=Number(user=user,number=number)
            number.save()

            messages.success(request,"You are now Registered")
            return redirect(login_view)

        return redirect(login_view)
    return render(request, 'login/register.html')

def generate_otp(request):
    username = request.session.get('username')
    if not username:
        return redirect('login')

    user = get_object_or_404(User, username=username)

    # Check if the OTP secret key is already in session
    if 'otp_secret_key' not in request.session:
        request.session['otp_secret_key'] = pyotp.random_base32()

    otp_secret_key = request.session['otp_secret_key']
    totp = pyotp.TOTP(otp_secret_key)
    otp_code = totp.now()

    if request.method == 'POST':
        user_otp = request.POST.get('otp')

        # Verify if the user OTP is valid
        if totp.verify(user_otp, valid_window=1):  
            login(request, user)
            request.session.modified = True
            del request.session['otp_secret_key']
            del request.session['username']
            return redirect('index')  
        else:
            return render(request, 'login/otp.html', {
                'otp': otp_code
            })

    send_mail(
        'OTP Code',
        f'Your OTP code is: {otp_code} Description description description',
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False
    )

    return render(request, 'login/otp.html', {'otp': otp_code,})

def event_data(request):
    data=[]
    webinars=Webinar.objects.all()
    
    for webinar in webinars:
        data.append({
            "title":webinar.title,
            "start":webinar.start_date.isoformat()
        })

    return JsonResponse(data, safe=False)

#user
def user_dashboard(request):
    return render(request, 'login/user_dashboard.html')

def calendar(request):
    return render(request,"login/user_nav/calendar.html")

def attendance(request):
    return render(request, "login/user_nav/attendance.html")

def aboutus(request):
    return render(request, "login/user_nav/aboutus.html")

def certificate(request):
    return render(request, "login/user_nav/certificate.html")

def evaluation_nav(request):
    return render(request, "login/user_nav/evaluation.html")


#ADMIN
def admin_panel(request):
    webinars=Webinar.objects.all()
    return render(request, 'login/admin_panel.html',{
        'webinars':webinars
    })


def admin_events(request):
    return render(request,"login/admin_panel/events.html")

def admin_calendar(request):
    return render(request,"login/admin_panel/calendar.html")

def admin_certificate(request):
    return render(request, "login/admin_panel/certificate.html")

def admin_events(request):
    webinar=Webinar.objects.all()
    return render(request, "login/admin_panel/events.html",{
        'webinars':webinar
    })

def admin_setting(request):
    return render(request, "login/admin_panel/setting.html")

def admin_users(request):
    users=User.objects.all()
    return render(request, "login/admin_panel/users.html",{
        'users':users
    })

def register_user(request):
    if request.method=="POST":
        username=request.POST.get("username")
        full_name=request.POST.get('fullname').strip()
        name=full_name.split(" ")

        if not name:
            first_name = ''
            last_name = ''
        elif len(name) == 1:
            first_name = name[0]
            last_name = ''
        else:
            first_name = name[0]
            last_name = ' '.join(name[1:])

        email=request.POST.get("gmail")
        number=request.POST.get("number")
        password=request.POST.get("password")

        if User.objects.filter(username=username).exists():
            messages.error(request,"username Already Exist")
        elif User.objects.filter(email=email).exists():
            messages.error(request,"Email Already Exist")
        else:
            user= User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
            user.save()

            number=Number(user=user,number=number)
            number.save()
    return redirect('admin_events')

def create_admin(request):
    if request.method=='POST':
        full_name=request.POST.get().split(" ")
        User.objects.create_superuser(
        )
    

def delete_user(request, id):
    user=User.objects.filter(id=id)
    user.delete()

    return redirect("admin_users")
