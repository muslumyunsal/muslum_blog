from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.

class Article(models.Model):
    author = models.ForeignKey("auth.User",on_delete=models.CASCADE,verbose_name = "Yazar")
    title = models.CharField(max_length = 50,verbose_name = "Başlık")
    content = RichTextField(verbose_name = "İçerik")
    created_date = models.DateTimeField(auto_now_add=True,verbose_name = "Oluşturulma Tarihi")
    article_image = models.FileField(blank= True,null =True,verbose_name="Fotoğraf") #bu alan hem boş olabilir hem dolu olabilir dedik.
    summary = models.CharField(max_length = 100,blank= True,null =True,verbose_name = "Özet")
    def __str__(self):
        return self.title
    #Makaleleri tarihe göre sıralamak için bağladık ve ordering yaptık.
    class Meta:
        ordering = ['-created_date']

#modelimizi değiştirdiğimiz için bunu djangoya söylemeli ve veritabanındaki tablo yapısını değiştirmeliyiz. python manage.py makemigrations ve python manage.py migrate

"""
Makalenin postları olacağı için öncelikle comment modeli oluşturuyoruz. Ardından bunu Article modeli ile bağlıyoruz. Her makalenin yorumu olabileceği için bunu yaptık.
Article silindiğinde yorum da silinsin diye on_delete.
Article'ların yorumlarını almamız için isim vermemiz gerekiyor. article.comments diyerek yorum tablosuna da erişebileceğiz.
"""

class Comment(models.Model):
    article = models.ForeignKey(Article,on_delete=models.CASCADE,verbose_name="Makale",related_name="comments")
    comment_author = models.CharField(max_length = 50,verbose_name="İsim")
    comment_content = models.CharField(max_length = 200,verbose_name="Yorum")
    comment_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.comment_content

    #Yorumları tarihe göre sıralamak için bağladık ve ordering yaptık.
    class Meta:
        ordering = ['-comment_date']