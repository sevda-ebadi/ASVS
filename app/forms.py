from django import forms


class EmployeeSignUpForm(forms.Form):
    firstname = forms.CharField(max_length=20)
    lastname = forms.CharField(max_length=20)
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=15)
    degree = forms.CharField(max_length=5)
    password = forms.CharField(max_length=20)

    def save(self):
        print(self)


class EmployeeSignInForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(max_length=20)


class EditEmployeeInfoForm(forms.Form):
    phone = forms.CharField(max_length=15)
    firstname = forms.CharField(max_length=30)
    lastname = forms.CharField(max_length=30)


class CompanySignUpForm(forms.Form):
    company_name = forms.CharField(max_length=30)
    email = forms.EmailField()
    province = forms.CharField(max_length=20, required=False)
    city = forms.CharField(max_length=20, required=False)
    phone = forms.CharField(max_length=15)
    description = forms.TextInput()
    password = forms.CharField(max_length=30)
    password_confirmation = forms.CharField(max_length=30)
    file = forms.FileField()


class CompanySignInForm(forms.Form):
    username = forms.CharField(max_length=40)
    password = forms.CharField(max_length=40)


class ResumeConfirmationForm(forms.Form):
    resume_id = forms.IntegerField()
    status = forms.CharField(max_length=2)


class EditCompanyInfoForm(forms.Form):
    company_name = forms.CharField(max_length=30)
    phone = forms.CharField(max_length=15)
    email = forms.EmailField()
    description = forms.CharField(max_length=255)


class CreateJobOpportunityForm(forms.Form):
    title = forms.CharField(max_length=30)
    description = forms.CharField(max_length=255)


class CreateResumeForm(forms.Form):
    file = forms.FileField()
    salary = forms.IntegerField()
