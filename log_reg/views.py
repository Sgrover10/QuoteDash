from django.shortcuts import render, redirect
from django.contrib import messages
from log_reg.models import User, Quote


def index(request):
    return render(request, 'login.html')

def register(request):
    if request.method=='GET':
        return redirect('/')
        ##validate the data
    errors=User.objects.validator(request.POST)
    if errors:
        for error in errors:
            messages.error(request, errors[error])
        return redirect('/')
    else:
        new_user = User.objects.register(request.POST)
        request.session['user_id']=new_user.id
        messages.success(request, "You have successfully registered!")
        return redirect('/quotes')

def login(request):
    if request.method=='GET':
        return redirect('/')
    if not User.objects.authenticate(request.POST['email'], request.POST['pw']):
        messages.error(request, 'Invalid Email/Password')
        return redirect('/')
    user = User.objects.get(email=request.POST['email'])
    request.session['user_id'] = user.id
    messages.success(request, "You have successfully logged in!")
    return redirect('/quotes')

def logout(request):
    request.session.clear()
    return redirect('/')

def all_quotes(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user=User.objects.get(id=request.session['user_id'])
    context={
        'user': user,
        'all_quotes': Quote.objects.all()
    }
    return render(request, "dashboard.html", context)

def add_quote(request):
    if request.method=='POST':
        error=Quote.objects.quote_validator(request.POST)
        if error:
            messages.error(request, error)
            return redirect('/quotes')
        Quote.objects.create(
            author=request.POST['author'],
            quote=request.POST['quote'],
            poster=User.objects.get(id=request.session['user_id'])
        )
        return redirect('/quotes')
    return redirect('/quotes')


def user_page(request, poster_id):
    ##get user
    user=User.objects.get(id=poster_id)
    context = {
        'user':User.objects.get(id=poster_id),
        'user_quotes': user.quotes.all()
    }
    return render(request, 'profile.html', context)

def edit_user(request, user_id):
    edit_user=User.objects.get(id=user_id)
    if request.method=='POST':
        errors=User.objects.edit_user_validator(request.POST)
        if errors:
            for error in errors:
                messages.error(request, errors[error])
            return redirect(f'/myaccount/{str(edit_user.id)}')
        else:
            edit_user=User.objects.get(id=user_id)
            edit_user.first_name=request.POST['fname']
            edit_user.last_name=request.POST['lname']
            edit_user.email=request.POST['email']
            edit_user.save()
            return redirect(f'/myaccount/{str(edit_user.id)}')
    context={
        'edit_user':User.objects.get(id=user_id)
    }
    return render(request, 'edit_user.html', context)


def like(request, quote_id):
    if request.method=="POST":
        liked_quote=Quote.objects.get(id=quote_id)
        user_liking=User.objects.get(id=request.session['user_id'])
        liked_quote.likes.add(user_liking)
        return redirect('/quotes')
    return redirect('/quotes')
    

def unlike(request, quote_id):
    if request.method=="POST":
        unliked_quote=Quote.objects.get(id=quote_id)
        user_unliking=User.objects.get(id=request.session['user_id'])
        unliked_quote.likes.remove(user_unliking)
        return redirect('/quotes')
    return redirect('/quotes')

def edit_quote(request, quote_id):
    edit_quote=Quote.objects.get(id=quote_id)
    
    if request.method=='POST':
        error=Quote.objects.quote_validator(request.POST)
        if error:
            messages.error(request, error)
            return redirect(f'/{str(edit_quote.id)}/edit_quote')
        else:
            edit_quote=Quote.objects.get(id=quote_id)
            edit_quote.author=request.POST['author']
            edit_quote.quote=request.POST['quote']
            edit_quote.save()
            return redirect('/quotes')
    context={
        'edit_quote':Quote.objects.get(id=quote_id)
    }
    return render(request, 'edit_quote.html', context)

def delete_quote(request, quote_id):
    Quote.objects.get(id=quote_id).delete()
    return redirect('/quotes')

