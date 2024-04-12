from typing import Any, List, Optional, Tuple
from django.contrib.admin import SimpleListFilter
from django.db.models.query import QuerySet
from .models import Member

class MemberAdminListFilter(SimpleListFilter):
    title = "회원상태"
    parameter_name ="member__status"

    def lookups(self, request: Any, model_admin: Any):
        return(
            ('active','승인'),
            ('cancel','취소')
        )

    def queryset(self, request, queryset):
        print('admin:',self.value())
        if not self.value():
            return queryset
        if self.value().lower() == 'cancel':
            return queryset.filter(status__id=8)
        elif self.value().lower() == 'active':
            return queryset.filter(status__id=7)
        return queryset.filter(user__email__regex=self.SOCIAL_EMAIL_REGEX)