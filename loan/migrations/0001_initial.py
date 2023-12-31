# Generated by Django 4.2.4 on 2023-08-28 13:03

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
            name='Request',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('interest_rate', models.DecimalField(decimal_places=2, max_digits=5)),
                ('repayment_period', models.PositiveIntegerField(help_text='Repayment period in months')),
                ('purpose', models.TextField()),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('funded', 'Funded'), ('repaid', 'Repaid')], default='pending', max_length=20)),
                ('borrower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('loan_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='loan.request')),
                ('payer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Funding',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount_funded', models.DecimalField(decimal_places=2, max_digits=10)),
                ('funded_at', models.DateTimeField(auto_now_add=True)),
                ('lender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('loan_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='loan.request')),
            ],
        ),
    ]
