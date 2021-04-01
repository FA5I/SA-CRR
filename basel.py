import math

from typing import List
from datetime import datetime
from derivatives import Derivative, Swap, Swaption
from helpers import *
from functools import reduce
from collections import defaultdict


class Basel:
    def calc_RC(self, derivatives: List[Derivative], c: float = 0) -> float:
        """This function returns replacement cost. 
        It takes in a list of derivatives, and a haircut value to be applied to the net value of the derivatives.
        More details on page 6 of BCBS279.
        """
        result = reduce(lambda accum, deriv: accum +
                        deriv.market_value, derivatives, 0)
        return max(result/1000 - c, 0)

    def calc_multiplier(self, lst: List[Derivative], add_on_agg: float, floor: float = 0.05, c: float = 0) -> float:
        """This function returns the add_on multiplier. 
        It takes in a list of derivatives, a floor value and a haircut value to be applied to the net value of the derivatives.
        More details on page 8 of BCBS279.
        """
        num = reduce(lambda accum, deriv: accum +
                     deriv.market_value, lst, 0) - c
        denom = 2 * (1 - floor) * add_on_agg
        val = floor + (1 - floor) * math.exp(num/denom)
        return min(1, val)

    def calc_hedging_set_effective_notional(self, lst: List[Derivative]) -> defaultdict(lambda: defaultdict(list)):
        """This function returns a dict which contains the effective notionals per hedging basket. 
        It takes in a list of derivatives.
        More details on page 14 of BCBS279.
        """
        d = defaultdict(lambda: defaultdict(list))
        for deriv in lst:
            d[deriv.base_currency][deriv.calc_maturity_bucket()].append(
                deriv.calc_effective_notional())
        return d

    def aggregate_hedging_set(self, d: defaultdict(lambda: defaultdict(list))) -> dict:
        """This function returns a dict which contains the effective notionals per hedging basket. 
        It takes in a list of derivatives.
        More details on page 14 of BCBS279.
        """
        notionals = dict.fromkeys(d.keys(), 0)

        for currency in d.keys():
            bucket_1 = sum(d[currency].get(1) or [0])
            bucket_2 = sum(d[currency].get(2) or [0])
            bucket_3 = sum(d[currency].get(3) or [0])

            sum_sq = math.pow(bucket_1, 2) + math.pow(bucket_2,
                                                      2) + math.pow(bucket_3, 2)

            sum_avg = 1.4 * bucket_1 * bucket_2 + 1.4 * \
                bucket_2 * bucket_3 + 0.4 * bucket_1 * bucket_3

            notionals[currency] = math.sqrt(sum_sq + sum_avg)

        return notionals

    def calc_addon_ir(self, notionals: dict, sf: float = 0.005) -> float:
        """This function returns the add on value given a dict that maps hedging basket currencies 
        to derivatives by maturity bucket. 
        It takes in a dict of hedging basket currencies to derivatives by maturity bucket.
        More details on page 14 of BCBS279.
        """
        total = 0
        for _, notional in notionals.items():
            total += sf * notional
        return total

    def calc_EAD(self, file_name: str, alpha: float = 1.4) -> float:
        """This function returns the EAD. It takes in a file name and an alpha value.
        More details on page 4 of BCBS279.
        """
        json = read_json_file(file_name)

        lst = []
        for data in json['data']:
            if data.get('type') == 'vanilla_swap':
                lst.append(Swap(data))
            elif data.get('type') == 'swaption':
                lst.append(Swaption(data))
            else:
                raise NotImplementedError(
                    'This code is only working for vanilla swaps and swaptions')

        rc = self.calc_RC(lst)
        notionals = self.aggregate_hedging_set(
            self.calc_hedging_set_effective_notional(lst))
        add_on = self.calc_addon_ir(notionals)
        m = self.calc_multiplier(lst, add_on)
        return alpha * (rc + m * add_on)
