from django.db import models

class Ureg(models.Model):

    ufname = models.CharField(max_length=20)
    usname = models.CharField(max_length=20)
    uname = models.CharField(max_length=20)
    umail = models.EmailField()
    upass = models.CharField(max_length=20)
    uphone = models.CharField(max_length=10)
    uaddr = models.TextField()
    ucard = models.CharField(max_length=12)
    utype = models.CharField(max_length=10, default='costumer')

    def __str__(self):
        return self.uname

class Books(models.Model):

    book_title = models.CharField(max_length=100)
    book_pmail = models.EmailField()
    book_isbn10 = models.IntegerField()
    book_author = models.CharField(max_length=20)
    book_publisher = models.CharField(max_length=20)
    book_copies = models.IntegerField()
    book_price = models.IntegerField()
    book_description = models.TextField()
    book_lang = models.CharField(max_length=20)
    book_year = models.IntegerField()
    book_image = models.ImageField(upload_to='', blank=True)
    book_genre = models.TextField(max_length=50)

    def __str__(self):

        return self.book_title

class Cate(models.Model):
    cate_name = models.CharField(max_length=100)
    cate_img = models.ImageField(upload_to='')

    def __str__(self):

        return self.cate_name

class Bcomm(models.Model):
    btitle = models.CharField(max_length=100)
    bumail = models.EmailField(blank=True,null=True)
    bcom = models.TextField()

    def __str__(self):
        return self.btitle


class Cart(models.Model):
    cbid = models.IntegerField()
    cbtitle  = models.CharField(max_length=100)
    cbmail = models.EmailField()
    cstat = models.CharField(default='no',max_length=3)
    cdeli = models.CharField(default='no',max_length=3)

    def __str__(self):
        return self.cbtitle






