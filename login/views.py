from django.shortcuts import render,redirect,get_object_or_404
from .models import UserProfile
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
import pyotp
from django.http import JsonResponse,HttpResponse
from django.utils import timezone
from django.core import serializers
from webinar.models import Webinar,WebinarAttendees
from exam_portal.models import CertificateTemplate
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
            return redirect('user_dashboard')

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

    today=timezone.now().date()
    upcoming_webinar=WebinarAttendees.objects.filter(user=request.user, webinar__start_date__gte=today )   
    past_webinar=WebinarAttendees.objects.filter(user=request.user, webinar__start_date__lt=today )
    upcoming_messages=""
    history_messages=""
    
    if not upcoming_webinar.exists():
        upcoming_messages="No webinar asssigned to you please wait for further notice"
    
    if not past_webinar.exists():
        history_messages="No Webinar Currently"


    return render(request, "login/user_nav/user_dashboard.html",{
        "upcoming_webinars":upcoming_webinar,
        "past_webinars":past_webinar,
        "upcoming_message":upcoming_messages,
        "past_message":history_messages
    })
    
def calendar(request):
    today=timezone.now().date()
    upcoming_webinar=WebinarAttendees.objects.filter(user=request.user, webinar__start_date__gte=today ) 

    return render(request,"login/user_nav/calendar.html",{
        'upcoming_webinars':upcoming_webinar
    })

def attendance(request):
    return render(request, "login/user_nav/attendance.html")

def aboutus(request):
    return render(request, "login/user_nav/aboutus.html")

def certificate(request):
    today = timezone.now().date()

    ongoing_webinars = Webinar.objects.filter(
        until_date__gt=today,
        attendees__user=request.user
    )
    completed_webinars = Webinar.objects.filter(
        until_date__lt=today,

        attendees__user=request.user
    )
    
    return render(request, 'login/user_nav/certificate.html', {
        'ongoind_webinars':ongoing_webinars,
        'completed_webinars': completed_webinars
    })


def certificate_data(request, id):
    webinar=get_object_or_404(Webinar, id=id)
    certificate=CertificateTemplate.objects.filter(webinar=webinar)
    data = serializers.serialize('json', certificate)
    return HttpResponse(data)

def evaluation_nav(request):
    return render(request, "login/user_nav/evaluation.html")

def user_setting(request):
    return render(request, "login/user_nav/user_setting.html")

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
    webinars=Webinar.objects.all()
    today=timezone.now().date()
    
    return render(request, "login/admin_panel/certificate.html",{
        'webinars':webinars,
        'today':today
    })

def admin_events(request):
    webinar=Webinar.objects.all()

    

    return render(request, "login/admin_panel/events.html",{
        'webinars':webinar,
      
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
        full_name=request.POST.get('user_fullname',' ').strip()
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

        email=request.POST.get("user_email")
        password=request.POST.get("user_password")
        school_id=request.POST.get("school_id")
        username=name[0]

        if User.objects.filter(username=username).exists():
            messages.error(request,"username Already Exist")
        elif User.objects.filter(email=email).exists():
            messages.error(request,"Email Already Exist")
        else:
            user= User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
            profile=UserProfile.objects.create(user=user, school_id=school_id)
    return redirect('admin_users')

def generete_authorization_key(request):
   
    otp=pyotp.random_base32()
    code=pyotp.TOTP(otp).now()
    request.session['authorization_key']=code

    send_mail(
    'Request for Admin Authorization Code',
    f'''User {request.user} has requested to create an admin account.
    If you approve this request, please share the following authorization code:

    {code}
    ''',
        f'{settings.EMAIL_HOST_USER}',  
        [f'{settings.ADMIN_EMAIL}'], )
    return redirect('admin_users')
            

def create_admin(request):
    if request.method == 'POST':
        if 'authorization_key' not in request.session:
            messages.error(request, 'Please request an Authorization Key before proceeding.')
            return redirect('admin_users')

        if request.POST.get('admin_code') == request.session.get('authorization_key'):
            del request.session['authorization_key']
            full_name = request.POST.get('admin_fullname', '').strip()
            name = full_name.split(" ")
            first_name = name[0] 
            last_name = ' '.join(name[1:])

            email = request.POST.get("admin_email")
            password = request.POST.get("admin_password")
            username = name[0]

            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists.")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email already exists.")
            else:
                user = User.objects.create_user(
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password=password
                )
                user.is_staff = True
                user.save()
                messages.success(request, "Admin account created successfully.")
        else:
            messages.error(request, "Invalid authorization code.")

    return redirect('admin_users')


def delete_user(request, id):
    user=User.objects.filter(id=id)
    user.delete()

    return redirect("admin_users")


def edit_user(request):
    user = User.objects.get(id=request.user.id)
    profile = UserProfile.objects.get(user=user)

    if request.method == 'POST':
        full_name = request.POST.get('fullname', '').strip()
        if full_name:
            name = full_name.split(" ")
            if not name:
                first_name = ''
                last_name = ''
            elif len(name) == 1:
                first_name = name[0]
                last_name = ''
            else:
                first_name = name[0]
                last_name = ' '.join(name[1:])
            user.username=first_name
            user.first_name = first_name
            user.last_name = last_name

        email = request.POST.get("email")
        img = request.FILES.get("img")  
        number = request.POST.get('number')
        school = request.POST.get('school')

        if email:
            user.email = email

        user.save()

        if img:
            profile.img = img
        if number:
            profile.number = number
        if school:
            profile.school = school
        profile.save()

    if request.user.is_superuser or request.user.is_staff:
        return redirect("admin_setting")
    else:
        return redirect("user_setting")



def change_password(request):
    user=User.objects.get(id=request.user.id)
    if request.method=='POST':
        if request.POST.get("current_password")==user.password:
            new_password=request.POST.get("new_password")
            user.password=new_password
            user.save()
    if request.user.is_superuser or request.user.is_staff:
        return redirect("admin_setting")
    else:
        return redirect("user_setting")

