import json
import unittest
from typing import List
from functools import reduce
import math

from datetime import datetime
from dateutil.relativedelta import relativedelta
from scipy.stats import norm

from collections import defaultdict
from helpers import *


class Derivative:
    def __init__(self, json: dict):
        self.data = json
        self.id = json.get('id')
        self.type = json.get('type')
        self.asset_class = json.get('asset_class')
        self.market_value = json.get('mtm_dirty')
        self.base_currency = json.get('currency_code')
        self.current_date = json.get('date')
        self.start_date = json.get('start_date')
        self.end_date = json.get('end_date')

    def print_data(self):
        print(self.data)

    def calc_S(self) -> float:
        """For interest rate and credit derivatives, this function returns the start date S, 
        of the time period referenced by an interest rate or credit contract. More details on page 9 of BCBS279.
        """
        start_date = parse_time_string(self.start_date)
        current_date = parse_time_string(self.current_date)
        if current_date >= start_date:
            return 0
        else:
            return abs(relativedelta(current_date, start_date).years)

    def calc_E(self) -> float:
        """For interest rate and credit derivatives, this function returns the end date E of the time period 
        referenced by an interest rate or credit contract. More details on page 9 of BCBS279.
        """
        end_date = parse_time_string(self.end_date)
        current_date = parse_time_string(self.current_date)
        return abs(relativedelta(current_date, end_date).years)

    def calc_M(self) -> float:
        """For all asset classes, the maturity M of a contract is the latest date when the contract may still
        be active. This function returns M. More details on page 9 of BCBS279.
        """
        M = None
        if self.type == 'vanilla_swap':
            M = self.calc_E()
        elif self.type == 'swaption':
            last_exercise_date = parse_time_string(self.last_exercise_date)
            current_date = parse_time_string(self.current_date)
            M = abs(relativedelta(current_date, last_exercise_date).years)
        else:
            raise NotImplementedError(
                'This function has only been implemented for vanilla swap and swaption cases.')
        return M

    def calc_supervisory_duration(self) -> float:
        """This function returns the supervisory duration for a derivative. More details on page 10 of BCBS279.
        """
        S = self.calc_S()
        E = self.calc_E()
        a = math.exp(-0.05 * S)
        b = math.exp(-0.05 * E)
        sd = (a - b) / 0.05
        return sd

    def calc_maturity_factor_unmargined(self):
        """This function returns the unmargined maturity factor for a derivative. More details on page 13 of BCBS279.
        """
        m = self.calc_M()
        return math.sqrt(min(m, 1)/1)

    def calc_effective_notional(self):
        """This function returns effective notional for the deriative. More details on page 23 of BCBS279.
        NOTE: This function is only implemented for vanilla swaps and swaptions.
        """
        if self.type != 'vanilla_swap' and self.type != 'swaption':
            raise NotImplementedError(
                'This function is only implemented for vanilla swaps and swaptions')
        sd = self.calc_supervisory_duration()
        delta = self.calc_supervisory_delta()
        mf = self.calc_maturity_factor_unmargined()
        return delta * self.notional_amount * sd * mf

    def calc_supervisory_delta(self, sigma: float = 0.5) -> float:
        """This function returns supervisory delta for the deriative. More details on page 11 of BCBS279.
        NOTE: it is not implemented for CDOs
        """
        if self.type != 'option' and self.type != 'swaption' and self.type != 'cdo':
            return self.primary_risk_direction()

        elif self.type == 'option' or self.type == 'swaption':
            current_date = parse_time_string(self.current_date)
            last_exercise_date = parse_time_string(self.last_exercise_date)
            T = abs(relativedelta(current_date, last_exercise_date).years)
            P = self.underlying_price
            K = self.strike_price
            num = math.log(P/K) + 0.5 * math.pow(sigma, 2) * T
            denom = sigma * math.sqrt(T)
            coeff = 1 if self.leg_type == 'call' else -1
            return self.primary_risk_direction() * norm.cdf(coeff * num/denom)

        else:
            raise NotImplementedError(
                'CDO branch has not been implemented for this function')

    def calc_maturity_bucket(self):
        """This function returns supervisory delta for the deriative. More details on page 29 of BCBS279.
        """
        E = self.calc_E()
        if E < 1:
            return 1
        if 1 <= E and E <= 5:
            return 2
        if E > 5:
            return 3


class Swap(Derivative):
    def __init__(self, json: dict):
        super(Swap, self).__init__(json)
        self.notional_amount = json.get('notional_amount')
        self.payment_type = json.get('payment_type')
        self.receive_type = json.get('receive_type')

    def primary_risk_direction(self) -> int:
        if self.receive_type == 'floating':
            return 1
        else:
            return -1


class Swaption(Swap):
    def __init__(self, json: dict):
        super(Swaption, self).__init__(json)
        self.last_exercise_date = json.get('last_exercise_date')
        self.underlying_price = json.get('underlying_price')
        self.strike_price = json.get('strike')
        self.leg_type = json.get('leg_type')
