# Generated by Django 3.2.8 on 2021-11-16 19:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_sellers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goodsdescriptionsvalues',
            name='feature',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='description_feature', to='app_sellers.goodsdescriptionsvalues', verbose_name='Description item'),
        ),
    ]
