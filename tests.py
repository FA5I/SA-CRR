import unittest
from derivatives import Derivative, Swap, Swaption
from basel import Basel
from helpers import *


test_data1 = read_json_file('test_data_1.json')
test_data2 = read_json_file('test_data_2.json')


class TestHelperFunctions(unittest.TestCase):
    def test_parse_time_string(self):
        time_string = '2017-01-10T00:00:00Z'
        result = isinstance(parse_time_string(time_string), datetime)
        self.assertEqual(result, True)

    def test_calc_replacement_cost_a(self):
        swap1 = Swap(test_data1['data'][0])
        swap2 = Swap(test_data1['data'][1])
        basel = Basel()
        result = basel.calc_RC([swap1, swap2])
        self.assertEqual(result, 0)

    def test_calc_replacement_cost_b(self):
        swap1 = Swap(test_data2['data'][0])
        swap2 = Swap(test_data2['data'][1])
        swap3 = Swap(test_data2['data'][2])
        basel = Basel()
        result = basel.calc_RC([swap1, swap2, swap3])
        self.assertEqual(result, 60)

    def test_calc_supervisory_duration(self):
        swap1 = Swap(test_data2['data'][0])
        swap2 = Swap(test_data2['data'][1])
        swap3 = Swap(test_data2['data'][2])
        self.assertTrue(abs(7.87 - swap1.calc_supervisory_duration()) < 0.01)
        self.assertTrue(abs(3.63 - swap2.calc_supervisory_duration()) < 0.01)
        self.assertTrue(abs(7.49 - swap3.calc_supervisory_duration()) < 0.01)

    def test_primary_risk_direction(self):
        swap1 = Swap(test_data2['data'][0])
        swap2 = Swap(test_data2['data'][1])
        result1 = swap1.primary_risk_direction()
        result2 = swap2.primary_risk_direction()
        self.assertEqual(result1, 1)
        self.assertEqual(result2, -1)

    def test_calc_supervisory_delta(self):
        swaption = Swaption(test_data2['data'][2])
        result = swaption.calc_supervisory_delta()
        self.assertTrue(abs(-0.27 - result) < 0.01)

    def test_calc_maturity_factor_unmargined(self):
        swaption = Swaption(test_data2['data'][2])
        result = swaption.calc_maturity_factor_unmargined()
        self.assertEqual(result, 1)

    def test_calc_effective_notional(self):
        swap = Swap(test_data2['data'][0])
        result = swap.calc_effective_notional()
        self.assertTrue(abs(78694 - result) < 1)

        swap = Swap(test_data2['data'][1])
        result = swap.calc_effective_notional()
        self.assertTrue(abs(36254 + result) < 1)

        swaption = Swaption(test_data2['data'][2])
        result = swaption.calc_effective_notional()
        self.assertTrue(abs(10083 + result) < 1)

    def test_calc_maturity_bucket(self):
        swap1 = Swap(test_data2['data'][0])
        swap2 = Swap(test_data2['data'][1])
        swaption = Swaption(test_data2['data'][2])
        self.assertEqual(swap1.calc_maturity_bucket(), 3)
        self.assertEqual(swap2.calc_maturity_bucket(), 2)
        self.assertEqual(swaption.calc_maturity_bucket(), 3)

    def test_aggregate_hedging_set(self):
        swap1 = Swap(test_data2['data'][0])
        swap2 = Swap(test_data2['data'][1])
        swaption = Swaption(test_data2['data'][2])
        lst = [swap1, swap2, swaption]
        basel = Basel()
        notionals = basel.calc_hedging_set_effective_notional(lst)
        result = basel.aggregate_hedging_set(notionals)
        self.assertTrue(abs(59270 - result['USD']) < 0.1)
        self.assertTrue(abs(10083 - result['EUR']) < 0.1)

    def test_calc_addon_ir(self):
        swap1 = Swap(test_data2['data'][0])
        swap2 = Swap(test_data2['data'][1])
        swaption = Swaption(test_data2['data'][2])
        lst = [swap1, swap2, swaption]
        basel = Basel()
        notionals = basel.aggregate_hedging_set(
            basel.calc_hedging_set_effective_notional(lst))
        result = basel.calc_addon_ir(notionals)
        self.assertTrue(abs(347 - result) < 1)

    def test_calc_EAD(self):
        basel = Basel()
        result = basel.calc_EAD('test_data_2.json')
        self.assertTrue(abs(569 - result) < 1)


if __name__ == '__main__':
    unittest.main()
