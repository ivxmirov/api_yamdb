import csv
import os

from django.apps import apps
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    APP_NAME = 'reviews'
    USERS_APP_NAME = 'users'

    def add_arguments(self, parser):
        parser.add_argument('path_to_files', type=str)

    def determine_model(self, filename):
        _, model_name, _ = filename.split('.')

        app_name = self.APP_NAME
        if model_name == 'customuser':
            app_name = self.USERS_APP_NAME

        try:
            model_class = apps.get_model(app_name, model_name)
            return model_class
        except LookupError:
            print(f"Model '{model_name}' not found in app '{app_name}'")
            return None

    def handle(self, *args, **options):
        path = options['path_to_files']

        for filename in os.listdir(path):
            with open(path + filename, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                class_instance = self.determine_model(filename)
                data = [class_instance(**row) for row in reader]
                class_instance.objects.bulk_create(data)
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Данные для "{class_instance.__name__}" загружены!'
                    )
                )
