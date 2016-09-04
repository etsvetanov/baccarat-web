from base.models import Options
from django.forms import ModelForm, IntegerField
from django.forms.widgets import TextInput, Select, CheckboxInput


INPUT_CLASSES = 'form-control preview centered_input'


# redefining NumberInput is a hack. It's necessary because the "min" attribute
# in "attrs" wasn't applied properly (no idea why).
# see: http://stackoverflow.com/questions/24743438/cannot-overwrite-step-attribute-of-numberinput-field-in-django
class NumberInput(TextInput):
    input_type = 'number'

    def get_class(self):
        return self.__class__



class OptionsForm(ModelForm):
    class Meta:
        model = Options
        exclude = ['user']

        step = IntegerField(min_value=2, max_value=11)

        widgets = {
            'starting_bet': TextInput(attrs={
                'min': 0.1,
                'max': 100,
                'step': 0.1,
                'class': INPUT_CLASSES
            }),
            'step': TextInput(attrs={
                'min': 2,
                'max': 10,
                'step': 1,
                'class': INPUT_CLASSES
            }),
            'pairs': TextInput(attrs={
                'min': 1,
                'max': 100,
                'step': 1,
                'class': INPUT_CLASSES
            })
        }




