# -*- coding: utf-8 -*-
import json
import random
import string
import sys

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Generates promo-code for specified group"

    DEFAULT_FILENAME = "codes.json"

    def add_arguments(self, parser):
        parser.add_argument(
            "--amount",
            type=lambda x: (int(x) > 0) and int(x) or sys.exit("Minimum amount is 1"),
            help="Number of promo-codes to be created",
        )
        parser.add_argument("--group", type=str, help="Group name")
        parser.add_argument("--filename", type=str, help="Result file")

    def handle(self, *args, **options):

        options["group"] = self._handle_group_name(options["group"])

        filename = options.get("filename") or self.DEFAULT_FILENAME

        self.codes = {}
        codes_file = settings.BASE_DIR.joinpath(f"codes_generator/results/{filename}")
        codes_file.parent.mkdir(parents=True, exist_ok=True)

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
            json.dump(self.codes, f, ensure_ascii=False)

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully generated {options["amount"]} code(s)'
                f' for group "{options["group"]}"'
            )
        )
        self.stdout.write(self.style.SUCCESS(f"Result: {codes_file.absolute()}"))

    def _generate_code(self) -> str:
        """Generates random A-Za-z0-9{10} code."""
        letters = string.ascii_letters + string.digits
        return "".join(random.choice(letters) for i in range(10))  # nosec

    def _check_if_code_exists(self, code: str) -> bool:
        for group in self.codes.keys():
            for existing_code in self.codes[group]:
                if code == existing_code:
                    return True
        return False

    def _handle_group_name(self, group_name: str) -> str:
        """Prepares group name from argument to be saved appropriately in JSON.
        1) Remove single or double quotes arount group name
        """
        if group_name.startswith('"') and group_name.endswith('"'):
            return group_name[1:-1]
        if group_name.startswith("'") and group_name.endswith("'"):
            return group_name[1:-1]
        return group_name
