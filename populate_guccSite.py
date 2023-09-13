import django
import os
import random
from groupProject.wsgi import *

from django.contrib.auth.models import User

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'groupProject.settings')

django.setup()
from guccSite.models import Gear, Category, PageContents


def populate():
    gear = [
        {'name': 'Dagger Axiom', 'description': 'info on size and difficulty of axiom',
         'size': 'medium', 'category': 'Boats', 'picture': '/gear_images/daggerAxiom.jpg'},
        {'name': 'Dagger Mamba', 'description': 'info on size and difficulty',
         'size': 'large', 'category': 'Boats', 'picture': '/gear_images/harness.jpg'},
        {'name': 'EXO T-REX', 'description': 'info on size and difficulty. Could mention its Patricks',
         'size': 'large', 'category': 'Boats', 'picture': '/gear_images/helmet.jpg'},
        {'name': 'Werner Orange Glass', 'description': 'orange Werner carbon and glass paddle ',
         'size': '197', 'category': 'Paddles', 'picture': '/gear_images/wernerGlassOrange.jpg'},
        {'name': 'Red Ainsworth ', 'description': 'red club paddle',
         'size': 'medium', 'category': 'Paddles', 'picture': '/gear_images/chalkbag.jpg'},
        {'name': 'Red Palm helmet', 'description': 'red club helmet', 'size': 'small',
         'category': 'Helmets', 'picture': '/gear_images/g12.jpg'},
        {'name': 'Red Bouyancy Aid', 'description': 'A wearable flotation device',
         'size': 'medium', 'category': 'BAs', 'picture': '/gear_images/petzl.jpeg'},
        {'name': 'Pink Wetsuit', 'description': 'A pink Wetsuit',
         'size': 'small', 'category': 'Wetsuits', 'picture': '/gear_images/raven.png'},
        {'name': 'Orange Club Cag', 'description': 'A club cag with seals that work well!',
         'size': 'large', 'category': 'CAGs', 'picture': '/gear_images/b2.jpg'},
        {'name': 'Nookie 1', 'description': 'A spray deck to keep water out your boat',
         'size': 'large', 'category': 'Spraydecks', 'picture': '/gear_images/default.png'},
        {'name': 'Nookie 2', 'description': 'A spray deck to keep water out your boat example with make and unique id to differentiate', 'size': 'small',
         'category': 'Spraydecks', 'picture': '/gear_images/tempest30.jpg'},
        {'name': 'Nookie small 5', 'description': 'A spray deck to keep water out your boat example of naming with make and size and id to differentiate',
         'size': 'small', 'category': 'Accessories', 'picture': '/gear_images/bigair.jpg'},
        {'name': 'Palm 17', 'description': 'A spray deck to keep water out your boat example of naming sith make and unique id', 'size': 'medium',
         'category': 'Clothing', 'picture': '/gear_images/summer.png'}
    ]

    categories = [
        {'name': 'Boats', 'description': 'Whitewater kayaking boats ', 'picture': '/category_images/ropes.jpg'},
        {'name': 'Paddles', 'description': 'Whitewater kayaking paddles', 'picture': '/category_images/harness.jpg'},
        {'name': 'BAs', 'description': 'Bouyancy Aides to keep you afloat', 'picture': '/category_images/chalkbag.jpg'},
        {'name': 'Wetsuits', 'description': 'Wetsuits to keep you warm', 'picture': '/category_images/bag.jpg'},
        {'name': 'CAGs', 'description': 'Dry jackets to keep your body warm and dry (ish)', 'picture': '/category_images/axes.jpg'},
        {'name': 'Helmets', 'description': 'Helmets to protect your head', 'picture': '/category_images/helmet.jpg'}
        {'name': 'Spraydecks', 'description': 'Spraydeck to keep water out your boat', 'picture': '/category_images/helmet.jpg'}
    ]

    default_data = [
        {'background_image': '/site_images/default_background.jpg',
         'logo_image': 'site_images/default_logo.png',
         'home_contents': 'Welcome to Gear Store! Gear Store is a website where you can find and borrow gear for sports! If you want to browse the gear available to be borrowed, take a look at the options in the left-hand sidebar, or browse the options in the Find Gear tab.',
         'about_contents': '''Hi, welcome to Gear Store! Here, you are able to view various pieces of gear available to be borrowed, and add them to your own account.
        If you don't already have an account, feel free to create one and log in, and view the My Account page. Here you can manage your account and your bookings, as well as logout.
        If you are a manager of the club, please create an account and enter your admin password to become a site admin. Then, you will be able to add gear and categories, as well as view all current bookings.
         ''',
         'contact_contents': '''Here is how you can contact us if you have any questions:
        If you want to ask us any questions regarding using this website, please email:
        help@guccsite.com
        If you have any questions about borrowing gear, please email:
        borrow@gucchelp.com
        You can drop us a follow on instagram @gusaCanoe
         ''',
         'contact': '07933 123 456',
         'contact_option': 'logo-whatsapp',
         'title': 'gucc-site'
         }
    ]

    categorydict = {}

    for category in categories:
        c = Category.objects.get_or_create(
            name=category['name'],
            description=category['description'],
            picture=category['picture']
        )[0]
        c.save()
        categorydict[category['name']] = c

    gearList = []

    for gearItem in gear:
        g = Gear.objects.get_or_create(
            name=gearItem['name'],
            category=categorydict[gearItem['category']],
            description=gearItem['description'],
            size=gearItem['size'],
            picture = gearItem['picture']
        )[0]
        gearList.append(g)
        g.save()

    for data in default_data:
        d = PageContents.objects.get_or_create(
            background_image=data['background_image'],
            logo_image=data['logo_image'],
            home_contents=data['home_contents'],
            about_contents=data['about_contents'],
            contact_contents=data['contact_contents'],
            contact=data['contact'],
            contact_option=data['contact_option'],
            title=data['title']
        )[0]
        d.save()

if __name__ == '__main__':
    print('starting population script')
    populate()
    print('Done!')
