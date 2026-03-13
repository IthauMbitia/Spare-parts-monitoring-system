print("\n ==========SPARE PARTS MONITORING SYSTEM=========")
import sqlite3

#------------DATABASE SETUP---------------
def init_db():

    conn = sqlite3.connect ('spare_part_monitoring_system.db')
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS spare_part_monitoring_system (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        spare_part_name text,
        spare_part_code text unique,
        machine text,
        quantity integer,
        minimum_level integer,
        location text
    )
    """)
    conn.commit()
    conn.close()

#------------INPUTS PROTECTION---------------
def input_int(prompt):
    while True:
        value = input(prompt)
        try:
            return int(value)
        except ValueError:
            print("Invalid input. Please enter a whole number.")


def input_non_empty(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Input cannot be empty.")

#------------ADD SPARE PARTS---------------
def add_spare_parts():
    spare_part_name = input_non_empty("Spare part name: ")
    spare_part_code = input_non_empty("Spare part code: ")
    machine = input_non_empty("Machine name: ")
    quantity = input_int("Quantity of spares: ")
    minimum_level = input_int("Minimum level of spares: ")
    location = input_non_empty("Location of spares: ")

    conn = sqlite3.connect('spare_part_monitoring_system.db')
    c = conn.cursor()

    c.execute("""INSERT INTO spare_part_monitoring_system (
    spare_part_name,spare_part_code,machine,quantity, minimum_level,location)
     VALUES (?,?,?,?,?,?)""", (spare_part_name,spare_part_code,
                               machine,quantity, minimum_level,location))
    conn.commit()
    conn.close()
    print("SPARE PARTS SUCCESSFULLY ADDED")

#------------ISSUE SPARE PARTS---------------
def issue_spare_parts():
    spare_part_code = input_non_empty("Spare part code: ")
    amount = input_int("Enter quantity to issue: ")


    conn = sqlite3.connect('spare_part_monitoring_system.db')
    c = conn.cursor()

    c.execute("""
       SELECT quantity FROM spare_part_monitoring_system
       WHERE spare_part_code = ?
       """, (spare_part_code,))

    result = c.fetchone()

    if result is None:
        print("Part not found.")
    elif amount <= 0:
        print("Quantity must be greater than zero.")
    elif result[0] < amount:
        print("Not enough stock available.")
    else:
        c.execute("""
           UPDATE spare_part_monitoring_system
           SET quantity = quantity - ?
           WHERE spare_part_code = ?
           """, (amount, spare_part_code))
        conn.commit()
        print("Part issued successfully.")

    conn.close()


#------------CHECK LOW STOCK---------------
def check_low_stock():
    conn = sqlite3.connect('spare_part_monitoring_system.db')
    c = conn.cursor()

    c.execute("""SELECT spare_part_name,quantity,minimum_level FROM spare_part_monitoring_system
    WHERE quantity <= minimum_level""")
    
    low_stock = c.fetchall()
    conn.close()

    if low_stock:
        print("LOW STOCK ITEMS:")
        for item in low_stock:
            print(f"{item[0]} | Qty: {item[1]} |Min: {item[2]}")
    else:
            print("NO LOW STOCK")


# ------------VIEW ALL SPARE PARTS---------------
def view_all_spare_parts():
    conn = sqlite3.connect('spare_part_monitoring_system.db')
    c = conn.cursor()

    c.execute("SELECT * FROM spare_part_monitoring_system")

    row = c.fetchall()
    c.close()

    print("ALL SPARE PARTS")
    print("\nID | PART NAME | PART CODE | MACHINE | QTY | MIN | LOCATION")
    for row in row:
        print(f"{row[0]:<7} {row[1]:<10} {row[2]:<10} {row[3]:<8} {row[4]:<5} {row[5]:<10} {row[6]}")


#------------MAIN MENU---------------
def main_menu():
    while True:

        print("*" * 60)
        print("1. Add spare parts")
        print("2. Issue spare parts")
        print("3. Check low stock")
        print("4. View all spare parts")
        print("5. Exit")

        operation = input_int("Enter operation [1-5]: ")

        print("*" * 60)

        if operation == 1:
            add_spare_parts()
        elif operation == 2:
            issue_spare_parts()
        elif operation == 3:
            check_low_stock()
        elif operation == 4:
            view_all_spare_parts()
        elif operation == 5:
            print("Exit successful ")
            break
        else:
            print("INVALID COMMAND")




#------------PROGRAM RUN---------------
init_db()
main_menu()



