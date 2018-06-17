# Generated by Django 2.0.5 on 2018-06-17 13:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('url', models.URLField(null=True)),
                ('photo', models.URLField(null=True)),
                ('category', models.TextField(null=True)),
                ('price', models.CharField(max_length=20)),
                ('star', models.CharField(max_length=20)),
                ('description', models.TextField(null=True)),
                ('details', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserProd',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='database.Product')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(blank=True, default='', max_length=16)),
                ('sex', models.CharField(max_length=5, null=True)),
                ('birthday', models.DateField(null=True)),
                ('address', models.TextField(null=True)),
                ('city', models.CharField(max_length=20, null=True)),
                ('country', models.CharField(max_length=20, null=True)),
                ('zip_code', models.CharField(max_length=20, null=True)),
                ('additional_info', models.TextField(null=True)),
                ('phone_number', models.CharField(max_length=20, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='userprod',
            name='user_info',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='database.UserProfile'),
        ),
    ]