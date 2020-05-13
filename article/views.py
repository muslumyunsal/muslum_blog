from django.shortcuts import render,redirect,get_object_or_404,reverse
from .forms import ArticleForm
from django.contrib import messages
from .models import Article,Comment
from django.contrib.auth.decorators import login_required

# Create your views here.

def articles(request):
    #arama yapmak bu kadar kolay...
    keyword = request.POST.get("keyword")
    if keyword:
        articles = Article.objects.filter(title__contains=keyword)
        return render(request,"articles.html",{"articles":articles})
    articles = Article.objects.all()
    return render(request,"articles.html",{"articles":articles})

def index(request):
    return render(request,"index.html")

def about(request):
    return render(request,"about.html")

#login_url = "user:login" dediğimizde kullanıcı giriş yapmadığı sayfaya gidemeyeceği gibi user uygulamasındaki login isimli sayfaya gidecek.
@login_required(login_url = "user:login") 
def dashboard(request):
    articles = Article.objects.filter(author = request.user)
    context = {
        "articles":articles
    }
    return render(request,"dashboard.html",context)

@login_required(login_url = "user:login") 
def addarticle(request):
    form = ArticleForm(request.POST or None,request.FILES or None)
    if form.is_valid():
        article = form.save(commit=False)
        article.author = request.user
        article.save()
        messages.success(request,"Makaleniz başarıyla eklendi.")
        return redirect("index")

    return render(request,"addarticle.html",{"form":form})

def detail(request,id):
    #eğer belirtilen id'de makale varsa getirip olmayan id get request yapıldığında getirilmesin diye get_object or 404 kullanıyoruz.
    article = get_object_or_404(Article,id = id)
    """article = Article.objects.filter(id = id).first() filter bize liste döner o yüzden first diyerek ilk objeyi alıyoruz. Bu şekilde alırsak id'si olmayan makaleyi de get requestte sayfalamaya çalışır."""
    comments = article.comments.all()
    return render(request,"detail.html",{"article":article,"comments":comments})

@login_required(login_url = "user:login") 
def updateArticle(request,id):
    article = get_object_or_404(Article,id = id)
    form = ArticleForm(request.POST or None,request.FILES or None,instance=article)
    #instance=article diyerek formumuzun şu anki bilgileriyle başlaması için yazılıyor.
    if form.is_valid():
        article = form.save(commit=False)
        article.author = request.user
        article.save()
        messages.success(request,"Makaleniz başarıyla güncellendi.")
        return redirect("index")
    
    return render(request,"update.html",{"form":form})

@login_required(login_url = "user:login") 
def deleteArticle(request,id):
    article = get_object_or_404(Article,id = id)
    article.delete()
    messages.success(request,"Makale başarıyla silindi.")
    return redirect("article:dashboard")
    #article'ın altındaki dashboard'a git dedik!
    
def addComment(request,id):
    article = get_object_or_404(Article,id = id)
    if request.method == "POST":
        comment_author = request.POST.get("comment_author")
        comment_content = request.POST.get("comment_content")

        newComment = Comment(comment_author = comment_author,comment_content= comment_content)
        newComment.article = article
        newComment.save()
    return redirect(reverse("article:detail",kwargs={"id":id}))
    #dinamik url'yi yönlendirmek için url'yi girmek yerine reverse kullandık. reverse+gidilecek adres+sözlük yapısında değişken.
