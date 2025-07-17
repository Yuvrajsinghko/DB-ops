import mysql.connector
from faker import Faker
import random
from datetime import datetime, timedelta
from mysql.connector import Error, IntegrityError, ProgrammingError, InterfaceError


FAKE=Faker()

mydb=mysql.connector.connect(
    host="localhost",
    user="yuvraj",
    passwd="root69",
    database='greendb'
)
mycursor=mydb.cursor()
print("Connection Successfull")
    

# except mysql.connector.ProgrammingError as pe:
#     print("SQL Syntax Error:",pe)
# except mysql.connector.IntegrityError as i:
#     print("Constraint Violation:",i)
# except mysql.connector.InterfaceError as pr:
#     print("Connection Error:",pr)
# except Error as e:
#     print("General DB Error:",e)
# except Exception as e:
#     print("Unexpected Error:",e)



#This function get required ids for foreign key reference.
def ids_capture(st):
    final_list=[]
    #User ids 
    if st=="login":
        mycursor.execute("SELECT id FROM SignupDetails")
        final_list=[row[0] for row in mycursor.fetchall()]
    #Transport ids       
    elif st=="transport":
        mycursor.execute("SELECT transport_id FROM TransportDetails")
        final_list=[row[0] for row in mycursor.fetchall()]
    #Diet ids        
    elif st=="diet":
        mycursor.execute("SELECT diet_id FROM DietDetails")
        final_list=[row[0] for row in mycursor.fetchall()]
    #Utility ids        
    elif st=="utility":
        mycursor.execute("SELECT utility_id FROM UtilityUsage")
        final_list=[row[0] for row in mycursor.fetchall()]
    #Lifestyle ids 
    elif st=="lifestyle":       
        mycursor.execute("SELECT lifestyle_id FROM LifestyleHabits")
        final_list=[row[0] for row in mycursor.fetchall()]
            
    else:
    #Daily entry ids
        mycursor.execute("SELECT daily_entry_id FROM DailyEntry")
        final_list=[row[0] for row in mycursor.fetchall()]
    return final_list


#This function is used to populate signup table 
def signup_entry(user_input):
    usernames=[]
    mycursor.execute("SELECT username FROM SignupDetails")
    existing_usernames = set(row[0] for row in mycursor.fetchall())
    usernames = set()


    while len(usernames)<user_input:
        usp=FAKE.user_name()
        if usp not in usernames and usp not in existing_usernames:
            usernames.add(usp)
    usernames=list(usernames)
    for i in range(user_input):
        name=FAKE.name()
        age=random.randint(18,80)
        gender=FAKE.random_element(['Male','Female'])
        username=usernames[i]
        phone_numbers=FAKE.phone_number()
        email=FAKE.email()
        password=FAKE.password(length=10)
        date_joined=FAKE.date_time_between(start_date="-1y",end_date="now")
        last_login=FAKE.date_time_between(start_date=date_joined,end_date="now")
        mycursor.execute("INSERT INTO SignupDetails(name,age,gender,username,phone_no,email,user_password,date_joined,last_login) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",(name,age,gender,username,phone_numbers,email,password,date_joined,last_login) )
        mydb.commit()
    print("Task completed successfully:USER")



    
#This function is used to populate login table
def login_user_insert(user_input):
    ids=ids_capture("login")
    existing_id=[(isd) for isd in ids]
    new_ids=[]
    for k in ids:
        if k not in existing_id:
            new_ids.append(k)

    for i in range(len(new_ids)):
        signupids=new_ids[i]
        user_status=FAKE.random_element(['Verified','Unverified'])
        mycursor.execute("INSERT INTO ValidUser(signup_id,status) VALUES(%s,%s)",(signupids,user_status))

    mydb.commit()
    new_ids=[]
    print("Task completed successfully:LOGIN USER")


#This function is being used to populate transport related details table
def transport_data_insert(user_input):
    valid_id=ids_capture("login")
    
    
    for i in range(user_input):
        trans_id=valid_id[i]
        transport_mode=FAKE.random_element(['car','bike','flight','ship','cycle'])
        distance=random.uniform(500,500000)
        fuel=FAKE.random_element(['petrol','diesel','CNG'])
        years_own=random.randint(1,15)
        mycursor.execute("INSERT INTO TransportDetails(tt_id,mode_of_transport,distance_travelled,fuel_type,years_owned) VALUES(%s,%s,%s,%s,%s)",(trans_id,transport_mode,distance,fuel,years_own))
        mydb.commit()
    print("Task completed successfully:TRANSPORT DETAILS")


#This function is used to populate diet related details table
def diet_insert(user_input):
    ref_ids=ids_capture("login")
    for k in range(user_input):
        diet_ref=ref_ids[k]
        d_type=FAKE.random_element(['Vegetarian','Non-Vegetarian','Mixed','Vegan'])
        meals=random.randint(1,4)
        food_s=FAKE.random_element(['Local','Imported','Mixed'])
        mycursor.execute("INSERT INTO DietDetails(diet_ref_id,diet_type,meals_per_day,food_source) VALUES(%s,%s,%s,%s)",(diet_ref,d_type,meals,food_s))
    mydb.commit()
    print("Task completed successfully:DIET DETAILS")



#This function is used to populate utility details related table
def utility_entry(user_input):
    ref_ids=ids_capture("login")
    
    for j in range(user_input):
        ref_utility=ref_ids[j]
        elec=random.randint(5,10)
        water=random.randint(50,135)
        gas=random.uniform(0.5,1)
        mycursor.execute("INSERT INTO UtilityUsage(ut_ref_id,electricity_consumption,water_consumption,gas_usage)VALUES(%s,%s,%s,%s)",(ref_utility,elec,water,gas))
    mydb.commit()
    print("Task completed successfully:UTILITY DETAILS")

#This function is used to populate lifestylehabits related info table
def lifestylehabits_entry(user_input):
    ids=ids_capture("login")
    
    for h in range(user_input):
        lif_ref=ids[h]
        plastic=random.randint(1,20)
        shopping=FAKE.random_element(['Daily','Weekly','Rarely'])
        mycursor.execute("INSERT INTO LifestyleHabits(life_ref_id,plastic_item_used,shopping_frequency) VALUES(%s,%s,%s)",(lif_ref,plastic,shopping))
    mydb.commit()
    print("Task completed successfully:LIFESTYLE DETAILS")

#This function is used to populate daily user entry table
def daily_entry(user_input):
    user_ids_list=ids_capture("login")
    transport_id_list=ids_capture("transport")
    diet_id_list=ids_capture("diet")
    utility_id_list=ids_capture("utility")
    lifestyle_id_list=ids_capture("lifestyle")
    
    for d in range(user_input):
        us_id=user_ids_list[d]
        tr_id=transport_id_list[d]
        di_id=diet_id_list[d]
        uti_id=utility_id_list[d]
        life_id=lifestyle_id_list[d]
        carbon=round(random.uniform(5.0, 50.0), 2)
        date_in=FAKE.date_time_between(start_date="-1y",end_date="now")
        mycursor.execute("INSERT INTO DailyEntry(signup_ref_id,transport_ref_id,diet_ref_id,utility_ref_id,lifestyle_ref_id,carbon_score,date_time_of_entry)VALUES (%s,%s,%s,%s,%s,%s,%s)",(us_id,tr_id,di_id,uti_id,life_id,carbon,date_in))
    mydb.commit()

    print("Task completed successfully:DAILY ENTRY DETAILS")

#This function is used to populate comparison table
def comparison_insert(user_input):
    daily_ref_list=ids_capture("daily")
    
    for t in range(user_input):
        daily_ids_ref=daily_ref_list[t]
        prev_score=round(random.uniform(15,50),2)
        curr_score=round(random.uniform(10,45),2)
        change_percent = round(((prev_score - curr_score) / prev_score) * 100, 2)
        feedback=FAKE.random_element(['Improved','Need Improvement','No Change Detected'])
        date_check= datetime.now().date() - timedelta(days=random.randint(1, 20))
        mycursor.execute("INSERT INTO ComparisonTab(daily_en_id,previous_score,current_score,change_percent,feedback,date_checked)VALUES(%s,%s,%s,%s,%s,%s)",(daily_ids_ref,prev_score,curr_score,change_percent,feedback,date_check))
    mydb.commit()
    print("Task completed successfully:COMPARISON DETAILS")

#This function is used to populate tips table
def tips_insert(user_input):
    user_id_list=ids_capture("login")
    dailyentry_id_list=ids_capture("daily")

    for p in range(user_input):
        user_ref=user_id_list[p]
        daily_ref=dailyentry_id_list[p]
        tip=FAKE.random_element(["turning off lights when not in use","using public transportation","carpooling to work","switching to LED bulbs","recycling plastic and paper","reducing water usage","avoiding single-use plastics","planting a tree","buying local produce","riding a bicycle","composting organic waste","bringing reusable bags for shopping"])
        mycursor.execute("INSERT INTO Tips(user_ref,daily_ref,tips)VALUES(%s,%s,%s)",(user_ref,daily_ref,tip))
    mydb.commit()

    print("Task completed successfully:TIPS TABLE")

#Common function to create all tables all at once 
def create_tab():
    mycursor.execute("CREATE TABLE SignupDetails(id INTEGER AUTO_INCREMENT PRIMARY KEY,name VARCHAR(30),age INTEGER,gender VARCHAR(10),username VARCHAR(150) NOT NULL UNIQUE,phone_no VARCHAR(100),email VARCHAR(255) NOT NULL,user_password VARCHAR(255) NOT NULL,date_joined DATETIME DEFAULT CURRENT_TIMESTAMP,last_login DATETIME)")
    mycursor.execute("CREATE TABLE ValidUser(valid_user_id INTEGER AUTO_INCREMENT PRIMARY KEY,signup_id INTEGER,status VARCHAR(10),FOREIGN KEY (signup_id) REFERENCES SignupDetails(id))")
    mycursor.execute("CREATE TABLE TransportDetails(transport_id INTEGER AUTO_INCREMENT PRIMARY KEY,tt_id INTEGER,mode_of_transport VARCHAR(150),distance_travelled FLOAT,fuel_type VARCHAR(50),years_owned INTEGER,FOREIGN KEY (tt_id) REFERENCES SignupDetails(id))")
    mycursor.execute("CREATE TABLE DietDetails(diet_id INTEGER AUTO_INCREMENT PRIMARY KEY,diet_ref_id INTEGER NOT NULL,diet_type VARCHAR(20),meals_per_day INTEGER,food_source VARCHAR(20),FOREIGN KEY (diet_ref_id) REFERENCES SignupDetails(id))")
    mycursor.execute("CREATE TABLE UtilityUsage(utility_id INTEGER AUTO_INCREMENT PRIMARY KEY,ut_ref_id INTEGER NOT NULL,electricity_consumption FLOAT,water_consumption INTEGER,gas_usage INTEGER,FOREIGN KEY (ut_ref_id) REFERENCES SignupDetails(id))")
    mycursor.execute("CREATE TABLE LifestyleHabits(lifestyle_id INTEGER AUTO_INCREMENT PRIMARY KEY,life_ref_id INTEGER NOT NULL,plastic_item_used INTEGER,shopping_frequency VARCHAR(50),FOREIGN KEY (life_ref_id) REFERENCES SignupDetails(id))")
    mycursor.execute("CREATE TABLE DailyEntry(daily_entry_id INT AUTO_INCREMENT PRIMARY KEY,signup_ref_id INT NOT NULL,transport_ref_id INT NOT NULL,diet_ref_id INT NOT NULL,utility_ref_id INT NOT NULL,lifestyle_ref_id INT NOT NULL,carbon_score FLOAT,date_time_of_entry DATETIME,FOREIGN KEY (signup_ref_id) REFERENCES SignupDetails(id))")
    mycursor.execute("CREATE TABLE ComparisonTab(comparision_id INT AUTO_INCREMENT PRIMARY KEY,daily_en_id INT NOT NULL,previous_score FLOAT NOT NULL,current_score FLOAT NOT NULL,change_percent FLOAT NOT NULL,feedback VARCHAR(50),date_checked Date,FOREIGN KEY (daily_en_id) REFERENCES DailyEntry(daily_entry_id))")
    mycursor.execute("CREATE TABLE Tips(tips_id INT AUTO_INCREMENT PRIMARY KEY,user_ref INT NOT NULL,daily_ref INT NOT NULL,tips VARCHAR(255),FOREIGN KEY(user_ref) REFERENCES SignupDetails(id),FOREIGN KEY (daily_ref) REFERENCES DailyEntry(daily_entry_id))")
    print("Success")


#Common function to populate all tables all at once 
def populate_tables():
    user_input=int(input("Enter number of entries to insert: "))
    signup_entry(user_input)
    login_user_insert(user_input)
    transport_data_insert(user_input)
    diet_insert(user_input)
    utility_entry(user_input)
    lifestylehabits_entry(user_input)
    daily_entry(user_input)
    comparison_insert(user_input)
    tips_insert(user_input)
    print(f"{user_input} entries added.Task Complete.")

