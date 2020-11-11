from django.contrib import admin

# Register your models here.
from .models import Company, CompanyComment, Employee, Employer, JobOpportunity, OpportunityComment, Resume, City, \
    JobCategory

admin.site.register(Company)
admin.site.register(CompanyComment)
admin.site.register(Employee)
admin.site.register(Employer)
admin.site.register(JobOpportunity)
admin.site.register(OpportunityComment)
admin.site.register(Resume)
admin.site.register(City)
admin.site.register(JobCategory)
