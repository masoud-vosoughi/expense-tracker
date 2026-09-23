import unittest
import json
from pathlib import Path
from tempfile import TemporaryDirectory

from storage import load_data, save_data


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
            
    def test_save_data_creates_json_file(self):
        with TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir)/"expenses.json"
            
            data = {
            "expenses": [],
            "last_id": 5
            }
            
            save_data(file_path, data)
            
            with file_path.open("r") as file:
                saved_data = json.load(file)
            self.assertEqual(saved_data, data)