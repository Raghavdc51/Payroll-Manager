# from django.apps import AppConfig


# class MyappConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'myapp'


# ✅ File: myapp/apps.py

from django.apps import AppConfig

class MyappConfig(AppConfig):  
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'  

    def ready(self):
        import myapp.signals  