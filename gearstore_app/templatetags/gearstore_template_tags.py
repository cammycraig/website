import datetime
import string
from datetime import *

from django import template
from db_models.gearstore import *
from slugify import slugify

register = template.Library()

app_label = 'gearstore_app'

def get_active_booking_statuses():
    views = []
    booking_views = STATUS_CHOICES
    for view in booking_views:
        bookings = Booking.objects.filter(status=view[0])
        if bookings:
            views.append(view[0])
    return views


def get_active_booking_statuses_for_user(user_profile):
    views = []
    booking_views = STATUS_CHOICES
    for view in booking_views:
        bookings = Booking.objects.filter(user=user_profile).filter(status=view[0])
        if bookings:
            views.append(view[0])
    return views


def get_active_booking_statuses_for_gear(gear):
    views = []
    booking_views = STATUS_CHOICES
    for view in booking_views:
        bookings = Booking.objects.filter(gearItem=gear).filter(status=view[0])
        if bookings:
            views.append(view[0])
    return views


def get_size_options(gear):
    size_options = {"all": "All Sizes"}
    for gear_item in gear:
        if not (slugify(gear_item.size) in size_options):
            size_options[slugify(gear_item.size)] = string.capwords(gear_item.size)
    return size_options


@register.inclusion_tag('./gearstore/category_menu.html')
def get_category_list():
    return {'categories': Category.objects.all()}


@register.inclusion_tag('./gearstore/base.html')
def get_categories():
    return {'categories': Category.objects.all()}


@register.inclusion_tag('./gearstore/display_title.html')
def get_title():
    content = PageContents.objects.all()
    if content:
        return {"title": content[0].title}
    else:
        return {"title": "Gear Store"}


@register.inclusion_tag('./gearstore/display_icon.html')
def get_icon():
    content = PageContents.objects.all()
    image_url = "/gearstore/site_images/default_icon.png"
    if content:
        image_url = content[0].icon_image
    if str(image_url)[0] != "/":
        image_url = "/" + str(image_url)
    return {"icon": image_url}


@register.inclusion_tag('./gearstore/display_colour.html')
def get_colour(booking_id):
    colour_dict = {
        'active': '#b2bda6',
        'requested': '#e8d9b7',
        'accepted': '#b5c9c6',
        'denied': '#d6bcb8',
        'returned': '#dacfe3',
        'unreturned': '#c9c7c7'
    }

    booking = Booking.objects.get(id=booking_id)
    colour = "ffffff"
    if booking:
        colour = colour_dict[booking.status.lower()]
    return {"colour": colour}


@register.inclusion_tag('./gearstore/display_background.html')
def get_background():
    content = PageContents.objects.all()
    image_url = "/gearstore/site_images/default_background.jpg"
    if content:
        image_url = content[0].background_image
    if str(image_url)[0] != "/":
        image_url = "/" + str(image_url)

    print(image_url)
    return {"background": image_url}


@register.inclusion_tag('./gearstore/display_all_bookings.html')
def show_all_bookings():
    orders = {
        "Default": {
            "id": "unordered",
            "bookings": Booking.objects.all()
        },

        "Personal": {
            "id": "personal",
            "bookings": Booking.objects.all().filter(purpose=SECONDARY_PURPOSE)
        },

        "Affiliated": {
            "id": "affiliated",
            "bookings": Booking.objects.all().filter(purpose=PRIMARY_PURPOSE)
        },

        "Due Sooner": {
            "id": "due-soon",
            "bookings": Booking.objects.all().order_by('dateToReturn')
        },

        "Due Later": {
            "id": "due-later",
            "bookings": Booking.objects.all().order_by('-dateToReturn')
        },

        "New": {
            "id": "new",
            "bookings": Booking.objects.all().order_by('-dateBorrowed')
        },

        "Old": {
            "id": "old",
            "bookings": Booking.objects.all().order_by('dateBorrowed')
        },

        "Name Asc.": {
            "id": "name-asc",
            "bookings": Booking.objects.all().order_by('user__last_name', 'user__first_name')
        },

        "Name Desc.": {
            "id": "name-desc",
            "bookings": Booking.objects.all().order_by('-user__last_name', '-user__first_name')
        }

    }

    orders_without_bookings = {}
    for order in orders:
        orders_without_bookings[order] = orders[order]["id"]

    return \
        {
            'orders': orders,
            'orders_without_bookings': orders_without_bookings,
            "booking_views": get_active_booking_statuses(),
            "section": "all"
        }


@register.inclusion_tag('gearstore/display_user_bookings.html')
def show_user_bookings(user_profile):
    orders = {
        "Default": {
            "id": "unordered",
            "bookings": Booking.objects.all().filter(user=user_profile)
        },

        "Personal": {
            "id": "personal",
            "bookings": Booking.objects.all().filter(user=user_profile).filter(purpose=SECONDARY_PURPOSE)
        },

        "Affiliated": {
            "id": "affiliated",
            "bookings": Booking.objects.all().filter(user=user_profile).filter(purpose=PRIMARY_PURPOSE)
        },

        "Due Sooner": {
            "id": "due-soon",
            "bookings": Booking.objects.all().filter(user=user_profile).order_by('dateToReturn')
        },
        "Due Later": {
            "id": "due-later",
            "bookings": Booking.objects.all().filter(user=user_profile).order_by('-dateToReturn')
        },
        "New": {
            "id": "new",
            "bookings": Booking.objects.all().filter(user=user_profile).order_by('-dateBorrowed')
        },
        "Old": {
            "id": "old",
            "bookings": Booking.objects.all().filter(user=user_profile).order_by('dateBorrowed')
        },
        "Name Asc.": {
            "id": "name-asc",
            "bookings": Booking.objects.all().filter(user=user_profile).order_by('user__last_name', 'user__first_name')
        },
        "Name Desc.": {
            "id": "name-desc",
            "bookings": Booking.objects.all().filter(user=user_profile).order_by('-user__last_name',
                                                                                 '-user__first_name')
        }

    }

    orders_without_bookings = {}
    for order in orders:
        orders_without_bookings[order] = orders[order]["id"]

    return \
        {
            'orders': orders,
            'orders_without_bookings': orders_without_bookings,
            "booking_views": get_active_booking_statuses_for_user(user_profile),
            "section": "user"
        }


@register.inclusion_tag('gearstore/display_all_bookings.html')
def show_gear_bookings(gear):
    orders = {
        "Default": {
            "id": "unordered",
            "bookings": Booking.objects.all().filter(gearItem=gear)
        },

        "Personal": {
            "id": "personal",
            "bookings": Booking.objects.all().filter(gearItem=gear).filter(purpose=SECONDARY_PURPOSE)
        },

        "Affiliated": {
            "id": "affiliated",
            "bookings": Booking.objects.all().filter(gearItem=gear).filter(purpose=PRIMARY_PURPOSE)
        },

        "Due Sooner": {
            "id": "due-soon",
            "bookings": Booking.objects.all().filter(gearItem=gear).order_by('dateToReturn')
        },
        "Due Later": {
            "id": "due-later",
            "bookings": Booking.objects.all().filter(gearItem=gear).order_by('-dateToReturn')
        },
        "New": {
            "id": "new",
            "bookings": Booking.objects.all().filter(gearItem=gear).order_by('-dateBorrowed')
        },
        "Old": {
            "id": "old",
            "bookings": Booking.objects.all().filter(gearItem=gear).order_by('dateBorrowed')
        },
        "Name Asc.": {
            "id": "name-asc",
            "bookings": Booking.objects.all().filter(gearItem=gear).order_by('user__last_name', 'user__first_name')
        },
        "Name Desc.": {
            "id": "name-desc",
            "bookings": Booking.objects.all().filter(gearItem=gear).order_by('-user__last_name',
                                                                             '-user__first_name')
        }

    }

    orders_without_bookings = {}
    for order in orders:
        orders_without_bookings[order] = orders[order]["id"]

    return \
        {
            'orders': orders,
            'orders_without_bookings': orders_without_bookings,
            "booking_views": get_active_booking_statuses_for_gear(gear),
            "section": "gear"
        }


@register.inclusion_tag('gearstore/display_booking_details.html')
def show_booking_details(booking):
    return {"booking": booking}


@register.inclusion_tag('gearstore/display_user_booking_details.html')
def show_user_booking_details(booking):
    return {"booking": booking}


@register.inclusion_tag('gearstore/display_view_filter_bar.html')
def show_view_filter_bar(order_id, booking_views, section):
    if booking_views[0] != "All":
        booking_views.insert(0, "All")
    return {
        "booking_views": booking_views,
        "order_id": order_id,
        "section": section

    }


@register.filter
def dict_lookup(dictionary, key):
    return dictionary.get(key)


@register.filter
def id_slugify(input_string):
    return slugify(input_string)


@register.filter
def get_status(gear):
    if gear.status == IN_SERVICE:
        if gear.is_available()[0]:
            return "available"
        else:
            return "unavailable"
    else:
        return "out-of-service"


@register.inclusion_tag('gearstore/display_order_filter_bar.html')
def show_order_filter_bar(orders, section):
    return {"orders": orders,
            "section": section
            }


@register.inclusion_tag('gearstore/display_description.html')
def show_description(description):
    return {"description": description}


@register.inclusion_tag('gearstore/display_comments.html')
def show_all_booking_comments(booking, user):
    comments = BookingComments.objects.all().filter(booking=booking)
    return {"comments": comments,
            "user": user,
            "show_comment_links": False}


@register.inclusion_tag('gearstore/display_comments.html')
def show_starred_gear_comments(gear, user):
    comments = BookingComments.objects.all().filter(booking__gearItem=gear).filter(starred=True)
    return {"comments": comments,
            "user": user,
            "show_comment_links": True}


@register.inclusion_tag('gearstore/display_date.html')
def get_date(date_type):
    relevant_date = ""
    if date_type == "min":
        relevant_date = datetime.now().date()
    elif date_type == "max":
        relevant_date = datetime.now().date() + timedelta(days=365)
    elif date_type == "default":
        relevant_date = datetime.now().date() + timedelta(days=14)
    return {"date": relevant_date}


@register.inclusion_tag('gearstore/display_gear_filter_bar.html')
def show_size_filter_bar(gear):
    options = get_size_options(gear)

    return {"options": options,
            "property_type": "size"}


@register.inclusion_tag('gearstore/display_gear_filter_bar.html')
def show_availability_filter_bar():
    options = {"all": "All",
               "available": "Available",
               "unavailable": "Unavailable",
               "out-of-service": "Out of Service"
               }

    return {"options": options,
            "property_type": "status"}


@register.inclusion_tag('gearstore/display_right_sidebar_links.html')
def show_right_sidebar_links():
    links = SidebarLinks.objects.all()
    if links:
        return {"links": links}
    else:
        return {}
