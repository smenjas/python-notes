import unittest
from debt import get_max_unsecured_debt_ratio

class TestDebt(unittest.TestCase):
    def test_types(self):
        self.assertRaises(TypeError, get_max_unsecured_debt_ratio, 1+1j)
        self.assertRaises(TypeError, get_max_unsecured_debt_ratio, "")
        self.assertRaises(TypeError, get_max_unsecured_debt_ratio, (1,))
        self.assertRaises(TypeError, get_max_unsecured_debt_ratio, [])
        self.assertRaises(TypeError, get_max_unsecured_debt_ratio, set())
        self.assertRaises(TypeError, get_max_unsecured_debt_ratio, {})

    def test_debt_ratios(self):
        self.assertAlmostEqual(get_max_unsecured_debt_ratio(-1), 0)
        self.assertAlmostEqual(get_max_unsecured_debt_ratio(0), 0)
        self.assertAlmostEqual(get_max_unsecured_debt_ratio(1), 0)
        self.assertAlmostEqual(get_max_unsecured_debt_ratio(40000), 0)
        self.assertAlmostEqual(get_max_unsecured_debt_ratio(41000), 0.505/3)
        self.assertAlmostEqual(get_max_unsecured_debt_ratio(60000), 0.2)
        self.assertAlmostEqual(get_max_unsecured_debt_ratio(90000), 0.25)
        self.assertAlmostEqual(get_max_unsecured_debt_ratio(120000), 0.3)
        self.assertAlmostEqual(get_max_unsecured_debt_ratio(170000), 1.15/3)
        self.assertAlmostEqual(get_max_unsecured_debt_ratio(180000), 0.4)
        self.assertAlmostEqual(get_max_unsecured_debt_ratio(float('inf')), 0.4)
