
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

