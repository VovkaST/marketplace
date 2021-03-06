# Generated by Django 3.2.8 on 2021-11-16 18:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_sellers', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'verbose_name': 'Profile', 'verbose_name_plural': 'Profiles'},
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.CreateModel(
            name='ViewHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('viewed_at', models.DateTimeField(auto_now_add=True, verbose_name='Viewed at')),
                ('compare', models.BooleanField(default=False, verbose_name='Compare')),
                ('goods', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='views_history', to='app_sellers.goods', verbose_name='Goods')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='view_history', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'View history',
                'verbose_name_plural': 'Views history',
            },
        ),
    ]
