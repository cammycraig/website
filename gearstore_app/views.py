import datetime
import os
from datetime import *

from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from forms.gearstore import UserForm, UserProfileForm, CategoryForm, GearForm, AdminForm, PageContentsForm, \
    BackgroundImageForm, LogoImageForm, BookingCommentsForm, IconImageForm
from db_models.gearstore import UserProfile, Category, Gear, Booking, AdminPassword, BookingComments, PageContents, \
    CONTACT_CHOICES, STATUS_CHOICES, GEAR_STATUS_CHOICES, PRIMARY_PURPOSE, PURPOSE_CHOICES, QR_Code, SidebarLinks

from django.template.defaultfilters import slugify

import hashlib

app_name = 'gearstore_app'

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

    if request.method == 'POST':
        errors = []

        if request.POST.get("edit-link-id"):
            try:
                link = SidebarLinks.objects.get(id=request.POST.get("edit-link-id"))
                link.link_text = request.POST.get("edit-link-text")
                link.url = request.POST.get("edit-link-url")
                link.save()
                return redirect(reverse('index'))
            except SidebarLinks.DoesNotExist:
                print("Missing ID")
                return redirect(reverse('index'))

        if request.POST.get("delete-link-id"):
            try:
                link = SidebarLinks.objects.get(id=request.POST.get("delete-link-id"))
                if request.POST.get("password"):
                    input_password = request.POST.get("password")
                    plaintext = input_password.encode()
                    hash = hashlib.sha256(plaintext)
                    readable_hash = hash.hexdigest()
                    passwords = AdminPassword.objects.all()
                    if passwords[0].password == readable_hash:
                        link.delete()
                        return redirect(reverse('index'))
                    else:
                        errors.append("Error: Incorrect admin password.")
                else:
                    errors.append("Error: No admin password entered.")
            except SidebarLinks.DoesNotExist:
                print("Missing ID")
                return redirect(reverse('index'))

        if request.POST.get("new-link-name"):
            if request.POST.get("new-link-url"):
                new_sidebar_link = SidebarLinks()
                new_sidebar_link.link_text = request.POST.get("new-link-name")
                new_sidebar_link.url = request.POST.get("new-link-url")
                new_sidebar_link.save()
                return redirect(reverse('index'))
            else:
                errors.append("Error: New link URL must be completed.")
        else:
            if request.POST.get("new-link-url"):
                errors.append("Error: New link name must be completed.")

        if request.POST.get("site-title"):
            content.title = request.POST.get("site-title")

        if request.POST.get("domain"):
            content.domain = request.POST.get("domain")

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
            else:
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
            else:
                for error_category in form.errors:
                    for error in form.errors[error_category]:
                        errors.append(error)

            # update icon image
            content = PageContents.objects.all()
            if content:
                content = content[0]
            form = IconImageForm(request.POST or None, request.FILES, instance=content)
            if form.is_valid():
                content = form.save()
            else:
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
            return redirect(reverse('index'))
    # render the page
    context_dict['content'] = content
    sidebar_links = SidebarLinks.objects.all()
    if sidebar_links:
        context_dict['sidebar_links'] = SidebarLinks.objects.all()
    else:
        context_dict['sidebar_links'] = None
    return render(request, './gearstore/index.html', context_dict)


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
        user_form = UserForm()

    if registered:
        return render(request, './gearstore/login.html', context=context_dict)

    else:
        errors = []
        for error_category in user_form.errors:
            for error in user_form.errors[error_category]:
                errors.append(error)
        context_dict['errors'] = errors
        context_dict['user_form'] = user_form
        context_dict['registered'] = registered

        return render(request, './gearstore/register.html', context=context_dict)


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
                return redirect(reverse('index'))
            else:
                errors.append("Account has been disabled due to inactivity. Please create a new account.")
        else:
            errors.append("Invalid combination of user and password.")
        context_dict['errors'] = errors
        return render(request, './gearstore/login.html', context=context_dict)
    else:
        return render(request, './gearstore/login.html', context=context_dict)


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
            return redirect(reverse('about'))

    return render(request, './gearstore/about.html', context_dict)


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
            return redirect(reverse('contact'))

    context_dict['options'] = CONTACT_CHOICES

    return render(request, './gearstore/contact.html', context_dict)


def category_menu(request):
    context_dict = {'categories': Category.objects.all()}
    context_dict['admin'] = False
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        if user_profile:
            if user_profile.adminStatus:
                context_dict['admin'] = True

    if request.POST:
        errors = []
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse('find-gear'))
        else:
            for error_category in form.errors:
                for error in form.errors[error_category]:
                    errors.append(error)
        context_dict['errors'] = errors
    context_dict['category'] = None
    return render(request, './gearstore/category_menu.html', context_dict)


def view_gear(request, gear_name_slug):
    context_dict = {'categories': Category.objects.all()}
    user_profile = None
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
    context_dict['user_profile'] = user_profile

    content = PageContents.objects.all()
    if content:
        content = content[0]
    context_dict['content'] = content

    context_dict['primary_purpose'] = PRIMARY_PURPOSE

    try:
        gear = Gear.objects.get(slug=gear_name_slug)
        context_dict['category'] = gear.category
        context_dict['gear'] = gear

        # attempt to borrow the gear
        if request.method == 'POST':
            errors = []
            if request.POST.get("edit-gear"):
                form = GearForm(request.POST or None, request.FILES or None, instance=gear)
                if form.is_valid():
                    new_slug = slugify(request.POST.get("name"))
                    if gear_name_slug != new_slug:
                        try:
                            existing_obj = Gear.objects.get(slug=new_slug)
                        except Gear.DoesNotExist:
                            existing_obj = None
                        if not existing_obj:
                            gear = form.save()
                            return redirect(reverse('view-gear',
                                                    kwargs={'gear_name_slug': gear.slug}))
                        else:
                            errors.append("Error: Gear name already exists.")
                    else:
                        gear = form.save(commit=False)
                        if request.POST.get("status"):
                            gear.status = request.POST.get("status")
                        gear.save()
                        return redirect(reverse('view-gear',
                                                kwargs={'gear_name_slug': gear.slug}))
                else:
                    for error_category in form.errors:
                        for error in form.errors[error_category]:
                            errors.append(error)
                context_dict['errors'] = errors
            elif request.POST.get("delete-gear"):
                input_password = request.POST.get("password")
                plaintext = input_password.encode()
                hash = hashlib.sha256(plaintext)
                readable_hash = hash.hexdigest()
                passwords = AdminPassword.objects.all()
                if passwords[0].password == readable_hash:
                    gear.delete()
                    return redirect(reverse('view-category',
                                            kwargs={'category_name_slug': gear.category.slug}))
                else:
                    errors.append("Error: Incorrect Password.")
            else:
                if request.POST.get('edit_id'):
                    if request.POST.get('comment'):
                        try:
                            comment = BookingComments.objects.get(id=request.POST.get('edit_id'))
                            comment.comment = request.POST.get('comment')
                            comment.save()
                            return redirect(reverse("view-gear", kwargs={'gear_name_slug': gear_name_slug}))
                        except BookingComments.DoesNotExist:
                            errors.append("Error: Booking does not exist.")
                elif request.POST.get('delete_id'):
                    if request.POST.get('delete_password'):
                        try:
                            comment = BookingComments.objects.get(id=request.POST.get('delete_id'))
                            input_password = request.POST.get("delete_password")
                            plaintext = input_password.encode()
                            hash = hashlib.sha256(plaintext)
                            readable_hash = hash.hexdigest()
                            passwords = AdminPassword.objects.all()
                            if passwords[0].password == readable_hash:
                                comment.delete()
                                return redirect(reverse("view-gear", kwargs={'gear_name_slug': gear_name_slug}))
                            else:
                                errors.append("Error: Incorrect Password.")
                            comment.save()
                        except BookingComments.DoesNotExist:
                            errors.append("Error: Booking does not exist.")
                elif request.POST.get('star_id'):
                    starred = request.POST.get('hidden_star_value')
                    if starred:
                        if request.POST.get('star_password'):
                            try:
                                comment = BookingComments.objects.get(id=request.POST.get('star_id'))
                                input_password = request.POST.get("star_password")
                                plaintext = input_password.encode()
                                hash = hashlib.sha256(plaintext)
                                readable_hash = hash.hexdigest()
                                passwords = AdminPassword.objects.all()
                                if passwords[0].password == readable_hash:
                                    if starred == "true" or starred == "false":
                                        starred = starred == "true"
                                        comment.starred = starred
                                        comment.save()
                                        return redirect(reverse("view-gear", kwargs={'gear_name_slug': gear_name_slug}))
                                else:
                                    errors.append("Error: Incorrect Password.")
                                comment.save()
                            except BookingComments.DoesNotExist:
                                errors.append("Error: Booking does not exist.")
                    else:
                        errors.append("Error: No star status.")
                else:
                    borrow = Booking()
                    if request.user:
                        borrow.gearItem = gear
                        borrow.user = UserProfile.objects.get(user=request.user)
                        borrow.dateToReturn = request.POST.get("dateToReturn")
                        borrow.purpose = request.POST.get("purpose")
                        borrow.save()
                        qr_code = QR_Code()
                        qr_code.booking = borrow
                        qr_code.save()
                        qr_code.update_qrcode()
                        return redirect(reverse("booking", kwargs={'booking_id': borrow.id }))

        # find if the gear is currently on loan
        is_available, active_booking = gear.is_available()
        context_dict['available'] = is_available
        context_dict['active_booking'] = active_booking

        # find the gear's category
        category = Category.objects.get(name=gear.category)
        context_dict['category'] = category
    except Gear.DoesNotExist:
        context_dict['gear'] = None

    context_dict['admin'] = False
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        if user_profile:
            if user_profile.adminStatus:
                context_dict['admin'] = True
    context_dict['options'] = STATUS_CHOICES
    context_dict['purpose_options'] = PURPOSE_CHOICES
    context_dict['gear_status_options'] = GEAR_STATUS_CHOICES
    return render(request, './gearstore/view_gear.html', context_dict)


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
        context_dict['form_open'] = True
        # check picture
        if request.FILES:
            picture_form = UserProfileForm(request.POST or None, request.FILES, instance=user_profile)
            if picture_form.is_valid():
                picture_form.save()
            else:
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
    context_dict["user_bookings"] = user_bookings

    context_dict['errors'] = errors
    return render(request, './gearstore/account.html', context_dict)


@login_required
def process_logout(request):
    context_dict = {'categories': Category.objects.all()}
    context_dict['category'] = None
    logout(request)
    return redirect(reverse('index'))


def admin_error(request):
    context_dict = {'categories': Category.objects.all()}
    context_dict['category'] = None
    return render(request, '/gearstore/admin_error.html', context=context_dict)


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
            if not gear_item.is_available()[0]:
                num_available -= 1

        context_dict['available'] = num_available
        context_dict['total'] = num_total
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['gear'] = None

    if request.method == 'POST':
        errors = []
        if request.POST.get("add-gear"):
            form = GearForm(request.POST, request.FILES)
            if form.is_valid():
                if category:
                    gear = form.save(commit=False)
                    gear.category = category
                    if not request.FILES:
                        gear.picture = category.picture
                    gear.save()
                    return redirect(reverse('view-category',
                                            kwargs={'category_name_slug': category_name_slug}))
            else:
                for error_category in form.errors:
                    for error in form.errors[error_category]:
                        errors.append(error)
        elif request.POST.get("edit-category"):
            form = CategoryForm(request.POST or None, request.FILES or None, instance=category)

            if form.is_valid():
                new_slug = slugify(request.POST.get("name"))
                if category_name_slug != new_slug:
                    try:
                        existing_obj = Category.objects.get(slug=new_slug)
                    except Category.DoesNotExist:
                        existing_obj = None
                    if not existing_obj:
                        category = form.save()
                        return redirect(reverse('view-category',
                                                kwargs={'category_name_slug': category.slug}))
                    else:
                        errors.append("Error: Category name already exists.")
                else:
                    category = form.save()
                    return redirect(reverse('view-category',
                                            kwargs={'category_name_slug': category.slug}))
            else:
                for error_category in form.errors:
                    for error in form.errors[error_category]:
                        errors.append(error)

        if request.POST.get("delete-category"):
            input_password = request.POST.get("password")
            plaintext = input_password.encode()
            hash = hashlib.sha256(plaintext)
            readable_hash = hash.hexdigest()
            passwords = AdminPassword.objects.all()
            if passwords[0].password == readable_hash:
                category.delete()
                return redirect(reverse('find-gear'))
            else:
                errors.append("Error: Incorrect Password.")

        context_dict['errors'] = errors
    return render(request, './gearstore/category.html', context=context_dict)


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

        if booking.user != user_profile and not user_profile.adminStatus:
            return redirect(reverse("admin-error"))

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
            errors = []
            if request.POST.get('edit_id'):
                if request.POST.get('comment'):
                    try:
                        comment = BookingComments.objects.get(id=request.POST.get('edit_id'))
                        comment.comment = request.POST.get('comment')
                        comment.save()
                        return redirect(reverse("booking", kwargs={'booking_id': booking.id}))
                    except BookingComments.DoesNotExist:
                        errors.append("Error: Booking does not exist.")
            elif request.POST.get('delete_id'):
                if request.POST.get('delete_password'):
                    try:
                        comment = BookingComments.objects.get(id=request.POST.get('delete_id'))
                        input_password = request.POST.get("delete_password")
                        plaintext = input_password.encode()
                        hash = hashlib.sha256(plaintext)
                        readable_hash = hash.hexdigest()
                        passwords = AdminPassword.objects.all()
                        if passwords[0].password == readable_hash:
                            comment.delete()
                            return redirect(reverse("booking", kwargs={'booking_id': booking.id}))
                        else:
                            errors.append("Error: Incorrect Password.")
                        comment.save()
                    except BookingComments.DoesNotExist:
                        errors.append("Error: Booking does not exist.")
            elif request.POST.get('star_id'):
                starred = request.POST.get('hidden_star_value')
                if starred:
                    if request.POST.get('star_password'):
                        try:
                            comment = BookingComments.objects.get(id=request.POST.get('star_id'))
                            input_password = request.POST.get("star_password")
                            plaintext = input_password.encode()
                            hash = hashlib.sha256(plaintext)
                            readable_hash = hash.hexdigest()
                            passwords = AdminPassword.objects.all()
                            if passwords[0].password == readable_hash:
                                if starred == "true" or starred == "false":
                                    starred = starred == "true"
                                    comment.starred = starred
                                    comment.save()
                                    return redirect(reverse("booking", kwargs={'booking_id': booking.id}))
                            else:
                                errors.append("Error: Incorrect Password.")
                            comment.save()
                        except BookingComments.DoesNotExist:
                            errors.append("Error: Booking does not exist.")
                else:
                    errors.append("Error: No star status.")
            if request.POST.get('status'):
                booking.status = request.POST.get('status')
                booking.purpose = request.POST.get('purpose')
                booking.dateToReturn = request.POST.get('dateToReturn')
                booking.save()
                return redirect(reverse("booking", kwargs={'booking_id': booking.id}))
            else:
                context_dict['form_open'] = True
                form = BookingCommentsForm(request.POST, request.FILES)
                if form.is_valid():
                    if request.POST.get("comment"):
                        comment = form.save(commit=False)
                        comment.user = user_profile
                        comment.booking = booking
                        comment.save()
                        context_dict['form_open'] = False

                else:
                    for error_category in form.errors:
                        for error in form.errors[error_category]:
                            errors.append(error)
                context_dict['errors'] = errors
                return redirect(reverse("booking", kwargs={'booking_id': booking.id}))
        else:
            context_dict['form'] = BookingCommentsForm
    except Booking.DoesNotExist:
        context_dict['booking'] = None

    context_dict['options'] = STATUS_CHOICES
    context_dict['purpose_options'] = PURPOSE_CHOICES
    context_dict['user'] = user_profile
    qr_code = QR_Code.objects.get(booking=booking)
    qr_code.update_qrcode()
    context_dict['qr_code'] = qr_code.qr_code
    return render(request, './gearstore/booking.html', context=context_dict)

@login_required
def user(request, user):
    context_dict = {'categories': Category.objects.all()}
    context_dict['category'] = None

    # check if user is admin
    user_profile = UserProfile.objects.get(user=request.user)
    if not user_profile.adminStatus:
        return redirect(reverse("admin-error"))

    try:
        user_page_user = User.objects.get(username=user)
        user_page_profile = UserProfile.objects.get(user=user_page_user)
        context_dict['user_profile'] = user_profile
        user_bookings = Booking.objects.filter(user=user_page_profile)
    except User.DoesNotExist:
        user_page_profile = None
        user_bookings = None

    context_dict['user_page_profile'] = user_page_profile
    context_dict["user_bookings"] = user_bookings

    return render(request, './gearstore/user.html', context_dict)

def handler404(request, exception):
    context_dict = {'categories': Category.objects.all()}
    context_dict['category'] = None
    return render(request, './gearstore/404.html', context=context_dict)