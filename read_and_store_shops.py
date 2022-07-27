#DB requirement
import mysql.connector

#Json requirement
# import urllib library for Url access requirement
from urllib.request import Request, urlopen

# import json
import json

#Functions

#Rename fuel type name to a simpler one
def rename(name):
   if name == "Gasolina de mistura (motores a 2 tempos)":
      name = "Gasolina de mistura"

   elif name == "GNC (gás natural comprimido) - €/kg":
      name = "GNC Kg"

   elif name == "GNC (gás natural comprimido) - €/m3" :
      name = "GNC m3"

   elif name == "GNL (gás natural liquefeito) - €/kg" :
      name = "GNL Kg"

   elif name == "Gasóleo (até setembro 2021)" :
      name = "Gasóleo setembro 2021"

   elif name == "Gasolina 95 (até setembro 2021)" :
      name = "Gasolina 95 setembro 2021"
      
   name = name.replace(" ", "_")

   #print(name)

   return(name)

#url which has the json file
url = "https://precoscombustiveis.dgeg.gov.pt/api/PrecoComb/PesquisarPostos?idsTiposComb=&idMarca=&idTipoPosto=&idDistrito=&idsMunicipios=&qtdPorPagina=&pagina=1"

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

#Retrieving single row
sql_select = f"SELECT Id FROM {table_name}"
cursor.execute(sql_select)

all_ids = [0]
for data in cursor:
    #get ids
    data_id=data[0]
    #print (data_id)
    all_ids.append(data_id)


#Headers to trick the website to not block us
req = Request(url, headers={'User-Agent': 'XYZ/3.0'})

# store the response of URL
response = urlopen(req).read()

# JSON
# storing the JSON response
# from url in data
data_json = json.loads(response)

# get the whole data and store it
all_data = data_json["resultado"]

#print(all_data)

counter = 0

for valor in all_data:

   #Id
   id_shop = valor["Id"]
   #print (id_shop)

   #If the id is not present in the SQL database
   if id_shop not in all_ids:
      all_ids.append(id_shop)
      #print (all_ids)
      #print("Not Present")

      #Name
      name_shop = valor["Nome"]

      #Brand
      brand_shop = valor["Marca"]

      #District
      district_shop = valor["Distrito"]

      #County
      county_shop = valor["Municipio"]

      #Address
      adress1_shop = valor["Morada"]
      adress2_shop = valor["CodPostal"]
      adress3_shop = valor["Localidade"]
        
      #Coordinates
      latitude_shop = valor["Latitude"]
      longitude_shop = valor["Longitude"]

      #Update date
      update_time = valor["DataAtualizacao"]

      #Tipo Combustivel
      fuel_type = valor["Combustivel"]

      #Rename in case of big name
      fuel_type = rename(fuel_type)

      #print(fuel_type)

      #Preco Combustivel
      fuel_price = valor["Preco"]
      #print (fuel_price)

      # Preparing SQL query to INSERT a record into the database.
      sql1 = f"INSERT INTO {table_name} (Id, Nome, Marca, Distrito, Municipio, Morada, CodPostal, Localidade, Latitude, Longitude, {fuel_type}_date, {fuel_type}) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

      val1 = (id_shop, name_shop, brand_shop, district_shop, county_shop, adress1_shop, adress2_shop, adress3_shop, latitude_shop, longitude_shop, update_time, fuel_price)

      #print (sql1)
      #print (val1)

      try:
         # Executing the SQL command
         #Insert one piece of data
         cursor.execute(sql1, val1)

         # Commit your changes in the database
         #print ("ok")
         conn.commit()

         counter+=1
   
      except:
         # Rolling back in case of error
         print (id_shop)
         print (name_shop)
         print (county_shop)
         print ("error_1")
         conn.rollback()

   else:
      #If id present in database
      #Update date
      update_time = valor["DataAtualizacao"]

      #Tipo Combustivel
      fuel_type = valor["Combustivel"]

      #Rename in case of big name
      fuel_type = rename(fuel_type)

      #print(fuel_type)

      #Fuel type update time
      fuel_type_date = fuel_type + '_date'
      #print(fuel_type_date)

      #Retrieving single row
      sql_select_date = f"SELECT {fuel_type_date} FROM {table_name} where Id = {id_shop} "
      cursor.execute(sql_select_date)
      datas=cursor.fetchone()[0]

      #print("ID")
      #print(id_shop)
      #print("fuel_type_date_json")
      #print(update_time)
      #print("fuel_type_date_sql")
      #print(datas)
      #print("replace")

      #convert sql date to the format it is present on the json
      #make sure to do it only if a date is present
      if datas:
         datas = datas.strftime("%Y-%m-%d %H:%M")
      #print("replace")
      #print(datas)

      #Check if price information on the sql is out of date
      if update_time != datas:
         #print("ID")
         #print(id_shop)
         #print("é diferente")
         #print("fuel_type_date_json")
         #print(update_time)
         #print("fuel_type_date_sql")
         #print(datas)
         #print("Updated")

         #Preco Combustivel
         fuel_price = valor["Preco"]
         #print (fuel_price)

         # Preparing SQL query to update a record into the database.
         #sql2 = "UPDATE shops SET fuel_type = fuel_price WHERE Id = id_shop"
         sql2 = f"UPDATE {table_name} SET {fuel_type} = %s , {fuel_type_date} = %s WHERE Id = %s"
         val2 = (fuel_price, update_time, id_shop)

         #print (sql2)
         #print (val2)

         try:
            # Executing the SQL command
            #Insert one piece of data
            cursor.execute(sql2,val2)

            # Commit your changes in the database
            #print ("ok")
            conn.commit()

            #print (id_shop)
            #print ("UPDATED")

         except:
            # Rolling back in case of error
            print (id_shop)
            print (fuel_type)
            print ("error_2")
            conn.rollback()

# Closing the connection
conn.close()