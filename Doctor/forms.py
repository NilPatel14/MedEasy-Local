from django import forms
from .models import *






IPD_OPD = (
    ('IPD','IPD'),
    ('OPD','OPD'),
)
frequency_list = (
    ('1 Time a day','1 Time a day'),
    ('2 Times a day','2 Times a day'),
    ('3 Times a day','3 Times a day'),
    ('1 Time in a two day','1 Time in a two day'),
)

class Prescription_Form(forms.ModelForm):
    # gender = forms.CharField(
    #     widget=forms.RadioSelect(
    #         choices=GENDER_LIST,
    #         attrs={
    #             'class': 'form-check-inline',
    #             'type' : 'radio'

    #         }
    #     )
    # )
    frequency = forms.CharField(
        widget=forms.Select(
            choices=frequency_list,
            attrs={
                'class': 'form-control',
                'type' : 'select',
            }
        )
    )
    ipd_opd = forms.CharField(
        widget=forms.Select(
            choices=IPD_OPD,
            attrs={
                'class': 'form-control',
                'type' : 'select',
                }
        )
    )


    class Meta:
        model = Prescription
        fields = ['patient_name','patient_age','gender','problem','diagnosis','medication','duration','frequency','prescription_details','ipd_opd','appointment_id']
        widgets = {
            # 'prescription_id': forms.TextInput(attrs={'class': 'form-control large-textbox','readonly':'readonly'},),
            'patient_name': forms.TextInput(attrs={'class': 'form-control large-textbox','readonly':'readonly'}),
            'patient_age': forms.TextInput(attrs={'class': 'form-control large-textbox','readonly':'readonly'}),
            'gender': forms.TextInput(attrs={'class': 'form-control large-textbox','readonly':'readonly'}),
            'problem': forms.TextInput(attrs={'class': 'form-control large-textbox','readonly':'readonly'}),
            'diagnosis': forms.TextInput(attrs={'class': 'form-control large-textbox',}),
            'medication': forms.TextInput(attrs={'class': 'form-control large-textbox',}),
            'duration': forms.TextInput(attrs={'class': 'form-control large-textbox',}),
            'frequency': forms.Select(attrs={'class': 'radio-group',}),
            'prescription_details': forms.Textarea(attrs={'class': 'form-control large-textbox',}),
            'ipd_opd': forms.Select(attrs={'class': 'radio-group',}),
            # 'appointment_id': forms.TextInput(attrs={'class': 'form-control large-textbox',}),


        }
    appointment_id = forms.ModelChoiceField(queryset=Appointment.objects.all())