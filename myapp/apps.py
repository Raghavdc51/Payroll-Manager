# from django.apps import AppConfig


# class MyappConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'myapp'


# ✅ File: myapp/apps.py

from django.apps import AppConfig

class MyappConfig(AppConfig):  # 👈 The class name must match your app's folder
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'  # 👈 Make sure this matches your folder name

    def ready(self):
        import myapp.signals  # 👈 This line activates your signal at app startup