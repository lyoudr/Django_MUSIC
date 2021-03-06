# Generated by Django 3.1.4 on 2021-10-13 06:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('order', '0002_auto_20211005_0210'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderinfo',
            name='order_user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='order_info_c', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='orderinfo',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order_info_a', to='order.order'),
        ),
    ]
