from django.contrib import admin

from .models import Topic, Course, Student, Order


class CourseAdmin(admin.ModelAdmin):
    def apply_discount(self, request, queryset):
        for course in queryset:
            course.price = course.price * 90 / 100
            course.save()

    apply_discount.short_description = 'Apply 10%% discount'
    fields = [('title', 'topic'), ('price', 'num_reviews', 'for_everyone')]
    list_display = ('title', 'topic', 'price')
    actions = ['apply_discount']


class OrderAdmin(admin.ModelAdmin):
    fields = ['courses', ('student', 'order_status')]
    readonly_fields = ['order_date']
    list_display = ('id', 'student', 'order_status', 'order_date', 'total_items')


class StudentAdmin(admin.ModelAdmin):
    fields = ['first_name', 'last_name', 'level', 'registered_courses']

    list_display = ('username', 'first_name', 'last_name', 'level', 'get_courses')

    def get_courses(self, obj):
        return ", ".join([p.title for p in obj.registered_courses.all()])


class CourseInline(admin.TabularInline):
    model = Course


class TopicAdmin(admin.ModelAdmin):
    fields = ['name', 'length']
    list_display = ('name', 'length')
    inlines = [CourseInline]


# Register your models here.
admin.site.register(Topic, TopicAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Order, OrderAdmin)
