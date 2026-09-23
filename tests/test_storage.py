import unittest
import json
from pathlib import Path
from tempfile import TemporaryDirectory

from storage import load_data


class TestStorage(unittest.TestCase):

    def test_load_data_when_file_does_not_exist(self):
        with TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "expenses.json"

            data = load_data(file_path)

            self.assertEqual(data["expenses"], [])
            self.assertEqual(data["last_id"], 0)

    def test_load_data_from_existing_file(self):
        with TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "expenses.json"

            expected_data = {
                "expenses": [],
                "last_id": 3
            }

            with file_path.open("w") as file:
                json.dump(expected_data, file)

            data = load_data(file_path)

            self.assertEqual(data["expenses"], [])
            self.assertEqual(data["last_id"], 3)