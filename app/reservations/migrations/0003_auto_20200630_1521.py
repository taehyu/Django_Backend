# Generated by Django 2.2.13 on 2020-06-30 15:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0002_auto_20200630_0346'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='discount_price',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='pay_with',
            field=models.CharField(choices=[('card', '신용/체크카드'), ('phone', '휴대폰결제'), ('kakao', '카카오페이'), ('payco', '페이코')], max_length=30),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='code',
            field=models.CharField(blank=True, max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='nonmember',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='nonmenbers', to='members.NonMember'),
        ),
    ]