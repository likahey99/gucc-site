import datetime
from datetime import *

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from gearStore.forms import UserForm, UserProfileForm, CategoryForm, GearForm, AdminForm, PageContentsForm, \
    BackgroundImageForm, LogoImageForm, BookingCommentsForm
from gearStore.models import UserProfile, Category, Gear, Booking, AdminPassword, BookingComments, PageContents, \
    CONTACT_CHOICES

from django.template.defaultfilters import slugify

import hashlib


# Create your views here.
def index(request):
    context_dict = {'categories': Category.objects.all()}
    content = PageContents.objects.all()
    if content:
        content = content[0]
    context_dict['category'] = None
    context_dict['content'] = content

    context_dict['admin'] = False
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        if user_profile:
            if user_profile.adminStatus:
                context_dict['admin'] = True

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
            profile.first_name = request.POST.get('first_name')
            profile.last_name = request.POST.get('last_name')
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
        errors = []
        for error_category in user_form.errors:
            for error in user_form.errors[error_category]:
                errors.append(error)
        context_dict['errors'] = errors
        context_dict['user_form'] = user_form
        context_dict['registered'] = registered

        return render(request, 'gearStore/register.html', context=context_dict)


def login_page(request):
    context_dict = {'categories': Category.objects.all()}
    context_dict['category'] = None
    errors = []
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('gearStore:index'))
            else:
                errors.append("Account has been disabled due to inactivity. Please create a new account.")
        else:
            print(f"Invalid login details: {username}, {password}")
            errors.append("Invalid combination of user and password.")
        context_dict['errors'] = errors
        return render(request, 'gearStore/login.html', context=context_dict)
    else:
        return render(request, 'gearStore/login.html', context=context_dict)


def about(request):
    context_dict = {'categories': Category.objects.all()}
    content = PageContents.objects.all()
    if content:
        content = content[0]
    context_dict['category'] = None
    context_dict['content'] = content

    context_dict['admin'] = False
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        if user_profile:
            if user_profile.adminStatus:
                context_dict['admin'] = True

    return render(request, 'gearStore/about.html', context_dict)


def contact(request):
    context_dict = {'categories': Category.objects.all()}
    content = PageContents.objects.all()
    if content:
        content = content[0]
    context_dict['category'] = None
    context_dict['content'] = content

    context_dict['admin'] = False
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        if user_profile:
            if user_profile.adminStatus:
                context_dict['admin'] = True

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

    context_dict['admin'] = False
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        if user_profile:
            if user_profile.adminStatus:
                context_dict['admin'] = True

    return render(request, 'gearStore/view_gear.html', context_dict)


@login_required
def account(request):
    context_dict = {'categories': Category.objects.all()}
    context_dict['category'] = None
    user_profile = UserProfile.objects.get(user=request.user)
    context_dict['user_profile'] = user_profile
    passwords = AdminPassword.objects.all()
    context_dict['nopass'] = False
    if not passwords:
        context_dict['nopass'] = True
    password_form = AdminForm()
    picture_form = UserProfileForm()
    context_dict['form_open'] = False
    errors = []
    if request.method == "POST":
        print("post")
        context_dict['form_open'] = True
        # check picture
        if request.FILES:
            picture_form = UserProfileForm(request.POST or None, request.FILES, instance=user_profile)
            if picture_form.is_valid():
                picture_form.save()
            else:
                print(picture_form.errors)
                for error_category in picture_form.errors:
                    for error in picture_form.errors[error_category]:
                        errors.append(error)

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
                    else:
                        errors.append("Error: Could not become admin - incorrect password.")
            else:
                print(picture_form.errors)
                for error_category in picture_form.errors:
                    for error in picture_form.errors[error_category]:
                        errors.append(error)

        if request.POST.get("first_name"):
            user_profile.first_name = request.POST.get("first_name")
            user_profile.save()

        if request.POST.get("last_name"):
            user_profile.last_name = request.POST.get("last_name")
            user_profile.save()

    context_dict['picture_form'] = picture_form
    context_dict['password_form'] = password_form

    user_bookings = Booking.objects.filter(user=user_profile)
    for booking in user_bookings:
        if not booking.is_current():
            user_bookings = user_bookings.exclude(id=booking.id)
    context_dict["user_bookings"] = user_bookings

    if user_profile.adminStatus:
        all_bookings = Booking.objects.all()
        for booking in all_bookings:
            if not booking.is_current():
                all_bookings = all_bookings.exclude(id=booking.id)
        context_dict["all_bookings"] = all_bookings
    context_dict['errors'] = errors
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
    errors = []
    context_dict = {'categories': Category.objects.all()}
    form = None
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect(reverse('gearStore:find-gear'))
        else:
            print(form.errors)
            for error_category in form.errors:
                for error in form.errors[error_category]:
                    errors.append(error)
    context_dict['errors'] = errors
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
        errors = []
        if form.is_valid():
            if category:
                gear = form.save(commit=False)
                gear.category = category
                gear.save()
                return redirect(reverse('gearStore:view-category',
                                        kwargs={'category_name_slug': category_name_slug}))
        else:
            print(form.errors)
            for error_category in form.errors:
                for error in form.errors[error_category]:
                    errors.append(error)
        context_dict['errors'] = errors
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
        form = CategoryForm(request.POST or None, request.FILES or None, instance=category)
        errors = []

        if form.is_valid():
            new_slug = slugify(request.POST.get("name"))
            if category_name_slug != new_slug:
                try:
                    existing_obj = Category.objects.get(slug=new_slug)
                except Category.DoesNotExist:
                    existing_obj = None
                if not existing_obj:
                    category = form.save()
                    return redirect(reverse('gearStore:view-category',
                                            kwargs={'category_name_slug': category.slug}))
                else:
                    errors.append("Error: Category name already exists.")

        else:
            print(form.errors)
            for error_category in form.errors:
                for error in form.errors[error_category]:
                    errors.append(error)
        context_dict['errors'] = errors
    category = Category.objects.get(slug=category_name_slug)
    context_dict['category'] = category
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
        errors = []
        if form.is_valid():
            new_slug = slugify(request.POST.get("name"))
            if gear_name_slug != new_slug:
                try:
                    existing_obj = Gear.objects.get(slug=new_slug)
                except Gear.DoesNotExist:
                    existing_obj = None
                if not existing_obj:
                    gear = form.save()
                    return redirect(reverse('gearStore:view-gear',
                                            kwargs={'gear_name_slug': gear.slug}))
                else:
                    errors.append("Error: Gear name already exists.")
        else:
            print(form.errors)
            for error_category in form.errors:
                for error in form.errors[error_category]:
                    errors.append(error)
        context_dict['errors'] = errors

    gear = Gear.objects.get(slug=gear_name_slug)

    context_dict['form'] = form
    context_dict['gear'] = gear
    context_dict['category'] = gear.category
    return render(request, 'gearStore/edit_gear.html', context=context_dict)


@login_required
def delete_gear(request, category_name_slug, gear_name_slug):
    # check if user is admin
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

    if request.method == 'POST':
        errors = []
        input_password = request.POST.get("password")
        plaintext = input_password.encode()
        hash = hashlib.sha256(plaintext)
        readable_hash = hash.hexdigest()
        passwords = AdminPassword.objects.all()
        if passwords[0].password == readable_hash:
            gear.delete()
            return redirect(reverse('gearStore:view-category',
                                    kwargs={'category_name_slug': gear.category.slug}))
        else:
            errors.append("Error: Incorrect Password.")
        context_dict['errors'] = errors
    context_dict['gear'] = gear
    context_dict['category'] = gear.category
    return render(request, 'gearStore/delete_gear.html', context=context_dict)


@login_required
def delete_category(request, category_name_slug):
    # check if user is admin
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

    if request.method == 'POST':
        errors = []
        input_password = request.POST.get("password")
        plaintext = input_password.encode()
        hash = hashlib.sha256(plaintext)
        readable_hash = hash.hexdigest()
        passwords = AdminPassword.objects.all()
        if passwords[0].password == readable_hash:
            category.delete()
            return redirect(reverse('gearStore:find-gear'))
        else:
            errors.append("Error: Incorrect Password.")
        context_dict['errors'] = errors
    context_dict['category'] = category
    return render(request, 'gearStore/delete_category.html', context=context_dict)


@login_required
def edit_home(request):
    # check if user is admin
    user_profile = UserProfile.objects.get(user=request.user)
    if not user_profile.adminStatus:
        return redirect(reverse("gearStore:admin-error"))

    # add categories into the context dict for left sidebar
    context_dict = {'categories': Category.objects.all()}
    context_dict['category'] = None

    # add page content into context dict for form autofill
    content = PageContents.objects.all()
    if content:
        content = content[0]
    else:
        context_dict['content'] = None
        return render(request, 'gearStore/index.html', context=context_dict)

    if request.method == 'POST':
        errors = []

        if request.POST.get("site-title"):
            content.title = request.POST.get("site-title")

        if request.POST.get("home-text"):
            content.home_contents = request.POST.get("home-text")

            content = content.save()

        if request.FILES:
            # update background-image
            content = PageContents.objects.all()
            if content:
                content = content[0]
            form = BackgroundImageForm(request.POST or None, request.FILES, instance=content)
            if form.is_valid():
                content = form.save()
                print(content.background_image)
            else:
                print(errors)
                for error_category in form.errors:
                    for error in form.errors[error_category]:
                        errors.append(error)
            # update logo image
            content = PageContents.objects.all()
            if content:
                content = content[0]
            form = LogoImageForm(request.POST or None, request.FILES, instance=content)
            if form.is_valid():
                content = form.save()
                print(content.logo_image)
            else:
                print(errors)
                for error_category in form.errors:
                    for error in form.errors[error_category]:
                        errors.append(error)
        context_dict['errors'] = errors
        if not errors:
            context_dict = {'categories': Category.objects.all()}
            content = PageContents.objects.all()
            if content:
                content = content[0]
            context_dict['category'] = None
            context_dict['content'] = content
            context_dict['admin'] = True
            return render(request, 'gearStore/index.html', context_dict)
            # return redirect('gearStore:index', context_dict=context_dict)
    # render the page
    context_dict['content'] = content
    return render(request, 'gearStore/edit_home.html', context=context_dict)


@login_required
def edit_about(request):
    # check if user is admin
    user_profile = UserProfile.objects.get(user=request.user)
    if not user_profile.adminStatus:
        return redirect(reverse("gearStore:admin-error"))

    # add categories into the context dict for left sidebar
    context_dict = {'categories': Category.objects.all()}
    context_dict['category'] = None

    # add page content into context dict for form autofill
    content = PageContents.objects.all()
    if content:
        content = content[0]
    else:
        context_dict['content'] = None
        return render(request, 'gearStore/about.html', context=context_dict)

    if request.method == 'POST':
        errors = []

        if request.POST.get("about-text"):
            content.about_contents = request.POST.get("about-text")

            content = content.save()

        context_dict['errors'] = errors
        if not errors:
            context_dict = {'categories': Category.objects.all()}
            content = PageContents.objects.all()
            if content:
                content = content[0]
            context_dict['category'] = None
            context_dict['content'] = content
            context_dict['admin'] = True
            return render(request, 'gearStore/about.html', context_dict)

    # render the page
    context_dict['content'] = content
    return render(request, 'gearStore/edit_about.html', context=context_dict)


@login_required
def edit_contact(request):
    # check if user is admin
    user_profile = UserProfile.objects.get(user=request.user)
    if not user_profile.adminStatus:
        return redirect(reverse("gearStore:admin-error"))

    # add categories into the context dict for left sidebar
    context_dict = {'categories': Category.objects.all()}
    context_dict['category'] = None

    # add page content into context dict for form autofill
    content = PageContents.objects.all()
    if content:
        content = content[0]
    else:
        context_dict['content'] = None
        return render(request, 'gearStore/contact.html', context=context_dict)

    if request.method == 'POST':
        errors = []

        if request.POST.get("contact-text"):
            content.contact_contents = request.POST.get("contact-text")

        if request.POST.get("contact"):
            content.contact = request.POST.get("contact")

        if request.POST.get("contact-option"):
            content.contact_option = request.POST.get("contact-option")

        content = content.save()

        context_dict['errors'] = errors
        if not errors:
            context_dict = {'categories': Category.objects.all()}
            content = PageContents.objects.all()
            if content:
                content = content[0]
            context_dict['category'] = None
            context_dict['content'] = content
            context_dict['admin'] = True
            return render(request, 'gearStore/contact.html', context_dict)

    context_dict['options'] = CONTACT_CHOICES
    # render the page
    context_dict['content'] = content
    return render(request, 'gearStore/edit_contact.html', context=context_dict)


@login_required
def booking(request, booking_id):
    context_dict = {'categories': Category.objects.all()}

    context_dict['admin'] = False
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        if user_profile:
            if user_profile.adminStatus:
                context_dict['admin'] = True

    try:
        # find and pass the booking
        booking = Booking.objects.get(id=booking_id)
        context_dict['booking'] = booking

        context_dict['borrowed'] = False
        if booking.is_current():
            context_dict['borrowed'] = True

        # pass the comments on the booking
        comments = BookingComments.objects.filter(booking=booking)
        context_dict['comments'] = comments

        # find and pass the page contents
        content = PageContents.objects.all()
        if content:
            content = content[0]
        context_dict['content'] = content

        context_dict['form_open'] = False
        if request.method == "POST":
            context_dict['form_open'] = True
            form = BookingCommentsForm(request.POST, request.FILES)
            errors = []
            if form.is_valid():
                if request.POST.get("comment"):
                    comment = form.save(commit=False)
                    comment.user = user_profile
                    comment.booking = booking
                    comment.save()
                    context_dict['form_open'] = False

            else:
                print(form.errors)
                for error_category in form.errors:
                    for error in form.errors[error_category]:
                        errors.append(error)
            context_dict['errors'] = errors
            return redirect(reverse("gearStore:booking", kwargs={'booking_id': booking.id}))
        else:
            context_dict['form'] = BookingCommentsForm
    except Booking.DoesNotExist:
        context_dict['booking'] = None

    context_dict['user'] = user_profile
    return render(request, 'gearStore/booking.html', context=context_dict)
