from collections.abc import Iterable
from typing import Any
from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from .models import User, Resource, Category, FavouriteList, FavouriteItem,  Type , BorrowTransaction
# Register your models here.

class IsActiveFilter(admin.SimpleListFilter):
    title = 'Active Status'
    parameter_name = 'is_active'
    
    def lookups(self, request: HttpRequest, model_admin: ModelAdmin):
        return (
            ('0', 'inactive'),
            ('1', 'active'),
        )
    
    def queryset(self, request: HttpRequest, queryset: QuerySet):
        if self.value() == '0':
            return queryset.filter(is_active = False)
        if self.value() == '1':
            return queryset.filter(is_active = True)

class IsMediathekarFilter(admin.SimpleListFilter):
    title = 'Permission'
    parameter_name = 'is_mediathekar'
    
    def lookups(self, request: HttpRequest, model_admin: ModelAdmin):
        return (
            ('0', 'user'),
            ('1', 'mediathekar'),
        )
    
    def queryset(self, request: HttpRequest, queryset: QuerySet):
        if self.value() == '0':
            return queryset.filter(is_mediathekar = False)
        if self.value() == '1':
            return queryset.filter(is_mediathekar = True)

class UserAdmin(admin.ModelAdmin):
    list_filter = (IsActiveFilter, IsMediathekarFilter,)
    list_display = ('username', 'email', 'is_active', 'is_staff', 'is_mediathekar')

class IsBorrowAvailableFilter(admin.SimpleListFilter):
    title = 'Borrow Availability'
    parameter_name = 'is_available_to_borrow'
    
    def lookups(self, request: HttpRequest, model_admin: ModelAdmin):
        return (
            ('0', 'available'),
            ('1', 'unavailable'),
        )
    
    def queryset(self, request: HttpRequest, queryset: QuerySet):
        if self.value() == '0':
            return queryset.filter(is_available_to_borrow = False)
        if self.value() == '1':
            return queryset.filter(is_available_to_borrow = True)

class IsDLAvailableFilter(admin.SimpleListFilter):
    title = 'Download Availability'
    parameter_name = 'is_available_to_download'
    
    def lookups(self, request: HttpRequest, model_admin: ModelAdmin):
        return (
            ('0', 'available'),
            ('1', 'unavailable'),
        )
    
    def queryset(self, request: HttpRequest, queryset: QuerySet):
        if self.value() == '0':
            return queryset.filter(is_available_to_download = False)
        if self.value() == '1':
            return queryset.filter(is_available_to_download = True)
        
class CategoryFilter(admin.SimpleListFilter):
    title = 'Category'
    parameter_name = 'categories'

    def lookups(self, request, model_admin):
        categories = set()
        for resource in model_admin.model.objects.all():
            for category in resource.categories.all():
                categories.add((category.id, category.name))
        return sorted(categories, key=lambda x: x[1])

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(categories__id=self.value())
        return queryset

class TypeFilter(admin.SimpleListFilter):
    title = 'Type'
    parameter_name = 'types'

    def lookups(self, request, model_admin):
        types = set()
        for resource in model_admin.model.objects.all():
            for type in resource.types.all():
                types.add((type.id, type.name))
        return sorted(types, key=lambda x: x[1])

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(types__id=self.value())
        return queryset

class ResourceAdmin(admin.ModelAdmin):

    list_filter = (IsBorrowAvailableFilter, IsDLAvailableFilter, CategoryFilter, TypeFilter)

    list_display = ('title', 'author', 'year', 'is_available_to_borrow', 'is_available_to_download', 'get_categories', 'get_types')

    def get_categories(self, obj):
        return ", ".join([c.name for c in obj.categories.all()])
    get_categories.short_description = 'Categories'

    def get_types(self, obj):
        return ", ".join([c.name for c in obj.types.all()])
    get_categories.short_description = 'Types'

class BorrowTransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'resource', 'due_date')

class TypeAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(User, UserAdmin)
admin.site.register(Category)
admin.site.register(Type,TypeAdmin)
admin.site.register(FavouriteItem)
admin.site.register(FavouriteList)
admin.site.register(BorrowTransaction, BorrowTransactionAdmin)
admin.site.register(Resource, ResourceAdmin)
