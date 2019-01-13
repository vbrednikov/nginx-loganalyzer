import unittest
from decimal import Decimal

from nginx_loganalyzer import median


class TestMedian(unittest.TestCase):
    def test_median_empty(self):
        self.assertIsNone(median([]))

    def test_median_1_element(self):
        self.assertEqual(median([1]), 1)

    def test_median_2_elements(self):
        self.assertEqual(median([1, 2]), 1.5)

    def test_median_wages_case_even(self):
        self.assertEqual(median([Decimal(x)
                                 for x in
                                 '1, 2, 1.5, 2, 3, 2.2, 2.1, 10000'.split(',')
                                 ]
                                ), Decimal('2.05'))

    def test_median_wages_case_odd(self):
        self.assertEqual(median([1, 1.9, 2, 1.5, 4, 3, 2.2, 2.1, 10000]), 2.1)

    def test_median_decimal(self):
        data = [Decimal(x)
                for x in
                '0.390 0.133 0.199 0.704 0.146 0.628 0.067 0.138 0.003 0.157'.split()
                ]
        self.assertEqual(median(data), Decimal('0.1515'))


if __name__ == '__main__':
    unittest.main()
