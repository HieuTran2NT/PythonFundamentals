from parking_system import ParkingSystem

ps = ParkingSystem()

while True:
    print("\n=== Parking System Menu ===")
    print("1. Park")
    print("2. Pickup")
    print("3. History")
    print("4. Exit")
    choice = input("Choose an option (1-4): ")

    try:
        if choice == '1':
            arrival = input("Enter arrival time (YYYY-MM-DD HH:MM): ")
            car_id = input("Enter car identity (e.g., 59C-12345): ")
            fp_number = input("Enter frequent parking number (optional): ").strip() or "N/A"
            ps.park(arrival, car_id, fp_number)
            print("✅ Parked successfully.")

        elif choice == '2':
            car_id = input("Enter car identity: ")
            current_time = input("Enter current time (YYYY-MM-DD HH:MM): ")

            try:
                fee = ps.calculate_fee_only(car_id, current_time)
                print(f"💰 Parking fee: ${fee:.2f}")
                payment = float(input("Enter payment amount: "))
                fee, excess = ps.process_payment(car_id, current_time, payment)
                print(f"✅ Payment successful. Excess: ${excess:.2f}")
            except Exception as e:
                print(f"⚠️ Error: {e}")

        elif choice == '3':
            car_id = input("Enter car identity: ")
            report = ps.history(car_id)
            print(f"📄 History report saved to {report}")

        elif choice == '4':
            print("👋 Exiting system.")
            break

        else:
            print("❌ Invalid choice.")

    except Exception as e:
        print(f"⚠️ Error: {e}")
