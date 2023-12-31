# Generated by Django 4.2.6 on 2023-10-26 13:14

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=70)),
                ('builtIn', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Author',
                'verbose_name_plural': 'Authors',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('builtIn', models.BooleanField(default=False)),
                ('sequence', models.IntegerField()),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('builtIn', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Publisher',
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shelfCode', models.CharField(max_length=6, validators=[django.core.validators.RegexValidator(code='invalid_shelf_code', message='Shelf code format should be AA-999', regex='^[A-Z]{2}-\\d{3}$')])),
                ('name', models.CharField(max_length=80)),
                ('isbn', models.CharField(max_length=17)),
                ('pageCount', models.IntegerField(blank=True, null=True)),
                ('publishDate', models.DateField()),
                ('image', models.ImageField(upload_to='images')),
                ('loanable', models.BooleanField(default=True)),
                ('active', models.BooleanField(default=True)),
                ('featured', models.BooleanField(default=False)),
                ('createDate', models.DateTimeField(auto_now_add=True)),
                ('builtIn', models.BooleanField(default=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.author')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.category')),
                ('publisher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.publisher')),
            ],
            options={
                'verbose_name': 'Book',
                'verbose_name_plural': 'Books',
            },
        ),
    ]
