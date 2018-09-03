from django.contrib import admin

from .models import *


class ProjectImageInline(admin.StackedInline):
    model = ProjectImage


class EventImageInline(admin.StackedInline):
    model = EventImage


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', '_startdate', '_enddate', "status")
    search_fields = ('title', 'description', "status")
    filter_horizontal = ("subevents",)

    list_filter = ("_startdate", "_enddate", "status")
    inlines = [EventImageInline]


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', '_startdate', '_enddate', "status")
    search_fields = ('title', 'description', "status")
    filter_horizontal = ("events",)

    list_filter = ("_startdate", "_enddate", "status")
    inlines = [ProjectImageInline]


@admin.register(Subevent)
class SubeventAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', '_startdate', '_enddate', "status")
    search_fields = ('title', 'description', "status")

    list_filter = ("_startdate", "_enddate", "status")


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("__str__", "first_name", "last_name", "second_name", "institute")


@admin.register(EventUserRegistration)
class EventUserRegistrationAdmin(admin.ModelAdmin):
    fields = ("person", "event", "role")
    list_display = ("__str__",)
    search_fields = ("__str__",)
    list_filter = ("person", "event", "role")


@admin.register(ProjectUserRegistration)
class ProjectUserRegistrationAdmin(admin.ModelAdmin):
    fields = ("person", "project", "role")
    list_display = ("__str__",)
    search_fields = ("__str__",)
    list_filter = ("person", "project", "role")
