from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Donation, Message
from .forms import UserUpdateForm, ProfileUpdateForm
from django.contrib.auth import logout
from .models import Profile
from user.models import SystemMessage
from django.utils import timezone
from django import forms
from .models import NGO, Donation
from .forms import NGORegistrationForm, UserUpdateForm, ProfileUpdateForm


def home(request):
    return render(request, "home.html")


def register(request): 
    if request.method == 'POST':
        username = request.POST['username']
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        mobile_number = request.POST['mobile_number']

       
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error_message': 'Username already exists.'})

        try:
           
            user = User.objects.create_user(username=username, email=email, password=password, first_name=name)
            user.save()

        
            user.profile.mobile_number = mobile_number
            user.profile.save()

            
            return redirect('login')

        except Exception as e:
            return render(request, 'register.html', {'error_message': f'Error occurred: {str(e)}'})

    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
         
            return redirect('donate') 
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'login.html')


@login_required
def donate(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
    
        donation_made = False

    
        medicine_quantity = request.POST.get('medicine_quantity')
        if medicine_quantity:
            try:
                quantity = int(medicine_quantity)
                donation = Donation(
                    user=request.user,
                    item_name="Medicines",
                    quantity=quantity,
                    description=request.POST.get('medicine_description'),
                    image=request.FILES.get('medicine_image'),
                    mfg_date=request.POST.get('mfg_date') or None,
                    exp_date=request.POST.get('exp_date') or None,
                    address=address,
                    date_donated=timezone.now()
                )
                donation.save()
                donation_made = True
            except ValueError:
                pass  

    
        clothes_quantity = request.POST.get('clothes_quantity')
        if clothes_quantity:
            try:
                quantity = int(clothes_quantity)
                donation = Donation(
                    user=request.user,
                    item_name="Clothes",
                    quantity=quantity,
                    description=request.POST.get('clothes_description'),
                    image=request.FILES.get('clothes_image'),
                    address=address, 
                    date_donated=timezone.now()
                )
                donation.save()
                donation_made = True
            except ValueError:
                pass

        books_quantity = request.POST.get('books_quantity')
        if books_quantity:
            try:
                quantity = int(books_quantity)
                donation = Donation(
                    user=request.user,
                    item_name="Books",
                    quantity=quantity,
                    description=request.POST.get('books_description'),
                    image=request.FILES.get('books_image'),
                    address=address,
                    date_donated=timezone.now()
                )
                donation.save()
                donation_made = True
            except ValueError:
                pass

       
        toys_quantity = request.POST.get('toys_quantity')
        if toys_quantity:
            try:
                quantity = int(toys_quantity)
                donation = Donation(
                    user=request.user,
                    item_name="Toys",
                    quantity=quantity,
                    description=request.POST.get('toys_description'),
                    image=request.FILES.get('toys_image'),
                    address=address,
                    date_donated=timezone.now()
                )
                donation.save()
                donation_made = True
            except ValueError:
                pass

    
        if donation_made:

           pass 
        else:
            try:
                warning_msg = Message.objects.get(message_type='donation_warning').content
            except Message.DoesNotExist:
                warning_msg = "Please fill at least one donation type before submitting."
            messages.warning(request, warning_msg)

        return redirect('donation_history')

    return render(request, "donate.html")
    
@login_required
def donation_history(request):
    donations = Donation.objects.filter(user=request.user).order_by('-date_donated')
    return render(request, 'donation_history.html', {'donations': donations})

@login_required
def edit_profile(request):
    profile = Profile.objects.get(user=request.user)
    
    if request.method == 'POST':
        mobile_number = request.POST.get('mobile_number')
        profile.mobile_number = mobile_number
        profile.save()
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('edit_profile')  
    
    return render(request, 'edit_profile.html', {'profile': profile})
 
def logout_view(request):
    logout(request)
    return redirect('login')  

def ngo_register(request):
    if request.method == 'POST':
        organization_name = request.POST.get('organization_name')
        email = request.POST.get('email')
        contact_person = request.POST.get('contact_person')
        contact_number = request.POST.get('contact_number')
        address = request.POST.get('address')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

      
        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect('ngo_register')

       
        if User.objects.filter(email=email).exists():
            messages.error(request, "An account with this email already exists!")
            return redirect('ngo_register')

        user = User.objects.create_user(username=email, email=email, password=password1)

     
        ngo = NGO.objects.create(
            user=user,
            organization_name=organization_name,
            contact_person=contact_person,
            contact_number=contact_number,
            address=address,
            email=email
        )

        messages.success(request, "NGO registered successfully! Please log in.")
        return redirect('ngo_login')

    return render(request, 'ngo_register.html')

        
from django.contrib import messages

def ngo_login(request):
    if request.method == 'POST':
        identifier = request.POST.get('username') 
        password = request.POST.get('password')

     
        user = authenticate(request, username=identifier, password=password)

       
        if user is None and User.objects.filter(email=identifier).exists():
            user = User.objects.get(email=identifier)
            user = authenticate(request, username=user.username, password=password)

        if user is not None:
            ngo = NGO.objects.filter(user=user).first()  
            if ngo:
                login(request, user)
                return redirect('ngo_dashboard')  
            else:
                messages.error(request, "You are not associated with any NGO.")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'ngo_login.html')



@login_required
def ngo_dashboard(request):
    try:
        ngo = request.user.ngo  
        assigned_donations = Donation.objects.filter(assigned_ngo=ngo).select_related('user')

        for donation in assigned_donations:
            
            donation.address = donation.address if donation.address else "Not Provided"
            donation.phone = donation.user.profile.mobile_number if hasattr(donation.user, 'profile') and donation.user.profile.mobile_number else "Not Provided"

        return render(request, 'ngo_dashboard.html', {
            'assigned_donations': assigned_donations
        })

    except AttributeError:
        messages.error(request, "You need to be registered as an NGO to access this page")
        return redirect('ngo_home')


def ngo_home(request):
    """
    NGO portal home page
    """
    
    if request.user.is_authenticated and hasattr(request.user, 'ngo'):
        return redirect('ngo_dashboard')
    
    return render(request, 'ngo_home.html')