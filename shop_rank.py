#distance library
from cmd import PROMPT
from pickletools import long1
import geopy.distance

#DB requirement
import mysql.connector

#table name
table_name = 'shops'

#DB connection
#establishing the connection
conn = mysql.connector.connect(
   user=my_user, 
   password=my_password,
   host=my_host, 
   database=my_database
   )

#Creating a cursor object using the cursor() method
cursor = conn.cursor()

#Variables
#Brand discount
BP_DISCOUNT=0
GALP_DISCOUNT=0
CEPSA_DISCOUNT=0
REPSOL_DISCOUNT=0
PRIO_DISCOUNT=0

#functions
#Ask for value of discount value
def ask_discount():
    print("Define your discount €/l")
    while True:
        try:
            
            DISCOUNT = float(input(""))
            return(DISCOUNT)
            #break
        except ValueError:
            print('This is not a number.')

#Insert data in list
def insert_list(i):
    best_shop_list.insert(0 + i, data_id)
    best_shop_list.insert(1 + i, data_name) 
    best_shop_list.insert(2 + i, data_brand) 
    best_shop_list.insert(3 + i, data_lat) 
    best_shop_list.insert(4 + i, data_long) 
    best_shop_list.insert(5 + i, total_fuel) 

#Questions
#What kind of fuel?

print("\nWhat kind of fuel?")
while True:  

    print("1. Gasolina_simples_95")
    print("2. Gasolina_especial_95")

    print("3. Gasolina_98")
    print("4. Gasolina_especial_98")

    print("5. Gasóleo_simples")
    print("6. Gasóleo_especial")

    print("7. GPL_Auto")

    fuel_choice = input("\nEnter your Choice number: ")

    if fuel_choice== '1':
        print("option 1")
        fuel_type = 'Gasolina_simples_95'
        print(fuel_type)
        break
    elif fuel_choice== '2':
        print("option 2")
        fuel_type = 'Gasolina_especial_95'
        print(fuel_type)
        break
    elif fuel_choice== '3':
        print("option 3")
        fuel_type = 'Gasolina_98'
        print(fuel_type)
        break
    elif fuel_choice== '4':
        print("option 4")
        fuel_type = 'Gasolina_especial_98'
        print(fuel_type)
        break
    elif fuel_choice== '5':
        print("option 5")
        fuel_type = 'Gasóleo_simples'
        print(fuel_type)
        break
    elif fuel_choice== '6':
        print("option 6")
        fuel_type = 'Gasóleo_especial'
        print(fuel_type)
        break
    elif fuel_choice== '7':
        print("option 7")
        fuel_type = 'GPL_Auto'
        print(fuel_type)
        break
    else :
        print("Oops! Incorrect Choice.")

#Ask my location
print("\nDefine your location")
while True:
    try:
        my_latitude= float(input("Latitude: "))
        break
    except ValueError:
        print('This is not a coordinate.')

while True:
    try:
        my_longitude= float(input("Longitude: "))
        break
    except ValueError:
        print('This is not a coordinate.')

#My location
my_cordinates = (my_latitude, my_longitude)

#Ask for the max radius you want to search the shops

print("\nDefine the radius to search the shops in Km")
while True:
    try:
        radius= int(input(""))
        break
    except ValueError:
        print('This is not a number.')

print("\nDefine your average car consumption in l/100 Km")
while True:
    try:
        consumption = float(input(""))
        break
    except ValueError:
        print('This is not a number.')

print("\nDefine how much you want to spend in €")
while True:
    try:
        money = int(input(""))
        break
    except ValueError:
        print('This is not a number.')


#Ask for discount

#Ask for brand
#discount_brand

print("\nWhat fuel brand?")
while True:  
    
    print("1. BP")
    print("2. Galp")

    print("3. Cepsa")
    print("4. Repsol")

    print("5. Prio")
    print("6. No more discounts")

    discount_brand_option = input("\nEnter your Choice number: ")
    
    if discount_brand_option== '1':
        print("BP")
        BP_DISCOUNT = ask_discount()
        
    elif discount_brand_option== '2':
        print("Galp")
        GALP_DISCOUNT = ask_discount()
        
    elif discount_brand_option== '3':
        print("Cepsa")
        CEPSA_DISCOUNT = ask_discount()        

    elif discount_brand_option== '4':
        print("Repsol")
        REPSOL_DISCOUNT = ask_discount()

    elif discount_brand_option== '5':
        print("Prio")
        PRIO_DISCOUNT = ask_discount()        

    elif discount_brand_option== '6':
        print("No more discounts")
        break

    else :
        print("Oops! Incorrect Choice.")  

#Retrieving single row
sql_select = f"SELECT Id, Nome, Marca, Latitude, Longitude, {fuel_type} FROM {table_name}"
cursor.execute(sql_select)

#Counter for the number of shops inside that radius
counter=0

#Shop rank list
best_shop_list= [0] * 18

#get the data for each row of the sql
for data in cursor:
    data_id=data[0]
    data_name=data[1]
    data_brand=data[2]
    data_lat=data[3]
    data_long=data[4]
    data_price=data[5]

    #Calculate distance
    shop_cordinates = (data_lat, data_long)

    #Calculate my distance from shop
    distance = geopy.distance.geodesic(my_cordinates, shop_cordinates).km

    #If shop is within radius and has the fuel type
    if distance <= radius and data_price:
        counter +=1

        #Calculate fuel spent going to the shop
        fuel_spent = (distance * consumption) / 100
        #going to the shop and returning
        fuel_spent = 2 * fuel_spent

        #Convert fuel price to float
        data_price = float(data_price.replace("€","").replace(",","."))

        #Check the brand of the shop
        if data_brand == "BP":
            discount = BP_DISCOUNT
        elif data_brand == "GALP":
            discount = GALP_DISCOUNT
        elif data_brand == "CEPSA":
            discount = CEPSA_DISCOUNT
        elif data_brand == "REPSOL":
            discount = REPSOL_DISCOUNT
        elif data_brand == "PRIO":
            discount = PRIO_DISCOUNT
        else:
            discount = 0

        #Apply discount on the price
        data_price = data_price - discount

        #liters of fuel bought with the money available
        fuel_bought = money / data_price
        
        #How much liters remaining after going to the shop and returning
        total_fuel= fuel_bought - fuel_spent

        #if the shop gives more fuel than the ranked 1
        #store it
        if total_fuel > best_shop_list[5]:

            i=0

            #insert values in rank 1 and move the previous rank 1 to rank 2 and rank 2 to rank 3
            insert_list(i)

        #if the shop gives more fuel than the ranked 2
        elif total_fuel > best_shop_list[11] and total_fuel < best_shop_list[5]:

            i=6

            #insert values in rank 2 and move the previous rank 2 to rank 3 and rank 3 to rank 4
            insert_list(i)

        #if the shop gives more fuel than the ranked 3
        elif total_fuel > best_shop_list[17] and total_fuel < best_shop_list[11]:

            i=12
            
            #insert values in rank 3 and move the previous rank 3 to rank 4
            insert_list(i)

#Delete values that are ranked <4 place
while len(best_shop_list) > 18:
    best_shop_list.pop()

print("Number of shops in the radius:")
print(counter)

#Ranked Shops
i = 0
j = 0
while i < 3:
    #list

    print(f"The {i + 1}º Choice is:")
    print(f"Id: {best_shop_list[0+j]}")
    print(best_shop_list[1+j])
    print(best_shop_list[2+j])
    print("Located in:")
    print(f"{best_shop_list[3+j]} , {best_shop_list[4+j]}")
    print("And the fuel you get is:")
    print("%.2f L" % best_shop_list[5+j])

    i = i +1
    j = j +6
