from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import User

# def login(request):
#     return render(request, 'login/Login.html')


# def user_login(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')

#         if email and password:
#             user = authenticate(request, username=email, password=password)

#             if user is not None:
#                 login(request, user)
#                 return redirect('product_list')  # Redirect to the product listing page

#     return render(request, 'login/Login.html')

@login_required
def success(request):
    return render(request, 'product/product-listing.html')

def registerPage(request): 
    try:    
        if request.method =='POST':
            form_data = request.POST
            name = form_data.get('full_name')
            email = form_data.get('email')
            phone_number = form_data.get('phone')
            password = form_data.get('password')
            repassword = form_data.get('re-password')
            print(form_data.dict())
            
            
            if password == repassword:
                print(name,email,phone_number,password,repassword)
                user_instance = User(name=name, email=email, password=password,phone=phone_number)
                user_instance.save()
                return redirect('product:product_list')
            else:
                return render(request, "login/success.html",{'message':"Password and Re-Password are not same"})
    except:
        return render(request, "login/Login.html",{'message':"Email already exists"})
    
    return render(request, "login/Login.html")
def user_login(request):
    if request.method =='POST':
        try:
            email = request.POST.get('email')
            password = request.POST.get('password')
            print(email,password)   
            user = verify_user(request, email=email, password=password,entity=User)
            request.session['id'] = user.id
            id = request.session.get('id')
            print("Session ka ",id)
            print("login ka ",user)
            print(user.id)
            print(user.name)
            if user :
                # login(request, user)
                print("idar  aaya aayaa par kch ni hua")  
                print(user.name)
                request.session['name'] = user.name
                request.session['id'] = user.id
                return redirect('product_list')  # Replace with the appropriate URL
            else:
                # Authentication failed
                print("Fail")
                message = 'Incorrect email or password. Please try again.'
                return render(request, 'login/Login.html',{'message': message})
        except:
            pass
            message="Pls Enter Password"
            print("User not Registered")
            return render(request, 'login/Login.html',{'message': message})
    
    print('login')
    return render(request, 'login/Login.html')
def verify_user(request, email=None, password=None, entity=None):
        try:
            user = entity.objects.get(email=email)
            print("I'm from Verify_User func  ",str(user) )
            print(user.email,user.password)
            if password == user.password:
                print("pass match")
                return user
            else:
                return False
        except:
            return False
  