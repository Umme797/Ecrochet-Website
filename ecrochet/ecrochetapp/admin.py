from django.contrib import admin
from ecrochetapp.models import Product, Pattern

# Register your models here.



class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'pdetails', 'is_active']  
    list_filter = ['price', 'is_active']

admin.site.register(Product, ProductAdmin)



class PatternAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'difficulty', 'patterndetails']  
    list_filter = ['difficulty']  
    search_fields = ['name']  

admin.site.register(Pattern, PatternAdmin)

