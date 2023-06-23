from django import template
from gearStore.models import Category, PageContents, Booking, STATUS_CHOICES

register = template.Library()


def get_active_booking_statuses():
    views = []
    booking_views = STATUS_CHOICES
    for view in booking_views:
        bookings = Booking.objects.filter(status=view[0])
        if bookings:
            views.append(view[0])
    return views


@register.inclusion_tag('gearStore/category_menu.html')
def get_category_list():
    return {'categories': Category.objects.all()}


@register.inclusion_tag('gearStore/base.html')
def get_categories():
    return {'categories': Category.objects.all()}


@register.inclusion_tag('gearStore/display_title.html')
def get_title():
    content = PageContents.objects.all()
    if content:
        return {"title": content[0].title}
    else:
        return {"title": "Gear Store"}


@register.inclusion_tag('gearStore/display_icon.html')
def get_icon():
    content = PageContents.objects.all()
    image_url = "/site_images/default_icon.png"
    if content:
        image_url = content[0].icon_image
    if str(image_url)[0] != "/":
        image_url = "/" + str(image_url)
    return {"icon": image_url}


@register.inclusion_tag('gearStore/display_colour.html')
def get_colour(booking_id):
    COLOUR_DICT = {
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
        print("hi")
        print(booking.id, booking_id)
        print(booking.status)
        colour = COLOUR_DICT[booking.status.lower()]
    return {"colour": colour}


@register.inclusion_tag('gearStore/display_background.html')
def get_background():
    content = PageContents.objects.all()
    image_url = "/site_images/default_background.jpg"
    if content:
        image_url = content[0].background_image
    if str(image_url)[0] != "/":
        image_url = "/" + str(image_url)
    return {"background": image_url}


@register.inclusion_tag('gearStore/display_all_bookings.html')
def show_all_bookings():
    orders = {
        "Default": {
            "id": "unordered",
            "bookings": Booking.objects.all()
        },
        "Due Sooner": {
            "id": "due-soon",
            "bookings": Booking.objects.all().order_by('-dateToReturn')
        },
        "Due Later": {
            "id": "due-later",
            "bookings": Booking.objects.all().order_by('dateToReturn')
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

    print(orders)

    print(orders_without_bookings)
    return \
        {
            'orders': orders,
            'orders_without_bookings': orders_without_bookings,
            "booking_views": get_active_booking_statuses()
        }


@register.inclusion_tag('gearStore/display_user_bookings.html')
def show_user_bookings(user_profile):
    user_bookings = Booking.objects.filter(user=user_profile)
    return {"user_bookings": user_bookings}


@register.inclusion_tag('gearStore/display_booking_details.html')
def show_booking_details(booking):
    return {"booking": booking}


@register.inclusion_tag('gearStore/display_view_filter_bar.html')
def show_view_filter_bar(order_id):
    booking_views = get_active_booking_statuses()
    booking_views.insert(0, "All")
    return {
        "booking_views": booking_views,
        "order_id": order_id
    }


@register.filter
def dict_lookup(dict, key):
    return dict.get(key)


@register.inclusion_tag('gearStore/display_order_filter_bar.html')
def show_order_filter_bar(orders):
    return {"orders": orders}