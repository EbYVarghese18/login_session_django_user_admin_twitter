from django.shortcuts import redirect, render
from django.contrib.auth import authenticate
from django.views.decorators.cache import cache_control
from django.contrib import messages
# from .models import users_table
from django.contrib.auth.models import User


# Create your views here.


# user view starts

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def register(request):
    if 'usersession' in request.session:
        return redirect('welcome')
    if request.method == 'POST':
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_name = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirmpassword']
        if password == confirm_password:
            if User.objects.filter(username=user_name).exists():
                messages.info(request, 'Username Taken !')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken !')
                return redirect('register')
            else:
                user = User.objects.create_user(
                    first_name=first_name, last_name=last_name, username=user_name, password=password, email=email)
                user.save()
                messages.info(request, 'User created succesfully')
                return redirect('signin')
        else:
            messages.info(request, 'Password not matching !')
            return redirect('register')
    else:
        return render(request, 'signup.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def signin(request):
    if 'usersession' in request.session:
        return redirect('welcome')
    if request.method == 'POST':
        username = request.POST['userName']
        password = request.POST['passWord']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_superuser:
                messages.info(request, 'Try with user account!')
                return redirect('signin')
            else:
                request.session['usersession'] = username  # creating session
                return redirect('welcome')
        else:
            messages.info(request, 'Invalid credentials!')
            return render(request, 'signin.html')
    else:
        return render(request, 'signin.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def welcome(request):
    if 'usersession' in request.session:
        return render(request, 'welcome.html')
    return redirect('signin')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def signout(request):
    if 'usersession' in request.session:
        try:
            del request.session['usersession']
            return redirect('signin')
        except KeyError:
            pass


#
#
# admin view starts
#
#


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def adminsignin(request):
    if 'adminsession' in request.session:
        return redirect('adminhome')
    if request.method == 'POST':
        username = request.POST['userName']
        password = request.POST['passWord']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_superuser:
                request.session['adminsession'] = username  # creating session
                return redirect('adminhome')
            else:
                messages.info(request, 'Try with admin account!')
                return render(request, 'admin_signin.html')
        else:
            messages.info(request, 'Invalid credentials!')
            return render(request, 'admin_signin.html')
    else:
        return render(request, 'admin_signin.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def adminhome(request):
    if 'adminsession' in request.session:
        args = {
            'users': User.objects.all()
        }
        return render(request, 'admin_home.html', args)
    else:
        return redirect('adminsignin')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def adduser(request):
    if 'adminsession' in request.session:
        if request.method == 'POST':
            first_name = request.POST['firstname']
            last_name = request.POST['lastname']
            user_name = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            if User.objects.filter(username=user_name).exists():
                messages.info(request, 'Username Taken !')
                return redirect('adduser')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken !')
                return redirect('adminhome')
            else:
                user = User.objects.create_user(
                    first_name=first_name, last_name=last_name, username=user_name, password=password, email=email)
                user.save()
                messages.success(request, 'The user created succesfully')
                return redirect('adminhome')
        else:
            return render(request, 'admin_adduser.html')
    else:
        return redirect('adminsignin')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def deleteuser(request, username):
    if 'usersession' in request.session:
        try:
            del request.session['usersession']
        except KeyError:
            pass
    try:
        u = User.objects.get(username=username)
        u.delete()
        messages.success(request, "The user is deleted")
        return redirect('adminhome')
    except:
        pass


def edituser(request, id):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        updateuser = User.objects.get(id=id)
        updateuser.first_name = firstname
        updateuser.last_name = lastname       
        updateuser.username = username
        updateuser.email = email
        updateuser.save()
        messages.success(request, "User updated successfully")
        return redirect('adminhome')
    else:
        user = User.objects.get(id=id)
        args = {
            'users': user
            }
        return render(request, "admin_edituser.html", args)


def searchuser(request):
    username=request.GET['searchuser']
    searchuser = User.objects.filter(username__contains=username)
    return render(request,"admin_searchuser.html",{
        'users':searchuser
        })


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def adminsignout(request):
    if 'adminsession' in request.session:
        try:
            del request.session['adminsession']
            return redirect('adminsignin')
        except KeyError:
            pass