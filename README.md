
# Car Parking System

This car parking system allows customers to manage their parking activities including parking a car, picking up a car, and viewing parking history. The system interacts with users via a command-line interface and stores data in files for persistence.

## Features

### 1. Park Option
Allows customers to park their car by providing the following inputs:
- **Arrival Time**: The time to start parking (e.g., `2023-06-18 18:30`).
- **Car Identity**: A valid car identity format such as `59C-12345` or `01E-00001`.
- **Frequent Parking Number (Optional)**: A 5-digit number where the last digit is a modulo 11 check digit (e.g., `12343`).

The system validates the inputs and stores the parking information in file(s). After storing, it returns to the main option selection.

### 2. Pickup Option
Allows customers to pick up their car by providing:
- **Car Identity**: The identity of the car to be picked up.

The system performs the following:
- Calculates and displays the parking fee (rounded to 2 decimal places, e.g., `50.46`).
- If the car identity is not found, an error is raised.
- Accepts a payment amount from the customer. The amount must be greater than or equal to the fee.
- Any excess payment is stored as credit for future use.

### 3. History Option
Allows customers to view their parking history by providing:
- **Car Identity**

The system generates a file named `<car_identity>.txt` containing:
- **Total Payments**
- **Available Credits** (remaining credits from overpayments)
- **Parked Dates** in the format: `parked datetime - stay time`

#### Example Output File (`59C-12345.txt`)

# 🅿️ Parking Regulation Pricing

This table outlines the parking regulations and pricing based on the day of the week and time of day.

| Day of Week | 08:00 - 16:59 (Max Stay / Price per Hour) | 17:00 - Midnight (Max Stay / Price per Hour) | Midnight - 07:59 (Max Stay / One-Time Price) |
|-------------|-------------------------------------------|----------------------------------------------|----------------------------------------------|
| Sunday      | 8 hrs / \$2.00                            | Until midnight / \$5.00                      | None / \$20.00                                |
| Monday      | 2 hrs / \$10.00                           | Until midnight / \$5.00                      | None / \$20.00                                |
| Tuesday     | 2 hrs / \$10.00                           | Until midnight / \$5.00                      | None / \$20.00                                |
| Wednesday   | 2 hrs / \$10.00                           | Until midnight / \$5.00                      | None / \$20.00                                |
| Thursday    | 2 hrs / \$10.00                           | Until midnight / \$5.00                      | None / \$20.00                                |
| Friday      | 2 hrs / \$10.00                           | Until midnight / \$5.00                      | None / \$20.00                                |
| Saturday    | 4 hrs / \$3.00                            | Until midnight / \$5.00                      | None / \$20.00                                |


## 💡 Notes

- 🚗 **Frequent Parking Discount**:
Customers with a valid frequent parking number receive:
    - **50% discount** for parking during: **17:00 – Midnight** and **Midnight – 08:00**
    - **10% discount** for parking during: **08:00 – 16:59**

- ⏱️ **Overstay Penalty**:
Any car parked **beyond the maximum stay hours** will be charged **double the price** for each exceeded hour.

