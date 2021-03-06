# Generated by Django 3.2.8 on 2022-01-20 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_auto_20211116_1809'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='files/', verbose_name='Avatar'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='patronymic',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Patronymic'),
        ),
    ]
