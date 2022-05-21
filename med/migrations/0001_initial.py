# Generated by Django 4.0.3 on 2022-05-10 23:22

from django.conf import settings
import django.contrib.auth.models
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


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
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('avatar', models.ImageField(default='avatars/default_avatar.jpg', upload_to='avatars/')),
                ('is_patient', models.BooleanField(default=False)),
                ('is_clinic', models.BooleanField(default=False)),
                ('is_doctor', models.BooleanField(default=False)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone', models.CharField(max_length=20)),
                ('patronymic', models.CharField(blank=True, max_length=25, null=True)),
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
            name='Chat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creationDate', models.DateTimeField(auto_now_add=True)),
                ('users', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(default='', max_length=50)),
                ('date_time', models.DateTimeField()),
                ('name', models.CharField(max_length=300)),
                ('description', models.CharField(blank=True, max_length=500)),
                ('instructions', models.CharField(blank=True, max_length=1000)),
                ('users', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Procedure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=None, max_length=40, null=True)),
                ('description', models.TextField(default=None, null=True)),
                ('steps', models.TextField(default=None, null=True)),
                ('doctor_spec', models.CharField(default='', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Treatment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(default=-1)),
                ('complaint', models.TextField(default=None, null=True)),
                ('symptoms', models.TextField(default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Clinic',
            fields=[
                ('specialization', models.TextField(default='')),
                ('address', models.CharField(default='', max_length=75)),
                ('extra', models.TextField(default='')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('specialization', models.TextField(default='')),
                ('extra', models.TextField(default='')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('clinics', models.ManyToManyField(to='med.clinic')),
            ],
            options={
                'verbose_name': 'Доктор',
            },
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('extra', models.TextField(default='')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('text', models.TextField()),
                ('creationDate', models.DateTimeField(auto_now_add=True)),
                ('event', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='med.event')),
                ('sender', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sender', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('sender', models.IntegerField()),
                ('creationDate', models.DateTimeField(auto_now_add=True)),
                ('chat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='med.chat')),
            ],
        ),
        migrations.CreateModel(
            name='CurrentProcedure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(blank=True, null=True)),
                ('procedure', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='med.procedure')),
                ('treatment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='med.treatment')),
            ],
        ),
        migrations.AddField(
            model_name='treatment',
            name='clinic',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='med.clinic'),
        ),
        migrations.AddField(
            model_name='treatment',
            name='doctor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='med.doctor'),
        ),
        migrations.AddField(
            model_name='treatment',
            name='patient',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='med.patient'),
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monday', django.contrib.postgres.fields.ArrayField(base_field=models.TimeField(), null=True, size=2)),
                ('tuesday', django.contrib.postgres.fields.ArrayField(base_field=models.TimeField(), null=True, size=2)),
                ('wednesday', django.contrib.postgres.fields.ArrayField(base_field=models.TimeField(), null=True, size=2)),
                ('thursday', django.contrib.postgres.fields.ArrayField(base_field=models.TimeField(), null=True, size=2)),
                ('friday', django.contrib.postgres.fields.ArrayField(base_field=models.TimeField(), null=True, size=2)),
                ('saturday', django.contrib.postgres.fields.ArrayField(base_field=models.TimeField(), null=True, size=2)),
                ('sunday', django.contrib.postgres.fields.ArrayField(base_field=models.TimeField(), null=True, size=2)),
                ('doctor', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='med.doctor')),
            ],
        ),
    ]
