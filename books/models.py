from django.db import models
from django.core.validators import RegexValidator


# Create your models here.

class Author(models.Model):
    name = models.CharField(max_length=70)
    builtIn = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'
        
    def __str__(self):
        return self.name
    
    
class Publisher(models.Model):
    name = models.CharField(max_length=50)
    builtIn = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Publisher'
        
    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=80)
    builtIn = models.BooleanField(default=False)
    sequence = models.IntegerField()

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        
    def __str__(self):
        return self.name


class Book(models.Model):
    shelfCode = models.CharField(
        max_length=6,
        validators=[
            RegexValidator(
                regex=r'^[A-Z]{2}-\d{3}$',  
                message='Shelf code format should be AA-999',
                code='invalid_shelf_code'
            )
        ]
    )
    
    name = models.CharField(max_length=80)
    isbn = models.CharField(
        max_length=17,
        validators=[
            RegexValidator(
                regex=r'^\d{3}-\d{2}-\d{5}-\d{1}$',  
                message='Invalid ISBN format. Please use XXX-XX-XXXXX-X format.',
                code='invalid_isbn'
            )
        ]
    )
    
    pageCount = models.IntegerField(blank=True, null=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    publishDate = models.DateField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images')
    loanable = models.BooleanField(default=True)
    active = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    createDate = models.DateTimeField(auto_now_add=True)
    builtIn = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Book'
        verbose_name_plural = 'Books'
        
    def __str__(self):
        return self.name