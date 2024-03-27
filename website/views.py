from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record
from django.contrib.auth.models import AnonymousUser

def home(request):
    if isinstance(request.user, AnonymousUser):
        records = []  # No records to display for anonymous users
    else:
        records = Record.objects.filter(user=request.user)
    
    if request.method == 'POST':
        # Handle login form submission
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have been logged in!')
            return redirect('home')
        else:
            messages.error(request, 'Username or password is incorrect')
            return redirect('home')
    else:
        return render(request, 'home.html', {'records': records})



def logout_user(request):
  logout(request)
  return redirect('home')




def register_user(request):
  if request.method == 'POST':
    form = SignUpForm(request.POST)
    if form.is_valid():
      form.save()
      #authenticate and login
      username = form.cleaned_data['username']
      password = form.cleaned_data['password1']
      user = authenticate(username=username, password=password)
      login(request, user)
      messages.success(request, 'You Have Successfully Registered!')
      return redirect('home')
  else:
    form = SignUpForm()      
    return render(request, 'register.html', {'form': form})
  
  return render(request, 'register.html', {'form': form})




@login_required
def customer_record(request, pk):
    customer_record = get_object_or_404(Record, id=pk)
    if customer_record.user == request.user:
        return render(request, 'record.html', {'customer_record': customer_record})
    else:
        messages.error(request, "You don't have permission to view this record.")
        return redirect('home')




@login_required
def delete_record(request, pk):
    delete_it = get_object_or_404(Record, id=pk)
    if delete_it.user == request.user:
        delete_it.delete()
        messages.success(request, "Record Deleted Successfully...")
    else:
        messages.error(request, "You don't have permission to delete this record.")
    return redirect('home')




@login_required
def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save(user=request.user)  # Pass the currently logged-in user to save() method
            messages.success(request, "Record Added...")
            return redirect('home')
    return render(request, 'add_record.html', {'form': form})




@login_required
def update_record(request, pk):
    current_record = get_object_or_404(Record, id=pk)

    if request.method == 'POST':
        form = AddRecordForm(request.POST, instance=current_record)
        if form.is_valid():
            # Ensure the user field is set correctly
            current_record.user = request.user
            current_record.save()
            messages.success(request, "Record has been updated successfully!")
            return redirect('home')
    else:
        form = AddRecordForm(instance=current_record)

    return render(request, 'update_record.html', {'form': form})

