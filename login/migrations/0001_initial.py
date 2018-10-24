# Generated by Django 2.1.2 on 2018-10-24 11:35

import django.core.validators
from django.db import migrations, models
import django.utils.timezone
import login.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('full_name', models.CharField(max_length=256, validators=[django.core.validators.RegexValidator(code='invalid_full_name', message='Name must be Alphabetic', regex='^[a-zA-Z ]*$')])),
                ('acc_no', models.PositiveIntegerField(unique=True, validators=[django.core.validators.MinValueValidator(10000000), django.core.validators.MaxValueValidator(99999999)])),
                ('OTPSeed', models.CharField(editable=False, max_length=16, validators=[django.core.validators.RegexValidator('^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')])),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=6)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('contact_no', models.IntegerField(unique=True)),
                ('Address', models.CharField(max_length=512)),
                ('city', models.CharField(max_length=256)),
                ('balance', models.DecimalField(decimal_places=2, default=1001, max_digits=12)),
                ('designation', models.CharField(choices=[('user', 'permission to do account operations'), ('merchant', 'create payments for their users'), ('employee', 'check the employee dashboard'), ('manager', 'Manager/Staff, critical transactions'), ('admin', 'admin')], max_length=25)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', login.managers.UserManager()),
            ],
        ),
    ]
