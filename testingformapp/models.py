from uuid import uuid4
from datetime import date, time, datetime
from django.db import models
from django.db.models import Count
from django.core.exceptions import ValidationError

from testingformapp.managers import MenuManager

class Menu(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    day = models.DateField(unique=True, default=date.today)

    close_time = models.TimeField(default=time(11))

    objects = MenuManager()

    @property
    def is_closed(self):
        return self.close_time < datetime.now().time()

    @property
    def options(self):
        return self.option_set.all()
    
    @property
    def options_count(self):
        return self.option_set.count()

    @property
    def orders(self):
        return Order.objects.filter(option__in=self.option_set.values_list('id', flat=True)).order_by('id')
    
    @property
    def orders_count(self):
        return self.option_set.aggregate(Count('order')).get('order__count')

    def __str__(self):
        return '{}'.format(self.day)


class Option(models.Model):
    menu = models.ForeignKey(Menu)
    name = models.CharField(max_length=255)

    @property
    def orders(self):
        return self.order_set.all()

    @property
    def orders_count(self):
        return self.order_set.count()

    def __str__(self):
        return self.name
 

class Order(models.Model):
    option = models.ForeignKey(Option)
    observation = models.TextField(null=True, blank=True)

    def clean(self):
        if self.option.menu.is_closed:
            raise ValidationError('Menu is closed')

    def __str__(self):
        return self.option.name