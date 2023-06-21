from django import template
from gearStore.models import Category, PageContents, Booking

register = template.Library()


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


@register.inclusion_tag('gearStore/display_colour.html')
def get_colour(booking_id):
    COLOUR_DICT = {
        'active': '#b2bda6',
        'requested': '#e8d9b7',
        'accepted': '#b5c9c6',
        'denied': '#d6bcb8',
        'returned': '#dacfe3',
        'not returned': '#c9c7c7'
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
