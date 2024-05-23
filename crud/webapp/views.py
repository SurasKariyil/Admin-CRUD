from django.shortcuts import render,redirect
from .forms import CreateUserForm,LoginForm,CreateRecordForm,UpdateRecordForm

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate

from django.contrib.auth.decorators import login_required

from .models import Record

from django.contrib import messages

#homepage

def home(request):
   
    return render(request, 'webapp/index.html')

#register a user

def register(request):

    form = CreateUserForm()
    
    if request.method == "POST":
        form = CreateUserForm(request.POST)

        if form.is_valid():
        
            form.save()

            messages.success(request,"Account created successfully")

            return redirect("my-login")

    context = {'form':form}

    return render(request,'webapp/register.html', context=context)

#login a user



def my_login(request):

    form = LoginForm()

    if request.method == "POST":

        form = LoginForm(request, data=request.POST)

        if form.is_valid():

            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:

                auth.login(request, user)
 # Store user-specific data in session
                request.session['username'] = username
                messages.success(request, "You have logged in")
                return redirect('dashboard')
            
    context = {'form': form}

    return render(request, 'webapp/my-login.html', context=context)


#dashboard

@login_required(login_url='my-login')
def dashboard(request):

# Retrieve user-specific data from session

    username = request.session.get('username')

    my_records = Record.objects.all()

    context = {'records': my_records, 'username': username}

    return render(request, 'webapp/dashboard.html', context=context)


# create a record

@login_required(login_url='my-login')
def create_record(request):
    
    form = CreateRecordForm()

    if request.method == "POST":

        form = CreateRecordForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(request,"Your record was created")

            return redirect("dashboard")
        
    context = {'form':form}
    return render(request,'webapp/create-record.html',context=context)


#update a record

@login_required(login_url='my-login')
def update_record(request,pk):
    
    record = Record.objects.get(id=pk)

    form = UpdateRecordForm(instance=record)

    if request.method == 'POST':

        form = UpdateRecordForm(request.POST, instance=record)

        if form.is_valid():
            form.save()

            messages.success(request,"Your record was updated")

            return redirect("dashboard")
        
    context = {'form':form}

    return render(request,'webapp/update-record.html',context=context)

#read or/ view a singular record

@login_required(login_url='my-login')
def singular_record(request,pk):

    all_records = Record.objects.get(id=pk)

    context = {'record':all_records}

    return render(request, 'webapp/view-record.html',context=context)

#delete a record

@login_required(login_url='my-login')
def delete_record(request,pk):

    record = Record.objects.get(id=pk)

    record.delete()

    messages.success(request,"Your record was deleted!")

    return redirect("dashboard")


#user logout

def user_logout(request):

    auth.logout(request)
# Delete session data upon logout

    if 'username' in request.session:
        del request.session['username']

    messages.success(request, "Logout success!")

    return redirect("my-login")



