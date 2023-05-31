import datetime
from datetime import *

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from gearStore.forms import UserForm, UserProfileForm, CategoryForm, GearForm, AdminForm
from gearStore.models import UserProfile, Category, Gear, Booking, AdminPassword

import hashlib

# Create your views here.
def index(request):
    context_dict = {'categories': Category.objects.all()}
    context_dict['categories'] = Category.objects.all()
    context_dict['category'] = None
    return render(request, 'gearStore/index.html', context_dict)


def view_category(request, category_name_slug):
    context_dict = {'categories': Category.objects.all()}
    context_dict['categories'] = Category.objects.all()
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        # Redirect to home page if category doesn't exist
        return redirect(reverse("gearStore:index"))
    context_dict["category"] = category
    context_dict["gear_list"] = Gear.object.filter(category=category)
    return render(request, 'gearStore/category.html', context=context_dict)


def register(request):
    context_dict = {'categories': Category.objects.all()}
    context_dict['category'] = None
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = UserProfile()
            profile.user = user
            profile.save()
            registered = True
        else:
            print("")
            print(user_form.errors)
    else:
        user_form = UserForm()

    if registered:
        return render(request, 'gearStore/login.html', context=context_dict)

    else:
        errorList = []
        for error_category in user_form.errors:
            for error in user_form.errors[error_category]:
                errorList.append(error)
        context_dict['errors'] = errorList
        context_dict['user_form'] = user_form
        context_dict['registered'] = registered

        return render(request, 'gearStore/register.html', context=context_dict)


def login_page(request):
    context_dict = {'categories': Category.objects.all()}
    context_dict['category'] = None
    errorList = []
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('gearStore:index'))
            else:
                errorList.append("Account has been disabled due to inactivity. Please create a new account.")
        else:
            print(f"Invalid login details: {username}, {password}")
            errorList.append("Invalid combination of user and password.")
        context_dict['errors'] = errorList
        return render(request, 'gearStore/login.html', context=context_dict)
    else:
        return render(request, 'gearStore/login.html', context=context_dict)


def about(request):
    context_dict = {'categories': Category.objects.all()}
    context_dict['category'] = None
    return render(request, 'gearStore/about.html', context_dict)


def contact(request):
    context_dict = {'categories': Category.objects.all()}
    context_dict['category'] = None
    return render(request, 'gearStore/contact.html', context_dict)


def category_menu(request):
    context_dict = {'categories': Category.objects.all()}
    context_dict['admin'] = False
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        if user_profile:
            if user_profile.adminStatus:
                context_dict['admin'] = True

    context_dict['category'] = None
    return render(request, 'gearStore/category_menu.html', context_dict)


def view_gear(request, gear_name_slug):
    context_dict = {'categories': Category.objects.all()}

    try:
        gear = Gear.objects.get(slug=gear_name_slug)
        context_dict['category'] = gear.category
        context_dict['gear'] = gear

        # attempt to borrow the gear
        if request.method == 'POST':
            borrow = Booking()
            if request.user:
                borrow.gearItem = gear
                borrow.user = UserProfile.objects.get(user=request.user)
                borrow.dateToReturn = datetime.now().date() + timedelta(days=14)
                borrow.save()

        # find if the gear is currently on loan
        current_borrow = False
        borrows = Booking.objects.filter(gearItem=gear)
        for borrow in borrows:
            if borrow.is_current():
                current_borrow = True
                context_dict["borrow"] = borrow
                break
        context_dict['borrowed'] = current_borrow

        # find the gear's category
        try:
            category = Category.objects.get(name=gear.category)
            context_dict['category'] = category
        except Category.DoesNotExist:
            context_dict['category'] = None
    except Gear.DoesNotExist:
        context_dict['gear'] = None
    return render(request, 'gearStore/view_gear.html', context_dict)


@login_required
def account(request):
    context_dict = {'categories': Category.objects.all()}
    context_dict['category'] = None
    user_profile = UserProfile.objects.get(user=request.user)
    context_dict['user_profile'] = user_profile
    passwords = AdminPassword.objects.all()
    if not passwords:
        user_profile.adminStatus = True
    password_form = AdminForm()
    picture_form = UserProfileForm()

    if request.method == "POST":
        # check picture
        if request.FILES:
            picture_form = UserProfileForm(request.POST or None, request.FILES, instance=user_profile)
            if picture_form.is_valid():
                picture_form.save()
        # check password
        if request.POST.get("password"):
            password_form = AdminForm(request.POST)
            if password_form.is_valid():
                if not passwords:
                    password = password_form.save(commit=True)
                    passwords = AdminPassword.objects.all()

                    input_password = request.POST.get("password")
                    plaintext = input_password.encode()
                    hash = hashlib.sha256(plaintext)
                    readable_hash = hash.hexdigest()

                    passwords[0].password = readable_hash
                    passwords[0].save()

                    user_profile.adminStatus = True
                    user_profile.save()
                elif user_profile.adminStatus:
                    input_password = request.POST.get("password")
                    plaintext = input_password.encode()
                    hash = hashlib.sha256(plaintext)
                    readable_hash = hash.hexdigest()

                    passwords[0].password = readable_hash
                    passwords[0].save()
                else:
                    input_password = request.POST.get("password")
                    plaintext = input_password.encode()
                    hash = hashlib.sha256(plaintext)
                    readable_hash = hash.hexdigest()

                    if passwords[0].password == readable_hash:
                        user_profile.adminStatus = True
                        user_profile.save()
    context_dict['picture_form'] = picture_form
    context_dict['password_form'] = password_form

    user_bookings = Booking.objects.filter(user=user_profile)
    for booking in user_bookings:
        if not booking.is_current():
            user_bookings = user_bookings.exclude(id = booking.id)
    context_dict["user_bookings"] = user_bookings

    if user_profile.adminStatus:
        all_bookings = Booking.objects.all()
        for booking in all_bookings:
            if not booking.is_current():
                all_bookings = all_bookings.exclude(id = booking.id)
        context_dict["all_bookings"] = all_bookings

    return render(request, 'gearStore/account.html', context_dict)


@login_required
def process_logout(request):
    context_dict = {'categories': Category.objects.all()}
    context_dict['category'] = None
    logout(request)
    return redirect(reverse('gearStore:index'))


def admin_error(request):
    context_dict = {'categories': Category.objects.all()}
    context_dict['category'] = None
    return render(request, 'gearStore/admin_error.html', context=context_dict)


def view_category(request, category_name_slug):
    context_dict = {'categories': Category.objects.all()}

    context_dict['admin'] = False
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        if user_profile:
            if user_profile.adminStatus:
                context_dict['admin'] = True

    try:
        category = Category.objects.get(slug=category_name_slug)

        gear = Gear.objects.filter(category=category)
        context_dict['gear'] = gear
        context_dict['category'] = category

        # calculate numbers total and available
        num_total = len(gear)
        num_available = num_total
        for gear_item in gear:
            borrows = Booking.objects.filter(gearItem=gear_item)
            for borrow in borrows:
                if borrow.is_current():
                    num_available -= 1

        context_dict['available'] = num_available
        context_dict['total'] = num_total
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['gear'] = None
    return render(request, 'gearStore/category.html', context=context_dict)


@login_required
def add_category(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if not user_profile.adminStatus:
        return redirect(reverse("gearStore:admin-error"))
    errorList = []
    context_dict = {'categories': Category.objects.all()}
    form = None
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('/gear-store/')
        else:
            print(form.errors)
            for error_category in form.errors:
                for error in form.errors[error_category]:
                    errorList.append(error)
    context_dict['errors'] = errorList
    context_dict['form'] = form
    return render(request, 'gearStore/add_category.html', context_dict)


@login_required
def add_gear(request, category_name_slug):
    user_profile = UserProfile.objects.get(user=request.user)
    if not user_profile.adminStatus:
        return redirect(reverse("gearStore:admin-error"))
    context_dict = {'categories': Category.objects.all()}
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    if category is None:
        return redirect(reverse("gearStore:index"))

    form = GearForm()

    if request.method == 'POST':
        form = GearForm(request.POST, request.FILES)

        if form.is_valid():
            if category:
                gear = form.save(commit=False)
                gear.category = category
                gear.save()
                return redirect(reverse('gearStore:view-category',
                                        kwargs={'category_name_slug': category_name_slug}))
        else:
            print(form.errors)
    context_dict['form'] = form
    context_dict['category'] = category
    return render(request, 'gearStore/add_gear.html', context=context_dict)

@login_required
def edit_category(request, category_name_slug):
    user_profile = UserProfile.objects.get(user=request.user)
    if not user_profile.adminStatus:
        return redirect(reverse("gearStore:admin-error"))
    context_dict = {'categories': Category.objects.all()}
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Gear.DoesNotExist:
        category = None

    if category is None:
        return redirect(reverse("gearStore:index"))

    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)

        if form.is_valid():
            if category:
                category = form.save(commit=False)
                category.save()
                return redirect(reverse('gearStore:view-category',
                                        kwargs={'category_name_slug': category_name_slug}))
        else:
            print(form.errors)
    context_dict['form'] = form
    return render(request, 'gearStore/edit_category.html', context=context_dict)

@login_required
def edit_gear(request, category_name_slug, gear_name_slug):
    user_profile = UserProfile.objects.get(user=request.user)
    if not user_profile.adminStatus:
        return redirect(reverse("gearStore:admin-error"))
    context_dict = {'categories': Category.objects.all()}
    try:
        gear = Gear.objects.get(slug=gear_name_slug)
    except Gear.DoesNotExist:
        gear = None

    if gear is None:
        return redirect(reverse("gearStore:index"))

    form = GearForm()

    if request.method == 'POST':
        form = GearForm(request.POST or None, request.FILES or None, instance=gear)

        if form.is_valid():
            if gear:
                gear = form.save()
                # gear.name = request.POST.get("name")
                # gear.description = request.POST.get("description")
                # gear.size = request.POST.get("size")
                # gear.save()
                return redirect(reverse('gearStore:view-gear',
                                        kwargs={'gear_name_slug': gear.slug}))
        else:
            print(form.errors)
    context_dict['form'] = form
    context_dict['gear'] = gear
    context_dict['category'] = gear.category
    return render(request, 'gearStore/edit_gear.html', context=context_dict)
