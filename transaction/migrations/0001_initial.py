<<<<<<< HEAD
# Generated by Django 2.1.2 on 2018-10-29 11:01
=======
# Generated by Django 2.1.2 on 2018-10-29 07:47
>>>>>>> 09a22451869c95e9c4ca51f398ee04a2044f2239

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TX_in',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=256, validators=[django.core.validators.RegexValidator(code='invalid_full_name', message='Name must be Alphabetic', regex='^[a-zA-Z ]*$')])),
                ('acc_no', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(10000000), django.core.validators.MaxValueValidator(99999999)])),
                ('Amount', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1000), django.core.validators.MaxValueValidator(100000)])),
                ('OTP', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(100000), django.core.validators.MaxValueValidator(999999)])),
                ('message', models.CharField(max_length=256, validators=[django.core.validators.RegexValidator(code='invalid_message_name', message='Messages must be Alphabetic', regex='^[a-zA-Z ]*$')])),
                ('status', models.CharField(choices=[('1', 'Approved'), ('2', 'Payment/Cash'), ('3', 'Processing'), ('4', 'Rejection'), ('5', 'Error_Occured')], default='3', editable=False, max_length=1)),
                ('Tr_type', models.CharField(default='1', max_length=1)),
                ('is_cash', models.BooleanField(editable=False)),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('fromUser', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='from_account', to=settings.AUTH_USER_MODEL)),
                ('toUser', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='to_account', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
