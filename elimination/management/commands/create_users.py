import random
import re

import progressbar
from decouple import config
from django.core.management.base import BaseCommand
from django.db import transaction

from elimination.models import Senior


def get_email_prefix(full_name, student_id):
    names = re.split(' ', full_name)
    end_id = student_id[3:]
    return names[0][0:1].lower() + names[len(names) - 1][0:1].lower() + end_id


def get_initial_password():
    password = ""
    for i in range(0, 5):
        password += chr(random.randint(ord('A'), ord('Z')))
    return password


class Command(BaseCommand):
    def handle(self, *args, **options):
        Senior.objects.all().delete()
        file = open('seniors.csv').read()
        seniors_csv = re.split('\n', file)

        Senior.objects.create_superuser('admin', password=config('SUPERUSER_PASSWORD'),
                                        first_name='Supa',
                                        last_name='Usa')

        with transaction.atomic():
            for senior_csv in progressbar.progressbar(seniors_csv):
                line_csv = re.split(',', senior_csv)
                if len(line_csv) != 2:
                    print('Invalid line:', line_csv)
                if len(line_csv) == 2:
                    full_name = line_csv[0]
                    student_id = line_csv[1]
                    email_prefix = get_email_prefix(full_name, student_id)
                    initial_password = get_initial_password()
                    name_list = re.split(" ", full_name)
                    Senior.objects.create_user(student_id, email_prefix + '@pausd.us', initial_password,
                                               initial_password=initial_password,
                                               first_name=name_list[0],
                                               last_name=name_list[-1])
        # send_email.send_initial_passwords()
