from django.contrib import admin
from .models import Size, Category, ClothingItem, ClothingItemSize


class ClothingItemSizeInline(admin.TabularInline): #для добавления дополнительных размеров товаров
    model = ClothingItemSize
    extra = 4
#Это встроенная (inline) админ-форма, которая позволяет редактировать связанные объекты ClothingItemSize
# прямо на странице редактирования ClothingItem в Django admin.

@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)} #автозаполнение слагом из поля name
    search_fields = ('name',)


@admin.register(ClothingItem)
class ClothingItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'category', 'available', 'price', 'discount', 'created_at', 'updated_at')
    list_filter = ('available', 'category')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('-created_at', )
    inlines = [ClothingItemSizeInline] #для добавления дополнительных размеров товаров