from django.shortcuts import render,redirect, get_object_or_404
from .models import Webinar,WebinarAttendees,ResponseQuestionaire,Speaker
from django.db.models import Avg,F



# Create your views here.

def make_webinar(request):
    if request.method=='POST':
        title=request.POST.get('title')
        description=request.POST.get('description')
        number_of_speaker=int(request.POST.get('number_of_speaker'))
        event_type=request.POST.get('event_type')
        start_date=request.POST.get('start_date')
        until_date=request.POST.get('until_date')
        time=request.POST.get('event_time')
        banner=request.FILES.get('banner')
        venue=request.POST.get('venue')


        webninar=Webinar(title=title,
                         description=description, number_of_speaker=number_of_speaker, event_type=event_type,
                         start_date=start_date, until_date=until_date, time=time, banner=banner,
                         venue=venue)
        webninar.save()

        for i in range(1,number_of_speaker+1):
            speaker_name=request.POST.get(f'speaker_name{i}')
            speaker_email=request.POST.get(f'speaker_email{i}')
            speaker=Speaker(webinar=webninar, speaker_name=speaker_name, speaker_email=speaker_email)
            speaker.save()
        return redirect('index')

        
        
    return render(request, 'webinar/makewebinar.html')


def webinar_detail(request, id):
    webinar=get_object_or_404(Webinar, id=id)

    return render(request, "webinar/webinar_detail.html",{
        'webinar':webinar
    })


def register(request, id):
    webinar=get_object_or_404(Webinar, id=id)
    if request.method=='POST':
        school_id=request.POST.get('school_id')
        email=request.POST.get('email')
        
        attendee=WebinarAttendees(webinar=webinar,school_id=school_id, email=email)
        attendee.save()
        return redirect(register, webinar.id)
    return render(request, 'webinar/register.html',{
        'webinar':webinar
    })


#validation
def validation(request, id):
    webinar=get_object_or_404(Webinar, id=id)

    if request.method=='POST':
        deped_id=request.POST.get('deped_id')
        email=request.POST.get('email')
        valid= WebinarAttendees.objects.filter(webinar=webinar, school_id=deped_id, email=email).exists()

        if valid:
            return redirect('questionaire', webinar.id)
        else:
            return redirect('validation', webinar.id)

    return render(request, "webinar/evaluation/validation.html", {
        "id":id
    })




#questionaire
def questionaire(request, id):
    user=request.user
    webinar=get_object_or_404(Webinar, id=id)
    if request.method=='POST':
        q1=request.POST.get('q1')
        q2=request.POST.get('q2')
        q3=request.POST.get('q3')
        q4=request.POST.get('q4')
        q5=request.POST.get('q5')
        q6=request.POST.get('q6')
        reponse=ResponseQuestionaire(webinar=webinar, user=user,q1=q1,
            q2=q2,q3=q3,q4=q4,q5=q5,q6=q6)
        reponse.save()
        return redirect(webinar_detail, webinar.id)
    if webinar.event_type == 'recognition':
        return render(request,'webinar/evaluation/recognition.html',{
        'webinar':webinar
    })

    elif webinar.event_type == 'seminar':
        return render(request,'webinar/evaluation/seminar.html',{
        'webinar':webinar
    })


    return render(request,'webinar/evaluation/workshop.html',{
        'webinar':webinar
    })


def average_result(request, id):
    webinar=get_object_or_404(Webinar, id=id)
    average=ResponseQuestionaire.objects.filter(webinar=webinar).aggregate(
        q1=Avg('q1'),
        q2=Avg('q2'),
        q3=Avg('q3'),
        q4=Avg('q4'),
        q5=Avg('q5'),
        q6=Avg('q6'),)
    
    total=sum(average.values())/6

    return render(request, 'webinar/result.html',{
        'webinar':webinar,
        'average':average,
        'total':total


    })