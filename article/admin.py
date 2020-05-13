from django.contrib import admin
from .models import Article,Comment

# Register your models here.
# admin.site.register(Article) admin panelinde göstermek için kullandığımız bu fonk.'u decorator olarak kullanarak özelleştirme yapacağız.

admin.site.register(Comment)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ["title","author","created_date"]
    list_display_links = ["title","created_date"]
    search_fields = ["title"]
    list_filter = ["created_date","author"]
    class Meta:
        model = Article
        #Bunun yaparak admin classı ile Article classını birleştirdik.

