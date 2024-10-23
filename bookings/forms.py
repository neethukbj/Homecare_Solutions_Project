from django import forms
from .models import Booking,ProviderAvailability

class BookingForm(forms.Form):
    # work_location = forms.CharField(
    #     label="Work Location",
    #     max_length=100,
    #     widget=forms.TextInput(attrs={
    #         'class': 'form-control',
    #         'placeholder': '',
    #         'id': 'exampleInputText02'
    #     })
    # )
    
    booking_date = forms.DateField(
        label="Booking Date",
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    service_type = forms.ChoiceField(
        label="Service Type*",
        choices=[],  # Empty by default, to be populated dynamically
        widget=forms.Select(attrs={
            'class': 'form-control ',
            
        })
    )
    
    start_time = forms.TimeField(
        label="Start Time*",
        widget=forms.TimeInput(attrs={
            'class': 'form-control',
            'type': 'time',
            'id': 'exampleInputText05'
        })
    )
    
    end_time = forms.TimeField(
        label="End Time*",
        widget=forms.TimeInput(attrs={
            'class': 'form-control',
            'type': 'time',
            'id': 'exampleInputText05'
        })
    )
    
    about_work = forms.CharField(
        label="About Work",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 2,
            'id': 'exampleInputText040'
        })
    )
    
    agree_to_terms = forms.BooleanField(
        label="I agree to the terms and conditions.",
        widget=forms.CheckboxInput(attrs={
            'id': 'termsCheckbox'
        })
    )

    def __init__(self, *args, provider=None, **kwargs):
        service_choices = kwargs.pop('service_choices', [])
        super().__init__(*args, **kwargs)
        self.fields['service_type'].choices = service_choices
        self.provider = provider
    

    class Meta:
        model = Booking
        fields = ['client_name', 'booking_date', 'service_type', 'start_time', 'end_time', 'about_work', 'agree_to_terms']
   

    def clean(self):
        cleaned_data = super().clean()
        booking_date = cleaned_data.get('booking_date')
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        # Fetch provider availability for the selected date
        if self.provider:
            availability = ProviderAvailability.objects.filter(
                provider=self.provider,
                date=booking_date,
                is_available=True,
                start_time__lte=start_time,
                end_time__gte=end_time
            )

            if not availability.exists():
                raise forms.ValidationError(
                    "The provider is not available at the selected time. Please choose a different time slot."
                )

        return cleaned_data

class ProviderAvailabilityForm(forms.ModelForm):
    class Meta:
        model = ProviderAvailability
        fields = ['date', 'start_time', 'end_time', 'is_available']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")

        if start_time and end_time and start_time >= end_time:
            raise forms.ValidationError("End time must be after start time.")

        return cleaned_data  
    