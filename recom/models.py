# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Career(models.Model):
    career_id = models.IntegerField(primary_key=True)
    career = models.CharField(max_length=80, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'career'

    def __str__(self):
        return "%s" % (self.career)


class Company(models.Model):
    company_id = models.IntegerField(primary_key=True)
    company = models.CharField(max_length=40, blank=True, null=True)
    basic_addr = models.CharField(max_length=40, blank=True, null=True)
    detail_addr = models.CharField(max_length=40, blank=True, null=True)
    region = models.ForeignKey('Region', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'company'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Favorite(models.Model):
    user = models.OneToOneField('User', models.DO_NOTHING, primary_key=True)
    notice = models.ForeignKey('Notice', models.DO_NOTHING)
    applieddate = models.DateTimeField(db_column='appliedDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'favorite'
        unique_together = (('user', 'notice'),)


class HolidayTpNm(models.Model):
    holiday_tp_nm_id = models.IntegerField(primary_key=True)
    holiday_tp_nm = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'holiday_tp_nm'


class JobsCd(models.Model):
    jobs_cd = models.IntegerField(primary_key=True)
    job_name = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'jobs_cd'


class License(models.Model):
    license_id = models.IntegerField(primary_key=True)
    license = models.CharField(max_length=80, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'license'

    def __str__(self):
        return "%s" % (self.license)


class Notice(models.Model):
    notice_id = models.IntegerField(primary_key=True)
    company = models.ForeignKey(Company, models.DO_NOTHING, blank=True, null=True)
    jobs_cd = models.ForeignKey(JobsCd, models.DO_NOTHING, db_column='jobs_cd', blank=True, null=True)
    title = models.CharField(max_length=40, blank=True, null=True)
    sal_tp_nm = models.CharField(max_length=40, blank=True, null=True)
    max_sal = models.IntegerField(blank=True, null=True)
    min_sal = models.IntegerField(blank=True, null=True)
    holiday_tp_nm = models.CharField(max_length=40, blank=True, null=True)
    max_edubg = models.CharField(max_length=20, blank=True, null=True)
    min_edubg = models.CharField(max_length=20, blank=True, null=True)
    career = models.CharField(max_length=40, blank=True, null=True)
    validation = models.CharField(max_length=40, blank=True, null=True)
    wanted_info_url = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'notice'


class Post(models.Model):
    notice = models.OneToOneField(Notice, models.DO_NOTHING, primary_key=True)
    company = models.ForeignKey(Company, models.DO_NOTHING)
    reg_dt = models.CharField(max_length=40, blank=True, null=True)
    close_dt = models.CharField(max_length=40, blank=True, null=True)
    smodify_dt = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'post'
        unique_together = (('notice', 'company'),)


class Region(models.Model):
    region_id = models.IntegerField(primary_key=True)
    region = models.CharField(max_length=80, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'region'

    def __str__(self):
        return "%s" % (self.region)


class User(models.Model):
    user = models.OneToOneField(AuthUser, models.DO_NOTHING, primary_key=True)
    name = models.CharField(max_length=40, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    region = models.ForeignKey(Region, models.DO_NOTHING, blank=True, null=True)
    location = models.CharField(max_length=64, blank=True, null=True)
    holiday_tp_nm = models.CharField(max_length=40, blank=True, null=True)
    min_sal = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'


class UserCareer(models.Model):
    user_spec = models.ForeignKey('UserSpec', models.DO_NOTHING)
    career = models.ForeignKey(Career, models.DO_NOTHING)
    user_career_id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'user_career'


class UserLicense(models.Model):
    user_spec = models.ForeignKey('UserSpec', models.DO_NOTHING)
    license = models.ForeignKey(License, models.DO_NOTHING)
    user_license_id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'user_license'


class UserSpec(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING)
    user_spec_id = models.IntegerField(primary_key=True)
    edu_level = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_spec'


class WantedHolidayTpNm(models.Model):
    wanted_spec = models.OneToOneField('WantedSpec', models.DO_NOTHING, primary_key=True)
    holiday_tp_nm = models.ForeignKey(HolidayTpNm, models.DO_NOTHING, db_column='holiday_tp_nm')

    class Meta:
        managed = False
        db_table = 'wanted_holiday_tp_nm'
        unique_together = (('wanted_spec', 'holiday_tp_nm'),)


class WantedJobsCd(models.Model):
    wanted_spec = models.OneToOneField('WantedSpec', models.DO_NOTHING, primary_key=True)
    jobs_cd = models.ForeignKey(JobsCd, models.DO_NOTHING, db_column='jobs_cd')

    class Meta:
        managed = False
        db_table = 'wanted_jobs_cd'
        unique_together = (('wanted_spec', 'jobs_cd'),)


class WantedRegion(models.Model):
    wanted_spec = models.OneToOneField('WantedSpec', models.DO_NOTHING, primary_key=True)
    region = models.ForeignKey(Region, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'wanted_region'
        unique_together = (('wanted_spec', 'region'),)


class WantedSpec(models.Model):
    user = models.OneToOneField(User, models.DO_NOTHING, primary_key=True)
    wanted_spec_id = models.IntegerField()
    min_salary = models.IntegerField(blank=True, null=True)
    max_salary = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wanted_spec'
        unique_together = (('user', 'wanted_spec_id'),)
