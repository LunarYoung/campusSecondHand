from django import forms

class MyForm(forms.Form):
    username = forms.CharField\
        (max_length=100, min_length=6)

    password = forms.CharField\
        (max_length=100, min_length=6)

class upthingform(forms.Form):

    link = forms.CharField(max_length=50, min_length=1)
    price = forms.CharField(max_length=50, min_length=1)
    detail = forms.CharField(max_length=500, min_length=1)


class upneedform(forms.Form):
    name = forms.CharField(max_length=30, min_length=1)
    price = forms.CharField(max_length=20, min_length=1)
    link = forms.CharField(max_length=100, min_length=1)
    detail = forms.CharField(max_length=220, min_length=1)






