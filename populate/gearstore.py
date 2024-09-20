'''
Background Image
Photo by Mike L on Unsplash: 
https://unsplash.com/photos/brown-mountain-with-trees-lSh6vd87jTs?utm_content=creditShareLink&utm_medium=referral&utm_source=unsplash
'''

import django

from db_models.gearstore import Gear, Category, PageContents
from website.wsgi import *
import os

django.setup()

def populate():

    print('starting population script')

    gear = []

    categories = []

    default_data = [
        {'background_image': '/gearstore/site_images/default_background.jpg',
         'logo_image': 'gearstore/site_images/default_logo.png',
         'home_contents': 'Welcome to Gear Store! Gear Store is a website where you can find and borrow gear for sports! If you want to browse the gear available to be borrowed, take a look at the options in the left-hand sidebar, or browse the options in the Find Gear tab.',
         'about_contents': '''Hi, welcome to Gear Store! Here, you are able to view various pieces of gear available to be borrowed, and add them to your own account.


If you don't already have an account, feel free to create one and log in, and view the My Account page. Here you can manage your account and your bookings, as well as logout.


If you are a manager of the club, please create an account and enter your admin password to become a site admin. Then, you will be able to add gear and categories, as well as view all current bookings.
         ''',
         'contact_contents': '''Here is how you can contact us if you have any questions:


If you want to ask us any questions regarding using this website, please email:

help@gearstore.com


If you have any questions about borrowing gear, please email:

borrow@gearstore.com


You can drop us a follow on instagram @gear-store
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
            picture=gearItem['picture']
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

    print('Done!')
