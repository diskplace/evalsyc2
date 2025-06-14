from django.shortcuts import render,redirect, get_object_or_404
from .models import Webinar,WebinarAttendees,ResponseQuestionaire,Speaker,Test_Question,TestResponse,Choice
from django.db.models import Avg,F
from django.core.mail import send_mail
from django.conf import settings
from django.core import serializers
from django.http import JsonResponse
import qrcode
import re
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

def events_data(request):
    events = []

    for webinar in Webinar.objects.all():
        events.append({
            'title': webinar.title,
            'start': webinar.start_date.isoformat(),  
            'end': webinar.until_date.isoformat() ,
        })

    return JsonResponse(events, safe=False)


def register(request, id):
    webinar = get_object_or_404(Webinar, id=id)

    if request.method == 'POST':
        school_id = request.POST.get('school_id')
        email = request.POST.get('email')

        attendee = WebinarAttendees(webinar=webinar, school_id=school_id, email=email)
        attendee.save()

        # Email subject and message
        subject = f"Registration Confirmed: {webinar.title}"
        message = (
            f"Hello,\n\n"
            f"You Are now Register \"{webinar.title}\".\n\n"
            f"📅 Date: {webinar.start_date}\n"
            f"📍 Location: {webinar.venue}\n\n"
            f"We look forward to seeing you there!\n\n"
            f"Best regards,\n"
            f"The Webinar Team"
        )

  
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )

        return redirect(register, webinar.id)

    return render(request, 'webinar/register.html', {
        'webinar': webinar
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
    webinar=get_object_or_404(Webinar, id=id)

    speaker=[]
    venue=[]
    meals=[]
    manage=[]
    all_responses = {
    "speaker": speaker,
    "venue": venue,
    "meals": meals,
    "manage": manage}

    if request.method=='POST':

        for key, value in request.POST.items():

            if key.startwith('speaker'):
                speaker.append(value)
            elif key.startwith('venue'):
                venue.append(value)
            elif key.startwith('meals'):
                meals.append(value)
            elif key.startwith("manage"):
                manage.append(value)
            
        for catergory , reponses in all_responses:
            ResponseQuestionaire.objects.create(
                webinar=webinar,
                user=request.user,
                type=catergory,
                q1=reponses[0],
                q2=reponses[1],
                q3=reponses[2],
                q4=reponses[3],
                q5=reponses[4],

            )
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



def create_test(request, id):
    webinar = get_object_or_404(Webinar, id=id)
    
    if request.method == 'POST':
        test_type = request.POST.get("test_type")
        q_type = request.POST.get('q_type')
        question_text = request.POST.get('question')

        if q_type == 'FB':
            fb_ans = request.POST.get("FB")
            Test_Question.objects.create(
                webinar=webinar,
                question=question_text,
                test_type=test_type,
                question_type=q_type,
                correct_answered=fb_ans
            )


        elif q_type == 'MC':
            mc_ans = int(request.POST.get("MC_correct",0))
            nc = int(request.POST.get("NC")) 

            question = Test_Question.objects.create(
                webinar=webinar,
                question=question_text,
                test_type=test_type,
                question_type=q_type,
                correct_answered=mc_ans
            )
            print(f"jkfsdoaifwoeu: {question.choices}")

            for i in range( nc + 1):  
                mc_choice = request.POST.get(f"MC_choice_{i}")
                if mc_choice: 
                    if mc_ans==i:
                        Choice.objects.create(
                        question=question,
                        text_option=mc_choice,
                        is_correct=True)
                    else:
                        Choice.objects.create(
                        question=question,
                        text_option=mc_choice,
                        is_correct=False)

        
        return redirect("redirect_create_test", id=id)  

    return redirect("redirect_create_test", id=id)

def redirect_create_test(request, id):
    webinar = get_object_or_404(Webinar, id=id)
    question=Test_Question.objects.filter(webinar=webinar)
    choices=Choice.objects.filter(question__in=question)
    json_choices=serializers.serialize("json", choices)
    q_count=len(question)

    return render(request, "webinar/create_test.html", {
        'id': id,
        'questions': question,
        'choices': json_choices,
        'count': q_count
        
    })

def edit_test(request, id):
    webinar=get_object_or_404(Webinar, id=id)
    if request.method== 'POST':
       inputs=request.POST.keys()
       for input in inputs:
            if re.search("question_", input):
                edit_question=input
                search_id=re.findall(r"\d+", edit_question)[0]
                question_text=request.POST.get(f"question_{search_id}")
        
                test=Test_Question.objects.get(id=search_id)
                q_type=request.POST.get(f"question_type_{search_id}")
                print(f"question type: {q_type}")
                if q_type == 'FB':
                    print("qtype works")
                    answered = request.POST.get(f"fb_ans_{search_id}")
                    test.question=question_text
                    test.correct_answered=answered
                    print(f"text: {question_text}")
                    print(f"text: {answered}")
                    print(f"id: {search_id}")
                    
                elif q_type == 'MC':  
                    answered = request.POST.get(f"option_{search_id}")
                    test.question=question_text
                    test.correct_answered=answered
                test.save()

                
            elif re.search("option_", input):
                choice_id = re.findall(r"\d+", input)[0]

                text_option = request.POST.get(f'text_option_{choice_id}', '')

                try:

                    
                    option = Choice.objects.get(id=choice_id)
                    question_id = option.question.id  

                   
                    selected_choice_id = request.POST.get(f"option_{question_id}") 
                    is_correct = (str(option.id) == selected_choice_id)

                    
                    option.text_option = text_option
                    option.is_correct = is_correct
                    option.save()
                except Choice.DoesNotExist:
                    continue  

    return redirect(redirect_create_test, id=id)


def delete_question(request, id):
    print(f"this is the delete id {id}")
    test=Test_Question.objects.get(id=id)
     
    test.delete()
    return redirect(redirect_create_test, id=test.webinar.id)

def display_test(request, id, type):
    webinar=Webinar.objects.get(id=id)

    question=webinar.question.filter(test_type=type)
    
    return render(request, "webinar/display_test.html", {
        "questions":question,
        "id":id,
        "type":type
    })

def record_test(request, id, type):
    webinar=Webinar.objects.get(id=id)
    question=webinar.question.filter(test_type=type)

    if request.method=='POST':
        userinputs=request.POST.key()
        for userinput in userinputs:
            correct=False
            if re.findall( "user_input_",userinput):
                input_id=userinput
                q_id=re.findall(r'\d+',input_id)[0]
                output_value=request.POST.get(f"user_input_{q_id}")
            
                try:
                    question=Test_Question.objects.get(id=q_id)
                    
        
                    if question.correct_answered==output_value:
                        correct=True
                    else:
                        correct=False
                        store_result=TestResponse.objects.create(
                                user=request.user,
                                question=question,
                                user_input=output_value,
                                is_correct=correct)                 

                except Test_Question.DoesNotExist:
                    mc_option=Choice.objects.get(id=output_value)
                    if mc_option.is_correct:
                        correct=True

                    store_result=TestResponse.objects.create(
                            user=request.user,
                            question=mc_option.question,
                            user_input=output_value,
                            is_correct=correct)