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
        {'name': 'Climbing Rope', 'description': 'A strong, dynamic rope used for climbing',
         'size': 'medium', 'category': 'Rope', 'picture': '/gear_images/rope.jpg'},
        {'name': 'Climbing Harnesses', 'description': 'A safety harness worn by climbers',
         'size': 'medium', 'category': 'Harnesses', 'picture': '/gear_images/harness.jpg'},
        {'name': 'Climbing Helmet', 'description': 'A protective helmet worn by climbers',
         'size': 'large', 'category': 'Clothing', 'picture': '/gear_images/helmet.jpg'},
        {'name': 'Climbing Shoes', 'description': 'Specialized shoes used for rock climbing',
         'size': 'medium', 'category': 'Clothing', 'picture': '/gear_images/shoes.jpg'},
        {'name': 'Climbing Chalk Bag', 'description': 'A bag used to hold chalk for climbing',
         'size': 'small', 'category': 'Accessories', 'picture': '/gear_images/chalkbag.jpg'},
        {'name': 'Crampons', 'description': 'Spiky attachments for climbing shoes', 'size': 'small',
         'category': 'Accessories', 'picture': '/gear_images/g12.jpg'},
        {'name': 'Steel Ice Axe', 'description': 'A tool used for ice climbing and mountaineering',
         'size': 'large', 'category': 'Axes', 'picture': '/gear_images/petzl.jpeg'},
        {'name': 'Raven Ice Axe', 'description': 'A tool used for ice climbing and mountaineering',
         'size': 'large', 'category': 'Axes', 'picture': '/gear_images/raven.png'},
        {'name': 'Mountaineering Boots', 'description': 'Boots designed for use in mountaineering',
         'size': 'large', 'category': 'Clothing', 'picture': '/gear_images/b2.jpg'},
        {'name': 'Backpack', 'description': 'A bag for carrying gear',
         'size': 'medium', 'category': 'Backpacks', 'picture': '/gear_images/default.png'},
        {'name': 'Rucksack', 'description': ' A rucksack for carrying gear', 'size': 'small',
         'category': 'Backpacks', 'picture': '/gear_images/tempest30.jpg'},
        {'name': 'Belay Device', 'description': 'A device used to control a climbing rope',
         'size': 'small', 'category': 'Accessories', 'picture': '/gear_images/bigair.jpg'},
        {'name': 'Hiking Boots', 'description': 'Boots designed for use in hiking', 'size': 'medium',
         'category': 'Clothing', 'picture': '/gear_images/summer.png'}
    ]

    categories = [
        {'name': 'Rope', 'description': 'Ropes for mountaineering', 'picture': '/category_images/ropes.jpg'},
        {'name': 'Harnesses', 'description': 'Harnesses for mountaineering', 'picture': '/category_images/harness.jpg'},
        {'name': 'Accessories', 'description': 'Misc accessories for mountaineering', 'picture': '/category_images/chalkbag.jpg'},
        {'name': 'Backpacks', 'description': 'Backpacks for mountaineering', 'picture': '/category_images/bag.jpg'},
        {'name': 'Axes', 'description': 'Ice axes for mountaineering', 'picture': '/category_images/axes.jpg'},
        {'name': 'Clothing', 'description': 'Clothing items for mountaineering', 'picture': '/category_images/helmet.jpg'}
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
         'title': 'Gear Store'
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
