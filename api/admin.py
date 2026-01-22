# from django.contrib import admin
# from django.contrib.auth.models import User
# from .models import Profile
#
#
# class ProfileAdmin(admin.ModelAdmin):
#     list_display = (
#         "id",
#         "username",
#         "user",
#         "is_active_profile",
#         "created_at",
#     )
#     list_filter = ("is_active_profile",)
#     search_fields = ("username", "display_name", "user__username")
#
#
# admin.site.register(Profile, ProfileAdmin)
#
#
# class ProfileInline(admin.StackedInline):
#     model = Profile
#     can_delete = False
#     extra = 0
#
#
# class CustomUserAdmin(admin.ModelAdmin):
#     inlines = (ProfileInline,)
#
#
# admin.site.unregister(User)
# admin.site.register(User, CustomUserAdmin)
#
#
#
# class UserAdmin(admin.ModelAdmin):
#     inlines = (ProfileInline,)
#
#
# class ProfileAdmin(admin.ModelAdmin):
#     list_display = (
#         "username",
#         "user",
#         "display_name",
#         "city",
#         "is_active_profile",
#         "created_at",
#     )
#     list_filter = ("is_active_profile", "city")
#     search_fields = ("username", "display_name", "user__username")
#
#
# # unregister default User admin
# admin.site.unregister(User)
#
# # register User with inline Profile
# admin.site.register(User, UserAdmin)
#
# # register Profile ONCE
# admin.site.register(Profile, ProfileAdmin)
#
#
# from django.contrib import admin
# from django.contrib.auth.models import User
# from .models import Profile
#
# class ProfileInline(admin.StackedInline):
#     model = Profile
#     can_delete = False
#
# class UserAdmin(admin.ModelAdmin):
#     inlines = (ProfileInline,)
#
# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)
#


from django.contrib import admin
from django.contrib.auth.models import User
from .models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    extra = 0


class CustomUserAdmin(admin.ModelAdmin):
    inlines = (ProfileInline,)


class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "username",
        "user",
        "display_name",
        "city",
        "is_active_profile",
        "created_at",
    )
    list_filter = ("is_active_profile", "city")
    search_fields = ("username", "display_name", "user__username")


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile, ProfileAdmin)
