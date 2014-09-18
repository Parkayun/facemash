from battle.monkey_django_facebook import connect as monkey_connect
from django_facebook import views

views.connect = monkey_connect
