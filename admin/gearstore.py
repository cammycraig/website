from django.contrib import admin
from models.gearstore import Category, UserProfile, Gear, Booking, PageContents, BookingComments, QR_Code


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'dateAdded', 'picture')

class GearAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'category', 'size', 'dateAdded', 'picture')


class BookingAdmin(admin.ModelAdmin):
    list_display = ('User.username', 'GearItem', 'DateToReturn')

class ContentsAdmin(admin.ModelAdmin):
    list_display = ('title', 'background_image', 'logo_image', 'home_contents', 'about_contents', 'contact_contents', 'contact', 'contact_option')

class BookingCommentsAdmin(admin.ModelAdmin):
    list_display = ('comment', 'booking', 'user',)

admin.site.register(UserProfile)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Gear, GearAdmin)
admin.site.register(Booking)
admin.site.register(PageContents)
admin.site.register(BookingComments, BookingCommentsAdmin)
admin.site.register(QR_Code)