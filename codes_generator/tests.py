# -*- coding: utf-8 -*-

import json
from io import StringIO

from django.conf import settings
from django.core.management import call_command
from django.test import TestCase


class GenerateCodeTest(TestCase):
    def setUp(self):
        codes_file = settings.BASE_DIR.joinpath("codes_generator/results/test.json")
        if codes_file.exists():
            codes_file.unlink()

    def test_generate_code_command_result(self):
        out = StringIO()

        call_command(
            "generate_codes",
            "--amount=10",
            "--group='агенства'",
            "--filename=test.json",
            stdout=out,
        )
        call_command(
            "generate_codes",
            "--amount=1",
            "--group='агенства'",
            "--filename=test.json",
            stdout=out,
        )
        call_command(
            "generate_codes",
            "--amount=42",
            "--group='avtostop'",
            "--filename=test.json",
            stdout=out,
        )
        call_command(
            "generate_codes",
            "--amount=5",
            "--group=1",
            "--filename=test.json",
            stdout=out,
        )

        # проверяем результат на соответствие

        codes_file = settings.BASE_DIR.joinpath("codes_generator/results/test.json")
        self.assertTrue(codes_file.exists())

        with open(codes_file, "r") as f:
            codes = json.load(f)

        self.assertIn("агенства", codes)
        self.assertEqual(len(codes["агенства"]), 11)
        self.assertIn("avtostop", codes)
        self.assertEqual(len(codes["avtostop"]), 42)
        self.assertIn("1", codes)
        self.assertEqual(len(codes["1"]), 5)

    def tearDown(self):
        codes_file = settings.BASE_DIR.joinpath("codes_generator/results/test.json")
        if codes_file.exists():
            codes_file.unlink()
