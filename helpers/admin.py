from django.contrib import admin
from .models import Callback, QuestionCategory, Question, PolicyConf
admin.site.register(Question)


class QuestionInline(admin.TabularInline):
    model = Question
    max_num = 15
    min_num = 1
    extra = 0


@admin.register(QuestionCategory)
class QuestionCategoryAdmin(admin.ModelAdmin):
    inlines = [QuestionInline, ]


@admin.register(PolicyConf)
class PolicyConfAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        if self.model.objects.count() >= 1:
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        if self.model.objects.count() < 1:
            return super().add_view(request, extra_context)
        else:
            obj = (self.model.objects.first()).id
            return super().change_view(request=request,
                                       extra_context=extra_context,
                                       object_id=str(obj))

    class Meta:
        model = PolicyConf


@admin.register(Callback)
class CallbackAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'created_on', 'checked']
    list_filter = ['checked', 'created_on', 'subject']
    search_fields = ['name', 'email']
