from django.contrib import admin
from .models import Category, Tag, FAQ, Contact, Subscribe, Answer


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]
    list_display = ['question']


admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Contact)
admin.site.register(Subscribe)
