from django.contrib import admin

from .models import *


class ProjectImageInline(admin.StackedInline):
    model = ProjectImage


class EventImageInline(admin.StackedInline):
    model = EventImage


class ProjectFileInline(admin.StackedInline):
    model = ProjectFile


class EventFileInline(admin.StackedInline):
    model = EventFile


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', '_startdate', '_enddate', "status")
    search_fields = ('title', 'description', "status")
    filter_horizontal = ("subevents",)

    list_filter = ("_startdate", "_enddate", "status")
    inlines = [EventImageInline, EventFileInline]


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', '_startdate', '_enddate', "status")
    search_fields = ('title', 'description', "status")
    filter_horizontal = ("events",)

    list_filter = ("_startdate", "_enddate", "status")
    inlines = [ProjectImageInline, ProjectFileInline]


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'description', '_startdate', '_enddate', "status")
    search_fields = ('title', 'description', "status")
    filter_horizontal = ("projects",)

    list_filter = ("type", "_startdate", "_enddate", "status")


@admin.register(Subevent)
class SubeventAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', '_startdate', '_enddate', "status")
    search_fields = ('title', 'description', "status")

    list_filter = ("_startdate", "_enddate", "status")


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("__str__", "first_name", "last_name", "second_name", "institute")


@admin.register(CourseUserRegistration)
class CourseUserRegistrationAdmin(admin.ModelAdmin):
    fields = ("person", "course", "role")
    list_display = ("__str__",)
    search_fields = ("__str__",)
    list_filter = ("person", "course", "role")


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


@admin.register(Diagnostic)
class DiagnosticAdmin(admin.ModelAdmin):
    list_display = ("title", "weight")


@admin.register(StudentDiag)
class StudentDiagAdmin(admin.ModelAdmin):
    list_display = ["person", "diagnostic"]
    search_fields = ["person", "diagnostic"]


@admin.register(PrTheme)
class PrThemeAdmin(admin.ModelAdmin):
    list_display = ("__str__",)
