import json

from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from recipes.models import Ingredient, Tag


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--path', help='file path', type=str)

    def handle(self, *args, **options):
        file_path = options['path']

        with open(file_path, encoding='utf-8') as f:
            data = json.load(f)
            if 'measurement_unit' in data[0]:
                for item in data:
                    try:
                        Ingredient.objects.create(
                            name=item['name'],
                            measurement_unit=item['measurement_unit']
                        )
                    except IntegrityError:
                        continue
            else:
                for item in data:
                    Tag.objects.create(
                        name=item['name'],
                        color=item['color'],
                        slug=item['slug']
                    )
