import unittest

from generatepage import extract_title, generate_pages_recursive

class TestGeneratePage(unittest.TestCase):
    def test_extract(self):
        header = extract_title("# Header")
        self.assertEqual(
            header,
            "Header"
        )