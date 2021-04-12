# -*- coding: utf-8 -*-
import json
import random
import string
from collections import defaultdict

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Generates promo-code for specified group"

    def add_arguments(self, parser):
        parser.add_argument("amount", type=int)
        parser.add_argument("group", type=str)

    def handle(self, *args, **options):

        self.codes = {}
        codes_file = settings.BASE_DIR.joinpath("codes_generator/results/codes.json")

        if codes_file.exists():

            with open(codes_file) as f:
                self.codes = json.load(f)

        for i in range(options["amount"]):
            while True:
                code = self._generate_code()
                if not self._check_if_code_exists(code):

                    if options["group"] not in self.codes:
                        self.codes[options["group"]] = []

                    self.codes[options["group"]].append(code)
                    break

        with open(codes_file, "w") as f:
            json.dump(self.codes, f)

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully generated: {options["amount"]} codes" \
                " for group {options["group"]} '
            )
        )

    def _generate_code(self):
        letters = string.ascii_letters + string.digits
        return "".join(random.choice(letters) for i in range(10))

    def _check_if_code_exists(self, code):
        for group in self.codes.keys():
            for existing_code in self.codes[group]:
                if code == existing_code:
                    return True
        return False
