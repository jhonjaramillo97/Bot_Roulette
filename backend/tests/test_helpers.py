"""
Tests para logic_helpers.py y helpers.py: utilidades compartidas.
"""
import pytest
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.roulette.logic_helpers import extract_numero, nums_to_emoji, KEYCAP_MAP


class TestExtractNumero:
    def test_from_dict_with_numero_key(self):
        assert extract_numero({"numero": 5}) == 5

    def test_from_dict_missing_numero_key(self):
        item = {"otro": 10}
        assert extract_numero(item) == item

    def test_from_int(self):
        assert extract_numero(42) == 42

    def test_from_sqlite_row(self):
        class FakeRow:
            def __getitem__(self, key):
                if key == "numero":
                    return 7
                raise KeyError(key)
        assert extract_numero(FakeRow()) == 7

    def test_from_sqlite_row_missing_numero(self):
        class FakeRow:
            def __getitem__(self, key):
                raise KeyError(key)
        row = FakeRow()
        assert extract_numero(row) == row


class TestNumsToEmoji:
    def test_basic_numbers(self):
        result = nums_to_emoji([1, 2, 3])
        assert result != ""

    def test_number_ten(self):
        items = [{"numero": 10}, {"numero": 5}]
        result = nums_to_emoji(items)

    def test_empty_list(self):
        result = nums_to_emoji([])
        assert result == ""

    def test_more_than_ten_limits(self):
        numeros = list(range(20))
        result = nums_to_emoji(numeros)
        parts = result.split(" ")
        assert len(parts) <= 10

    def test_mixed_int_and_dict(self):
        items = [1, {"numero": 2}, 3]
        result = nums_to_emoji(items)
        assert len(result) > 0


class TestKeycapMap:
    def test_all_digits_mapped(self):
        for d in "0123456789":
            assert d in KEYCAP_MAP
            assert len(KEYCAP_MAP[d]) == 2  # emoji keycap = 2 chars
