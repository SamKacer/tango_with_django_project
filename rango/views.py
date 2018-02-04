from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse 
from rango.models import Category, Page, User, UserProfile
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.contrib.auth.decorators import login_required

def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {"categories" : category_list,
        "pages" : page_list}
    return render(request, 'rango/index.html', context = context_dict)

def about(request):
    context_dict = {}
    return render(request, 'rango/about.html', context = context_dict)

def show_category(request, category_name_url):
    context_dict ={}
    try:
        category = Category.objects.get(slug = category_name_url)
        pages = Page.objects.filter(category = category)
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['pages'] = None
        context_dict['category'] = None

    return render(request, 'rango/category.html', context_dict)

@login_required
def add_category(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        
        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print(form.errors)
    
    return render(request, 'rango/add_category.html', {'form' : form})

@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None
    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return show_category(request, category_name_slug)
        else:
            print(form.errors)
    context_dict = {'form':form, 'category': category}
    return render(request, 'rango/add_page.html', context_dict)

def register(request):
    # tracks if registration was successful 
    registered = False
    #process data if http post
    if request.method == 'POST':
        #grab data from form
        user_form = UserForm(data = request.POST)
        profile_form = UserProfileForm(data=request.POST)
        # if the forms are valid
        if user_form.is_valid() and profile_form.is_valid():
            # save the data to database
            user = user_form.save()
            # hash the password and update user object
            user.set_password(user.password)
            user.save()# sort out user profile
            profile = profile_form.save(commit=False)
            profile.user = user
            #check if user specified picture
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            #  save profile model instance and update 'registered' variable
            profile.save()
            registered = True
        else: # forms invalid 
            # print errors to console
            print(user_form.errors, profile_form.errors)
    else: # request isnt POST
        # so render form using blank form instances
        user_form = UserForm()
        profile_form = UserProfileForm()
    
    return render(request,
        'rango/register.html',
        {'user_form' : user_form,
        'profile_form' : profile_form,
        'registered' : registered})

def user_login(request):
    # if request is post pull out data
    if request.method == 'POST':
        # pull username and password from form
        username = request.POST.get('username')        
        password = request.POST.get('password')        
        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username = username, password = password)
        if user: # check if user exists 
            if user.is_active:             # check if user is active
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else: # inactive user
                return HttpResponse("Your Rango account is disabled.")
        else: # invalid user details provided 
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("invalid login details.")
    else: # request is not post
        return  render(request, 'rango/login.html', {})

@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")

@login_required
def user_logout(request):
    # since user is logged in we can just log them out
    logout(request)
    # redirect to index 
    return HttpResponseRedirect(reverse('index'))
