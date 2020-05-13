from django.shortcuts import render,redirect
from .forms import RegisterForm,LoginForm
from django.contrib.auth.models import User #User modelini kullanarak bir obje oluşturacağımızdan dahil ettik.
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages #django mesajlarını dahil ettik.
# Create your views here.

#Aşağıda UZUN YOLU MUTLAKA OKU!
def register(request):
    form = RegisterForm(request.POST or None) #bu sayede Post request varsa işlem yapacak Get request'te ise boş formu dönecek. Post veya Get'i kontrol etmek zorunda kalmıyoruz.
    if form.is_valid():
        username = form.cleaned_data.get("username")
        first_name = form.cleaned_data.get("first_name")
        last_name = form.cleaned_data.get("last_name")
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")

        newUser = User(username = username,first_name=first_name,last_name=last_name,email=email)
        newUser.set_password(password)
        newUser.save()
        login(request,newUser)
        messages.success(request,"Başarıyla kayıt oldunuz.")
        return redirect("index")#urls.py'de url'ye isim verdiğimiz için redirect yapabiliyoruz.
        
    context = {
        "form":form
    }
    return render(request,"register.html",context)

    """UZUN YOL
    if request.method == "POST":
        form = RegisterForm(request.POST)
        clean metodunu çağırmış olduk. Böylece girilen bilgileri alacağız. Clean sadece is_valid ile çalışır.
        Değerler sağlanırsa değerler döner ve is_valid True olarak döner.
        Değerler sağlanmazsa False döner ve hata fırlatılır.
        if form.is_valid():
            username = form.cleaned_data.get("username")
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")

            User objesi oluşturuyoruz.
            newUser = User(username = username,first_name=first_name,last_name=last_name,email=email)
            newUser.set_password(password)#parolayı şifreledik.
            newUser.save()
            Kullanıcıyı kayıt ettikten sonra otomatik giriş yapabilmesi için login fonksiyonunu kullacağız.
            login(request,newUser)

            return redirect("index")
        is_valid olmaması durumunda
        context = {
        "form":form
        }
        return render(request,"register.html",context)

    else: Get request olması halinde
        form = RegisterForm()
        context = {
        "form":form
        }
        return render(request,"register.html",context)"""

def loginUser(request):
    form = LoginForm(request.POST or None)
    context = {
        "form":form
    }
    #clean zaten forms'un kendi metodu. Dolayısıyla override yapmadan is_valid kullanabiliriz.
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        #authenticate kullanıcının olup olmadığını kontrol eder.
        user = authenticate(username=username,password=password)

        if user is None:
            messages.info(request,"Kullanıcı bilgileri hatalı.")
            return render(request,"login.html",context)
        messages.success(request,"Başarıyla giriş yaptınız.")
        login(request,user)
        return redirect("index")
    return render(request,"login.html",context)

def logoutUser(request):
    logout(request)
    messages.success(request,"Başarıyla çıkış yaptınız.")
    return redirect("index")