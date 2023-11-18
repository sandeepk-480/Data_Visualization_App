from django.shortcuts import render
from app.models import Dataviz, Contact
from datetime import datetime
from django.contrib import messages
from django.shortcuts import redirect
from django.views.decorators.cache import cache_control
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


# Create your views here.
def topic(num_records=5):
    data_obj = Dataviz.objects.all()
    d_list = []
    for obj in data_obj:
        d_list.extend(obj.d[:num_records])

    topics = []
    topic_dict = {}

    for data in d_list:
        topics.append(data.get('topic', 'unknown'))
    for i in topics:
        if i in topic_dict:
            topic_dict[i] += 1
        else:
            topic_dict[i] = 1

    return topic_dict

#----------------------------------------------------------------------------------------------------------------------------------------------------

def chart1(num_records=5):
    data_objects = Dataviz.objects.all()

    data_list = []
    for obj in data_objects:
        data_list.extend(obj.d[:num_records])
    
    # Extract data for each variable
    topic_data = {}

    for data in data_list:
        topic = data.get('topic', 'Unknown')
        intensity = data.get('intensity', 0)
        if intensity == "":
            intensity=0
        likelihood = data.get('likelihood', 0)
        if likelihood == "":
            likelihood=0

        if topic in topic_data:
            topic_data[topic]['intensities'].append(intensity)
            topic_data[topic]['likelihoods'].append(likelihood)
        else:
            topic_data[topic] = {'intensities': [intensity], 'likelihoods': [likelihood] }               # example- {'Weather': {'intensities': [8, 6], 'likelihoods': [0.85, 0.75]}, 'Technology': {'intensities': [9], 'likelihoods': [0.95]}}


    # print(topic_data)
    avg_data = []
    for topics, values in topic_data.items():

        avg_intensity = sum(values['intensities']) / len(values['intensities'])
        avg_likelihood = sum(values['likelihoods']) / len(values['likelihoods'])

        avg_data.append({
            'topic': topics,
            'avg_intensity': avg_intensity,
            'avg_likelihood': avg_likelihood,
        })
    
    return avg_data
    


def chart2(num_records=5):                              # Not considering sectors which dont have their start and end years
    data_object = Dataviz.objects.all()
    data_list = []
    for obj in data_object:
        data_list.extend(obj.d[:num_records])

    sector_data = {}

    for data in data_list:
        sector = data.get('sector', 'unknown')
        start_year = data.get('start_year', 0)
        if start_year == "":
            start_year = 0
        end_year = data.get('end_year', 0)
        if end_year == "":
            end_year = 0

        if start_year == 0 and end_year == 0:
            continue

        if sector in sector_data:
            sector_data[sector].append({'start_year': start_year, 'end_year': end_year})
        else:
            sector_data[sector] = [{'start_year': start_year, 'end_year': end_year}]
    
    sector_years = []

    for sector, years_list in sector_data.items():
        sector_years.append({'sector':sector, 'years':years_list})


    return sector_years


def chart3(num_records=5):                              # Not considering topic which dont have their start and end years
    data_object = Dataviz.objects.all()
    data_list = []
    for obj in data_object:
        data_list.extend(obj.d[:num_records])

    topic_data = {}

    for data in data_list:
        topic = data.get('topic', 'unknown')
        start_year = data.get('start_year', 0)
        if start_year == "":
            start_year = 0
        end_year = data.get('end_year', 0)
        if end_year == "":
            end_year = 0

        if start_year == 0 and end_year == 0:
            continue

        if topic in topic_data:
            topic_data[topic].append({'start_year': start_year, 'end_year': end_year})
        else:
            topic_data[topic] = [{'start_year': start_year, 'end_year': end_year}]
    
    topic_years = []

    for topic, years_list in topic_data.items():
        topic_years.append({'topic':topic, 'years':years_list})


    return topic_years

# --------------------------------------------------------------------------------------------------------------------------------------------------
@login_required
def dashboard(request):
    num_records = int(request.GET.get('num_records', 5))

    avg_data = chart1(num_records)
    sector_years = chart2(num_records)
    topic_years = chart3(num_records)
    topic_dict = topic(num_records)

    return render(request, 'dashboard.html', {
        'avg_data': avg_data,
        'sector_years': sector_years,
        'topic_years': topic_years,
        'num_records': num_records,
        'topics':topic_dict,
    })




def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username , password=password)
        if user is not None:
            login(request, user)
            return redirect('/home/')
        else:
            messages.error(request, 'Invalid Credentials')
            return render(request, 'login.html')
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    request.session.clear()
    return redirect('/login')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if not username or not password1 or not password2 or not fname or not lname or not email:
            messages.error(request, "All fields are required")  
            return redirect('register')

        if len(username)>10:
            messages.error(request, "Your username Should be under 10 Characters ")
            return redirect('register')
        
        if not username.isalnum():
            messages.error(request, "Username Should Only COntain Letters and Numbers")
            return redirect('register')
        if (password1 != password2):
            messages.error(request, "Passwords do not match")
            return redirect('register')
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username has been taken")
            return redirect('register')
        if len(password1)<8:
            messages.error(request, "password should be atleast 8 character long")
            return redirect('register')
    
        myuser = User.objects.create_user(username, email, password1)
        myuser.first_name= fname
        myuser.last_name= lname
        myuser.save()

        messages.success(request, "User has been created")
        return redirect('login')

    return render (request, 'register.html')


@login_required
def contact(request):
    if request.method == 'POST':
        name1 = request.POST.get('name')         # 'name' here should be same as name mentioned in the contact.html
        email1 = request.POST.get('email')       # 'email' here should be same as name mentioned in the contact.html
        phone1 = request.POST.get('phone')       # 'phone' here should be same as name mentioned in the contact.html
        desc1 = request.POST.get('desc')         # 'desc' here should be same as name mentioned in the contact.html


        if len(phone1) < 9:
            messages.error(request, "Phone number should be greater than 9")
            return redirect('contactus')

        contact1 = Contact(name=name1, email=email1, phone=phone1, desc=desc1, date=datetime.today())
        contact1.save()
        messages.success(request, "Your message has been sent")
    return render(request,'contact.html')


@login_required
def about_us(request):
    return render(request, 'aboutus.html')