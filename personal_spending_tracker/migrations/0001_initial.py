# Generated by Django 4.1.7 on 2023-03-23 13:05

import datetime
from django.conf import settings
import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import personal_spending_tracker.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(max_length=20, unique=True, validators=[django.core.validators.RegexValidator(message='Username must contain at least 5 characters', regex='^.{5,}$')])),
                ('email', models.EmailField(max_length=254, unique=True, validators=[django.core.validators.EmailValidator(message='Please enter a valid email address')])),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('bio', models.TextField(blank=True, max_length=200)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('cycle_length', models.CharField(choices=[('WEEKLY', 'weekly'), ('MONTHLY', 'monthly')], default='MONTHLY', max_length=50)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='ConcreteCategory',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('limit', models.IntegerField()),
                ('goal_as_little_as_possible', models.BooleanField(default=False)),
                ('goal_well_distributed', models.BooleanField(default=False)),
                ('goal_x_less', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Cycle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(default=datetime.date.today)),
                ('cycle_length', models.CharField(choices=[('WEEKLY', 'weekly'), ('MONTHLY', 'monthly')], default='MONTHLY', max_length=50)),
                ('accounts_session_date', models.DateField(blank=True, null=True)),
                ('user', models.ForeignKey(default=personal_spending_tracker.models.get_user_id, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TemplateCategory',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('limit', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Spending',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('date', models.DateField(default=datetime.date.today)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.TextField(blank=True, null=True)),
                ('photo', models.ImageField(blank=True, upload_to='spendings/%Y/%m/%d/')),
                ('is_regular', models.BooleanField(default=False)),
                ('frequency', models.CharField(blank=True, choices=[('monthly', 'Monthly'), ('yearly', 'Yearly')], max_length=20, null=True)),
                ('next_due_date', models.DateField(blank=True, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='personal_spending_tracker.concretecategory')),
                ('user', models.ForeignKey(default=personal_spending_tracker.models.get_user_id, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PointReward',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points', models.IntegerField()),
                ('rewarding_for', models.CharField(choices=[('A1', 'not exceeding category limit'), ('A2', 'timely completion of the accounts session'), ('B1', 'spending as little as possible'), ('B2', 'well-distributed spending'), ('B3', 'cutting spending by x %')], max_length=50)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='personal_spending_tracker.concretecategory')),
                ('cycle', models.ForeignKey(default=personal_spending_tracker.models.get_cycle_id, on_delete=django.db.models.deletion.CASCADE, to='personal_spending_tracker.cycle')),
            ],
        ),
        migrations.CreateModel(
            name='ModelConcreteCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_name', models.CharField(max_length=100)),
                ('user', models.ForeignKey(default=personal_spending_tracker.models.get_user_id, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'current_name')},
            },
        ),
        migrations.AddField(
            model_name='concretecategory',
            name='cycle',
            field=models.ForeignKey(default=personal_spending_tracker.models.get_cycle_id, on_delete=django.db.models.deletion.CASCADE, to='personal_spending_tracker.cycle'),
        ),
        migrations.AddField(
            model_name='concretecategory',
            name='model_concrete_category',
            field=models.ForeignKey(default=personal_spending_tracker.models.get_model_concrete_category_id, on_delete=django.db.models.deletion.CASCADE, related_name='category', to='personal_spending_tracker.modelconcretecategory'),
        ),
        migrations.AddField(
            model_name='concretecategory',
            name='user',
            field=models.ForeignKey(default=personal_spending_tracker.models.get_user_id, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='concretecategory',
            unique_together={('user', 'name', 'cycle')},
        ),
    ]
