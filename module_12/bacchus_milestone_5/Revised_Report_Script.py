#Group Gamma 
#Julian Gomez Jr., Zachary Mazairz, Jeremiah Kellam, Emily Wojan
#CSD 310
#Module 12.2 Assignment
#May 16, 2023

"""The purpose of this program is to enable access to the MySQL Bacchus
database and query the MySQL bacchus database run specific buisness reports."""

import mysql.connector
from mysql.connector import errorcode


config = {
    "user" : "bacchus_user",
    "password" : "gamma",
    "host" : "127.0.0.1",
    "database" : "bacchus",
    "raise_on_warnings" : True 
}

try:
    db = mysql.connector.connect(**config)
    print("\n Database user {} connected to MySQL on host {} with database {}". format(config["user"], config["host"], config["database"]))

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print(" The supplied username or password are invalid")

    elif err.errno == errcode.ER_BAD_DB_ERROR:
        print(" The specified database does not exist")

    else:
        print(err)



cursor = db.cursor()



def employeeSnapshot(cursor, title):  

    cursor.execute(
    """
    SELECT 
        e.employee_id,
        CONCAT(e.first_name, ' ', e.last_name) AS full_name,
        SUM(t.hours_worked_monthly) AS total_hours
    FROM
        timecards t
            JOIN
        Employees e ON e.employee_id = t.employee_ID
    WHERE
        t.Date_Posted >= '2022-04-01'
    GROUP BY e.employee_id
    """
    )

    employees = cursor.fetchall()
    print("\n -- {:^30} --\n".format(title))
    print("Employee ID\tEmployee Name	\tHours Worked From April 2022 - March 2023")
    print("-----------\t-------------	\t-----------------------------------------")

    for employee in employees:
        print("{:<10}\t{:<20}\t{} Hours".format(employee[0], employee[1], employee[2]))

    print("")
    print("")  

def orderSnapshot(cursor, title):  
    #not sure the DateDiff function is going to work, but worth looking into functions similar to show the difference in the days between the two delivery fields
    cursor.execute(
    """
    SELECT sup.supplier_name, so.order_date, so.estimated_delivery_date, so.actual_delivery_date, DATEDIFF(so.actual_delivery_date, so.estimated_delivery_date), so.supply_order_id
    FROM supply_order AS so
    INNER JOIN supplier AS sup ON so.supplier_id = sup.supplier_id
    """
    )

    supplyOrder = cursor.fetchall()
    print("\n -- {:^30} --\n".format(title))
    print("Supplier Name	\tOrder ID\tOrder Date\tEstimated Delivery\tActual Delivery	\tDelivery Gap")
    print("--------------	\t--------\t----------\t------------------\t---------------	\t------------")

    for entry in supplyOrder:
        print("{:<20}\t{:<10}\t{}\t{}	\t{}	\t{:^5} Days".format(entry[0], entry[5], entry[1], entry[2], entry[3], entry[4]))
    
    print("")
    print("")  

def wineSnapshot(cursor, title):  
    
    cursor.execute(
    """
    SELECT w.wine_name, FORMAT((w.units_on_hand + SUM(wod.units_ordered)), 0) AS produced, FORMAT(SUM(wod.units_ordered), 0) AS ordered, FORMAT((w.units_on_hand + SUM(wod.units_ordered) - SUM(wod.units_ordered)), 0) AS sold
    FROM wine AS w
    INNER JOIN wine_order_details AS wod ON w.wine_id = wod.wine_id
    GROUP BY w.wine_name, w.units_on_hand
    
    """
    )

    wines = cursor.fetchall()
    print("\n -- {:^30} --\n".format(title))
    print("Wine Name\tUnits Produced	\tUnits Purchased	\tUnits Remaining")
    print("---------\t--------------	\t----------------\t---------------")
    
    for wine in wines:
        print("{:<10}\t{} units 	\t{} units	\t{} units".format(wine[0], wine[1], wine[2], wine[3]))

    print("")
    print("")  
        
def distributionSnapshot(cursor, title):
	 
    cursor.execute(
    
    """
    SELECT w.wine_name, d.distributor_name
    FROM wine  AS w
    INNER JOIN distributor AS d ON w.wine_id= d.wine_id 
    GROUP BY d.distributor_name, w.wine_name
    """
    )
    
    distributors = cursor.fetchall()
    print("\n -- {:^30} --\n".format(title))
    print("Distributor		\tWine Carried")
    print("-----------		\t------------")
    
    for distributor in distributors:
        print("{:<30}\t{:<30}".format(distributor[1], distributor[0]))            


employeeSnapshot(cursor, "EMPLOYEE HOURS REPORT")
orderSnapshot(cursor, "ORDERS REPORT (a negative delivery gap shows supplies that were delivered before the estimated delivery date)")
wineSnapshot(cursor, "WINE SALES REPORT")
distributionSnapshot(cursor, "WINE DISTRIBUTION REPORT")


db.close()
