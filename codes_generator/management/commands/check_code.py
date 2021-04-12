# -*- coding: utf-8 -*-
import json

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Checks if code exists in the json file"

    DEFAULT_FILENAME = "codes.json"

    def add_arguments(self, parser):
        parser.add_argument("code", type=str, help="Code to be checked")
        parser.add_argument("--filename", type=str, help="Result file")

    def handle(self, *args, **options):

        filename = options.get("filename") or self.DEFAULT_FILENAME

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

        else:

            self.stdout.write(
                self.style.ERROR(f"File with codes NOT exists: {codes_file.absolute()}")
            )
