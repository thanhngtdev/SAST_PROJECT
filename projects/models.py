from django.db import models

from projects.const import TARGET_STATUS, SCAN_STATUS


class Organization(models.Model):
    organization_id = models.AutoField(primary_key=True)
    organization_name = models.CharField(max_length=200)
    organization_short_name = models.CharField(max_length=200, default="")

    class Meta:
        verbose_name_plural = "1. Organization"

    def __str__(self):
        return self.organization_name


class Projects(models.Model):
    project_name = models.CharField(max_length=10000, verbose_name="Project name")
    project_note = models.TextField(default="", blank=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, blank=True)

    class Meta:
        verbose_name_plural = "2. Projects"

    def __str__(self):
        return self.project_name


class Targets(models.Model):
    project = models.ForeignKey(Projects, on_delete=models.CASCADE, default=None)
    target_name = models.TextField(default='', blank=True)
    target_status = models.IntegerField(choices=TARGET_STATUS, default=1)
    target_source_code = models.FileField(upload_to='documents/%Y/%m/%d/', default=None)
    target_scan_options_json = models.TextField(blank=True, null=True,
                                                default='''{"language":["python","java"],"scan_type":"full_scan"}''')
    target_scan_notification_config_json = models.TextField(blank=True, null=True, default='''{}''')

    def __str__(self):
        return self.target_name

    class Meta:
        verbose_name_plural = "3. Targets"


class Scans(models.Model):
    target = models.ForeignKey(Targets, on_delete=models.CASCADE, default=None)
    start_time = models.DateTimeField('Finished time', auto_now_add=True, editable=True)
    finished_time = models.DateTimeField('Finished time', auto_now_add=True, editable=True)
    scan_result_json = models.TextField(blank=True, null=True)
    scan_status = models.IntegerField(choices=SCAN_STATUS, default=1)
    scan_options_json = models.TextField(blank=True, null=True,
                                         default='''{"language":["python","java"],"scan_type":"full_scan"}''',
                                         editable=False)
    scan_notification_config_json = models.TextField(blank=True, null=True, default='''{}''')

    class Meta:
        verbose_name_plural = "4. Scans"
