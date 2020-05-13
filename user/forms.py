from django import forms
#django'nun kendi form yapısını dahil ettik. Flask'ta wtf form kullanmıştık.

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=50,label = "Kullanıcı Adı")
    first_name = forms.CharField(label = "Adınız")
    last_name = forms.CharField(label = "Soyadınız")
    email = forms.EmailField(label = "E-mail Adresiniz")
    password = forms.CharField(min_length=5,label="Şifreniz",widget=forms.PasswordInput)
    confirm = forms.CharField(min_length=5,label="Şifrenizi Doğrulayın",widget=forms.PasswordInput)
    #password ve confirm'in uyuşmasını kontrol etmek için clean metodunu kullanıyoruz.
    #clean aslında forms içinde hazır bir metod. Burada override edeceğiz.
    def clean(self):
        username = self.cleaned_data.get("username")
        first_name = self.cleaned_data.get("first_name")
        last_name = self.cleaned_data.get("last_name")
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        confirm = self.cleaned_data.get("confirm")
        
        if password and confirm and password != confirm:
            #Hata fırlatıyoruz.
            raise forms.ValidationError("Şifre eşleşmiyor.")
        #Eğer sıkıntı yoksa bilgileri dönebilmek için sözlük yapısı kullanmamız gerekiyor.
        values = {
            "username" : username,
            "first_name" : first_name,
            "last_name" : last_name,
            "email" : email,
            "password" : password,
        }
        return values

class LoginForm(forms.Form):
    username= forms.CharField(label = "Kullanıcı Adı")
    password = forms.CharField(label = "Şifreniz",widget = forms.PasswordInput)