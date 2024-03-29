import random

import progressbar
from django.core.management.base import BaseCommand
from django.db import transaction

from elimination.models import Senior, Elimination


class Command(BaseCommand):
    def handle(self, *args, **options):
        seniors_query = Senior.objects.filter(is_superuser=False)
        seniors = list(seniors_query)
        random.shuffle(seniors)
        with transaction.atomic():
            Elimination.objects.all().delete()
            seniors_query.update(target=None)
            for i in progressbar.progressbar(range(0, len(seniors))):
                senior = seniors[i]
                senior.target = seniors[(i + 1) % len(seniors)]
                senior.save()
        # send_reassign_targets()
