import unittest
from core import calculate_tax

class TestCoreFinancial(unittest.TestCase):
    def test_tax_ny(self):
        self.assertEqual(calculate_tax(100.0, "NY"), 8.875, "NY tax rate (8.875%) failed")

    def test_tax_ca(self):
        self.assertEqual(calculate_tax(100.0, "CA"), 7.25, "CA tax rate (7.25%) failed")

if __name__ == '__main__':
    unittest.main()
