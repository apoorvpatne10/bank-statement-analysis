from django import forms
from .models import Fraud

class MyForm(forms.Form):
    current_account_list = list(Fraud.objects.values_list('acc_no', flat=True).distinct())
    # CHOICES = tuple(enumerate(current_account_list, start=1))
    # choices_new = []
    # for x, y in CHOICES:
    #     choices_new.append((y, y))
    # choices_new = tuple(choices_new)

# [409000611074 409000493201 409000425051 409000405747 409000438611
#  409000493210 409000438620      1196711      1196428 409000362497]

    CHOICES = (
        (409000611074, 409000611074),
        (409000493201, 409000493201),
        (409000425051, 409000425051),
        (409000405747, 409000405747),
        (409000438611, 409000438611),
        (409000493210, 409000493210),
        (409000438620, 409000438620),
        (1196711, 1196711),
        (1196428, 1196428),
        (409000362497, 409000362497),
    )

    account_choice = forms.ChoiceField(choices=CHOICES)
