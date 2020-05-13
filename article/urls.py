from django.contrib import admin
from django.urls import path
from . import views

app_name = "article"
#İleride redirect yaparken hangi uygulamanın içindeki hangi url'ye gideceğimizi belirleyebilmek için app'e isim veriyoruz.

urlpatterns = [
    path('dashboard/',views.dashboard,name = "dashboard"),
    path('addarticle/',views.addarticle,name = "addarticle"),
    path('article/<int:id>',views.detail,name = "detail"),
    path('update/<int:id>',views.updateArticle,name = "update"),
    path('delete/<int:id>',views.deleteArticle,name = "delete"),
    path('',views.articles,name = "articles"),
    path('comment/<int:id>',views.addComment,name = "comment"),
]

    #ana url dosyamızda articles'ı dahil ettiğimizden burada uzantı vermemize gerek yok. direkt /articles'a gidecek.
