from datetime import date
from django.db.models import Manager


class MenuManager(Manager):
    def has_daily_menu(self):
        return not not (self
            .get_queryset()
            .filter(day=date.today())
            .count())
    
    def get_daily_menu(self):
        return self.get_queryset().filter(day=date.today()).first()