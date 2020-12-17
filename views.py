from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages 
import bcrypt
# Create your views here.

def index(request):

     return render(request, 'index.html')

def register(request):
     if request.method =="POST":
          errors = User.objects.create_validator(request.POST)
          if len(errors) > 0:
               for key, value in errors.items():
                    messages.error(request, value)
               return redirect('/')
          else:
               hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
               user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=hashed_pw)
               request.session['user_id'] = user.id
               return redirect('/wishes')
               
     return redirect('/')

def login(request):
     user = User.objects.filter(email=request.POST['email'])
     if len(user) > 0:
          user = user[0]
          if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
               request.session['user_id'] = user.id
               return redirect('/wishes')
     messages.error(request, "Email or Password is incorrect")
     return redirect('/')

def wishes(request):
     if 'user_id' not in request.session:
          messages.error(request, "You need to register or log in!")
          return redirect('/')
     context = {
          'user': User.objects.get(id=request.session['user_id']),
          'wishes': Wish.objects.all()
     }
     return render(request, "wishes.html", context)

def logout(request):
     request.session.clear()
     return redirect('/')

def new_wish(request):
     if 'user_id' not in request.session:
          messages.error(request, "You need to register or log in!")
          return redirect('/')
     context = {
          'user': User.objects.get(id=request.session['user_id']),
          'wishes': Wish.objects.all()
     }

     return render(request, "makeWish.html", context)

def create_wish(request):
     if request.method =="POST":
          errors = Wish.objects.wish_validator(request.POST)
          if errors:
               for key, values in errors.items():
                    messages.error(request, values)
               return redirect('/wishes/new')
          new_wish = Wish.objects.create(name=request.POST['name'], 
          creator=User.objects.get(id=request.session['user_id']))
          print(new_wish)
          return redirect('/wishes')
     return redirect('/')

def edit(request, id):
     edit_wish = Wish.objects.get(id=id)
     context = {
          'wish': edit_wish
     }
     return render(request, 'edit.html', context)

def update(request, id):
     errors = Wish.objects.wish_validator(request.POST)
     if len(errors) > 0:
          for key, value in errors.items():
               messages.error(request, value)
          return redirect(f'/wishes/edit/{str(id)}')
     else:
          wish_update = Wish.objects.get(id=id)
          wish_update.name = request.POST['name']
          wish_update.description = request.POST['description']
          wish_update.save()

          return redirect('/wishes')
          
def delete(request, id):
     Wish.objects.get(id=id).delete()
     return redirect('/wishes')
# Create your views here.

def granted(request, id):
     user = User.objects.get(id=request.session['user_id'])
     wish = Wish.objects.get(id=id)
     user.granted.add(wish)

     return redirect('/wishes')