from django.core.management import BaseCommand
from django.conf import settings

import os


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('filename', type=str, nargs='?', help='Name of the file to be decoded')

    def handle(self, *args, **options):
        filename = os.path.join(settings.BASE_DIR, options.get('filename', None))
        split_filename = os.path.splitext(filename)
        try:
            open(f"{split_filename[0]}-new{split_filename[1]}", "wb").write(
                # str(open(filename, "r", encoding='unicode_escape').read()).replace('=\"', '\u003D\u005C\u0022')
                #     .replace('\">', '\u005C\u0022\u003E').encode('utf-8')
                # str(open(filename, "r", encoding='unicode_escape').read()).replace('=\"', '\u003D\u0022')
                #     .replace('\">', '\u0022\u003E').encode('utf-8')
                str(open(filename, "r").read()).replace('=\"', '\u003D\u0022')
                    .replace('\">', '\u0022\u003E').encode('utf-8')
            )
        except TypeError:
            self.stdout.write("Error: not filename")
# python manage.py dumpdata main.Paradox --indent 2 --format yaml > paradox.yaml
