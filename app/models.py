from django.db import models

from django.conf import settings


class Company(models.Model):
    name = models.CharField(max_length=40)
    website = models.URLField(null=True)
    logo = models.ImageField(upload_to='company_logo', null=True)
    description = models.TextField(null=True)
    phone = models.CharField(max_length=15, null=True)

    def __str__(self):
        return self.name


class Employer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='employer_user')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='employer')

    def __str__(self):
        return self.user.username


class Employee(models.Model):
    CERTIFICATE_CHOICES = (
        ('D', 'diploma'),
        ('BA', 'bachlor'),
        ('MA', 'master'),
        ('PHD', 'phd'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='employee_user')
    default_resume = models.FileField(null=True, upload_to='resume')
    phone = models.CharField(max_length=15, null=True)
    degree = models.CharField(max_length=5, null=True, choices=CERTIFICATE_CHOICES)

    def __str__(self):
        return self.user.username


class City(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class JobCategory(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class JobOpportunity(models.Model):
    GENDER_CHOICS = (
        ('خانم', 'خانم'),
        ('آقا', 'آقا'),
    )
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='opportunity')
    title = models.CharField(max_length=50)
    description = models.TextField()
    created_at = models.DateField(auto_now=True)
    image = models.ImageField(upload_to='opportunity_img', null=True)
    category = models.ForeignKey(JobCategory, null=True, related_name='category_job')
    city = models.ForeignKey(City, null=True, related_name='city_job')
    gender = models.CharField(null=True, max_length=20, choices=GENDER_CHOICS)

    def __str__(self):
        return self.title


class Resume(models.Model):
    STATUS_CHOICES = (
        ('F', 'مناسب برای آینده'),
        ('A', 'قبول'),
        ('R', 'رد'),
        ('W', 'در انتظار پاسخ'),
    )
    opportunity = models.ForeignKey(JobOpportunity, on_delete=models.CASCADE, related_name='r_opportunity')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='r_employee')
    resume = models.FileField(upload_to='job_resume')
    salary = models.IntegerField(null=True)
    description = models.CharField(max_length=100, null=True)
    created_at = models.DateField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="W")


class CompanyComment(models.Model):
    user = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='cc_user')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='cc_company')
    text = models.TextField()
    created_at = models.DateField(auto_now=True)


class OpportunityComment(models.Model):
    user = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='oc_user')
    opportunity = models.ForeignKey(JobOpportunity, on_delete=models.CASCADE, related_name='oc_opportunity')
    text = models.TextField()
    created_at = models.DateField(auto_now=True)
