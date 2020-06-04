# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Career(models.Model):
    career_id = models.IntegerField(primary_key=True)
    career = models.CharField(max_length=80, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'career'


class Company(models.Model):
    company_id = models.IntegerField(primary_key=True)
    company = models.CharField(max_length=40, blank=True, null=True)
    basic_addr = models.CharField(max_length=40, blank=True, null=True)
    detail_addr = models.CharField(max_length=40, blank=True, null=True)
    region = models.ForeignKey('Region', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'company'


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


class User(models.Model):
    user_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=40, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    region = models.ForeignKey(Region, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'


class UserCareer(models.Model):
    user_spec = models.OneToOneField('UserSpec', models.DO_NOTHING, primary_key=True)
    career = models.ForeignKey(Career, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'user_career'
        unique_together = (('user_spec', 'career'),)


class UserLicense(models.Model):
    user_spec = models.OneToOneField('UserSpec', models.DO_NOTHING, primary_key=True)
    license = models.ForeignKey(License, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'user_license'
        unique_together = (('user_spec', 'license'),)


class UserSpec(models.Model):
    user = models.OneToOneField(User, models.DO_NOTHING, primary_key=True)
    user_spec_id = models.IntegerField()
    edu_level = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_spec'
        unique_together = (('user', 'user_spec_id'),)


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