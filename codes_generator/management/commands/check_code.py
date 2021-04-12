# -*- coding: utf-8 -*-
import json
import random
import string
import sys

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Checks if code exists in the json file"

    def add_arguments(self, parser):
        parser.add_argument("code", type=str, help="Code to be checked")
        parser.add_argument("--filename", type=str, help="Result file")

    def handle(self, *args, **options):

        filename = options.get("filename") or "codes.json"

        codes_file = settings.BASE_DIR.joinpath(f"codes_generator/results/{filename}")

        if codes_file.exists():

            with open(codes_file) as f:
                self.codes = json.load(f)

            for group in self.codes.keys():
                for existing_code in self.codes[group]:
                    if options["code"] == existing_code:
                        self.stdout.write(
                            self.style.SUCCESS(
                                f'Code "{options["code"]}" found for group "{group}"'
                            )
                        )
                        self.stdout.write(
                            self.style.SUCCESS(f"File: {codes_file.absolute()}")
                        )
                        return

        self.stdout.write(self.style.ERROR(f'Code "{options["code"]}" NOT found'))
        self.stdout.write(self.style.ERROR(f"File: {codes_file.absolute()}"))
