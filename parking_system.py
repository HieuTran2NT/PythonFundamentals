import re
import os
from datetime import datetime, timedelta, time
from decimal import Decimal

class ParkingRate:
    rate_table = {
        'Sunday': {
            '08:00-16:59': {'max_hours': 8, 'rate': 2.00},
            '17:00-23:59': {'max_hours': None, 'rate': 5.00},
            '00:00-07:59': {'max_hours': None, 'rate': 20.00, 'flat': True}
        },
        'Monday': {
            '08:00-16:59': {'max_hours': 2, 'rate': 10.00},
            '17:00-23:59': {'max_hours': None, 'rate': 5.00},
            '00:00-07:59': {'max_hours': None, 'rate': 20.00, 'flat': True}
        },
        'Tuesday': {
            '08:00-16:59': {'max_hours': 2, 'rate': 10.00},
            '17:00-23:59': {'max_hours': None, 'rate': 5.00},
            '00:00-07:59': {'max_hours': None, 'rate': 20.00, 'flat': True}
        },
        'Wednesday': {
            '08:00-16:59': {'max_hours': 2, 'rate': 10.00},
            '17:00-23:59': {'max_hours': None, 'rate': 5.00},
            '00:00-07:59': {'max_hours': None, 'rate': 20.00, 'flat': True}
        },
        'Thursday': {
            '08:00-16:59': {'max_hours': 2, 'rate': 10.00},
            '17:00-23:59': {'max_hours': None, 'rate': 5.00},
            '00:00-07:59': {'max_hours': None, 'rate': 20.00, 'flat': True}
        },
        'Friday': {
            '08:00-16:59': {'max_hours': 2, 'rate': 10.00},
            '17:00-23:59': {'max_hours': None, 'rate': 5.00},
            '00:00-07:59': {'max_hours': None, 'rate': 20.00, 'flat': True}
        },
        'Saturday': {
            '08:00-16:59': {'max_hours': 4, 'rate': 3.00},
            '17:00-23:59': {'max_hours': None, 'rate': 5.00},
            '00:00-07:59': {'max_hours': None, 'rate': 20.00, 'flat': True}
        }
    }

    @staticmethod
    def get_time_slot(hour_minute):
        if time(8, 0) <= hour_minute <= time(16, 59):
            return '08:00-16:59'
        elif time(17, 0) <= hour_minute <= time(23, 59):
            return '17:00-23:59'
        else:
            return '00:00-07:59'

    @classmethod
    def calculate_fee(cls, arrival_time, current_time, has_discount=False):
        total_fee = Decimal('0.00')
        time_cursor = arrival_time

        while time_cursor < current_time:
            day_name = time_cursor.strftime("%A")
            time_slot = cls.get_time_slot(time_cursor.time())
            rate_info = cls.rate_table[day_name][time_slot]

            if rate_info.get('flat'):
                fee = Decimal(str(rate_info['rate']))
            else:
                fee = Decimal(str(rate_info['rate']))
                if time_slot == '17:00-23:59':
                    midnight = datetime.combine(time_cursor.date(), time(23, 59))
                    max_hours = (midnight - time_cursor).total_seconds() / 3600
                else:
                    max_hours = rate_info['max_hours']
                if max_hours is not None and (current_time - arrival_time).total_seconds() / 3600 > max_hours:
                    fee *= 2

            if has_discount:
                if time_slot in ['17:00-23:59', '00:00-07:59']:
                    fee *= Decimal('0.5')
                else:
                    fee *= Decimal('0.9')

            total_fee += fee
            time_cursor += timedelta(hours=1)

        return round(total_fee, 2)

class Validator:
    @staticmethod
    def is_valid_datetime(dt_str):
        try:
            datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
            return True
        except ValueError:
            return False

    @staticmethod
    def is_valid_car_identity(car_id):
        return re.match(r'^\d{2}[A-Z]-\d{5}$', car_id) is not None

    @staticmethod
    def calculate_modulo11_check_digit(number):
        digits = [int(d) for d in str(number)]
        weights = list(range(2, 2 + len(digits)))[::-1]
        total = sum(d * w for d, w in zip(digits, weights))
        remainder = total % 11
        return (11 - remainder) % 11

    @staticmethod
    def is_valid_frequent_number(fp_number):
        if not re.match(r'^\d{5}$', fp_number):
            return False
        base = fp_number[:-1]
        check_digit = int(fp_number[-1])
        return Validator.calculate_modulo11_check_digit(base) == check_digit

class ParkingSystem:
    def __init__(self):
        self.records_file = "parking_records.txt"
        self.history_file = "payment_history.txt"
        self.excess_file = "excess_payments.txt"

    def park(self, arrival_time_str, car_identity, fp_number="N/A"):
        if not Validator.is_valid_datetime(arrival_time_str):
            raise ValueError("Invalid datetime format.")
        if not Validator.is_valid_car_identity(car_identity):
            raise ValueError("Invalid car identity format.")
        if fp_number != "N/A" and not Validator.is_valid_frequent_number(fp_number):
            raise ValueError("Invalid frequent parking number.")

        with open(self.records_file, "a") as f:
            f.write(f"{arrival_time_str},{car_identity},{fp_number}\n")

    def history(self, car_identity):
        total_payment = Decimal('0.00')
        available_credits = Decimal('0.00')
        history = []

        if os.path.exists(self.history_file):
            with open(self.history_file, "r") as f:
                for line in f:
                    parts = line.strip().split(",")
                    if len(parts) == 4 and parts[0] == car_identity:
                        arrival, departure, fee = parts[1], parts[2], Decimal(parts[3])
                        total_payment += fee
                        history.append((arrival, departure, fee))

        if os.path.exists(self.excess_file):
            with open(self.excess_file, "r") as f:
                for line in f:
                    parts = line.strip().split(",")
                    if len(parts) == 2 and parts[0] == car_identity:
                        try:
                            available_credits += Decimal(parts[1])
                        except:
                            continue

        report_filename = f"{car_identity}.txt"
        with open(report_filename, "w") as f:
            f.write(f"Total payment: ${total_payment:.2f}\n")
            f.write(f"Available credits: ${available_credits:.2f}\n")
            f.write("Parked Dates:\n")
            for arrival, departure, fee in history:
                f.write(f"{arrival} – {departure} ${fee:.2f}\n")

        return report_filename

    def get_parking_details(self, car_identity):
        if not Validator.is_valid_car_identity(car_identity):
            raise ValueError("Invalid car identity format.")

        found = False
        arrival_time = None
        fp_number = "N/A"

        if not os.path.exists(self.records_file):
            raise FileNotFoundError("No parking records found.")

        with open(self.records_file, "r") as f:
            lines = f.readlines()

        for line in lines:
            parts = line.strip().split(",")
            if len(parts) >= 2 and parts[1] == car_identity:
                arrival_time = parts[0]
                fp_number = parts[2] if len(parts) > 2 else 'N/A'
                found = True
                break

        if not found:
            raise ValueError("Car identity not found in records.")

        return arrival_time, fp_number

    def calculate_fee_only(self, car_identity, current_time_str):
        if not Validator.is_valid_datetime(current_time_str):
            raise ValueError("Invalid current time format.")

        arrival_time_str, fp_number = self.get_parking_details(car_identity)

        has_discount = fp_number != 'N/A' and Validator.is_valid_frequent_number(fp_number)
        fee = ParkingRate.calculate_fee(
            datetime.strptime(arrival_time_str, "%Y-%m-%d %H:%M"),
            datetime.strptime(current_time_str, "%Y-%m-%d %H:%M"),
            has_discount
        )
        return fee

    def process_payment(self, car_identity, current_time_str, payment_amount):
        fee = Decimal(str(self.calculate_fee_only(car_identity, current_time_str))) # Ensure fee is Decimal

        # Convert payment_amount to Decimal
        payment_amount = Decimal(str(payment_amount))

        if payment_amount < fee:
            raise ValueError("Payment is less than the required fee.")
        excess = payment_amount - fee
        if excess > 0:
            with open(self.excess_file, "a") as ef:
                ef.write(f"{car_identity},{excess:.2f}\n")

        arrival_time_str, _ = self.get_parking_details(car_identity)
        with open(self.history_file, "a") as ph:
            ph.write(f"{car_identity},{arrival_time_str},{current_time_str},{fee:.2f}\n")

        return fee, excess

