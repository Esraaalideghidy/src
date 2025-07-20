from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.core.exceptions import ObjectDoesNotExist



# Create your views here.

def register_customer(request):
    if request.method == 'POST':
        form=RegisterForm(request.POST)
        if form.is_valid():
            new=form.save(commit=False)
            new.is_buyer=True
            new.is_active = False
            new.save()
            #user activation
            current_site=get_current_site(request)
            mail_subject = 'Activate your account'
            message = render_to_string('account_activation_email.html', {
                'user': new,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(new.pk)),
                'token': default_token_generator.make_token(new),
            })
            print("📩 Email message content:\n", message)
          
            to_email = new.email
            send_email=EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            messages.success(request, 'Account created successfully. Please check your email to activate your account.')
            return redirect('/users/login/?command=verification&email='+to_email)


          
        else:

            print("❌ Form is not valid:", form.errors)
       
            messages.error(request, 'Error creating account')
    else:
        form=RegisterForm()
    return render(request, 'register.html', {'form': form})


def login_customer(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, 'Login successful')
                return redirect('/')
            else:
                messages.error(request, 'Your account is not active. Please check your email to activate your account.')
                return redirect('/users/login/?command=verification&email='+user.email)
        else:
            
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')

def logout_customer(request):
    logout(request)
    messages.success(request, 'Logout successful')
    return redirect('login')
# @login_required()
def contact(request):
    contact = ContactInfo.objects.all().first()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            new=form.save()
            if request.user.is_authenticated:
                new.user = request.user
            else:
                new.user = None
            new.save()
            messages.success(request, 'Message sent successfully')
            return redirect('contact')
        else:
            messages.error(request, 'Error sending message')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'contact': contact,'form': form})


def index(request):
    form = ContactForm()
    contact_info = ContactInfo.objects.first()
    return render(request, 'index.html', {'contact_info': contact_info,'form': form})



def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been activated successfully.')
        return redirect('login')
    else:
        messages.error(request, 'Activation link is invalid!')
        return redirect('register')
    

def forgotpassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if User.objects.filter(email=email):
            user=User.objects.get(email__exact=email)
            # Reset Password email
            current_site = get_current_site(request)
            mail_subject = 'Reset Your Password'
            message = render_to_string('reset_password_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            print("📩 Email message content:\n", message)

            to_email = user.email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            messages.success(request, 'Password reset email has been sent to your email address.')
            return redirect('login')
        else:
            messages.error(request, 'Email not found')
            return redirect('forgotpassword')

    return render(request, 'forgotpassword.html')




def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password.')
        return redirect('resetpassword')
        
    else:
        messages.error(request, 'The reset link is invalid!')
        return redirect('login')
    



def resetpassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return redirect('resetpassword')

        uid = request.session.get('uid')
        if uid is None:
            messages.error(
                request, 'Session expired or invalid reset request.')
            return redirect('login')

        try:
            user = User.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(
                request, 'Your password has been reset successfully.')
            return redirect('login')
        except ObjectDoesNotExist:
            messages.error(request, 'User not found.')
            return redirect('resetpassword')
    return render(request, 'resetpassword.html')
