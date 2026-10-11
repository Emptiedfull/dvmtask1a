from django.contrib import admin

from .models import Choice, Question,Tag


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass 

class QuestionAdmin(admin.ModelAdmin):
    list_display = ["question_text", "pub_date", "was_published_recently"]
    fieldsets = [
        (None, {"fields": ["question_text","tags"]}),
        ("Date information", {"fields": ["pub_date"], "classes": ["collapse"]}),
    ]
    list_filter  = ["pub_date","tags"]
    inlines = [ChoiceInline]


admin.site.register(Question, QuestionAdmin)