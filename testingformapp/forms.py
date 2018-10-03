from django.forms import inlineformset_factory, ModelForm, ModelChoiceField

from testingformapp.models import Menu, Option, Order

OptionFormSet = inlineformset_factory(Menu, Option, fields=('name',))

class MenuForm(ModelForm):
    class Meta(object):
        model = Menu
        fields = ('day', 'close_time',)

class OrderForm(ModelForm):
    def __init__(self, *args, **kwargs):
        menu = kwargs.pop('menu')

        super(OrderForm, self).__init__(*args, **kwargs)

        self.fields['option'].queryset = menu.options

    class Meta(object):
        model = Order
        fields = ('option', 'observation',)