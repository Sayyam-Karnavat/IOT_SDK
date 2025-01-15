
import sqlite3


def get_raspberry_connection():
    try:
        conn = sqlite3.connect("raspberry.db" , check_same_thread= False)
        return conn
    except Exception as e:
        print("Error :-" , e)
        return None
    
def create_table(json_data):
    try :
        conn = get_raspberry_connection()
        if conn and json_data:
            cursor = conn.cursor()
            keys = [f"{key} text" for key in json_data.keys()]
            keys_string = ','.join(keys)

            cursor.execute(f"CREATE TABLE IF NOT EXISTS RASPBERRY ({keys_string})")
            conn.commit()
            conn.close()
        else:
            print("Connection could not be made or json data is null !!!")
    except Exception as e:
        print("Error :-" , e)
     
def drop_table():
    try :
        conn = get_raspberry_connection()
        if conn :
            cursor = conn.cursor()

            cursor.execute("DROP TABLE IF EXISTS RASPBERRY")
            conn.close()
        else:
            print("Connection could not be made !!!")
    except Exception as e:
        print("Error :-" , e)


def get_all_data():
    try :
        conn = get_raspberry_connection()
        
        if conn :
            cursor = conn.cursor()

            all_rows = cursor.execute("SELECT * FROM RASPBERRY").fetchall()
            conn.close()
            return all_rows
        else:
            print("Connection could not be made !!!")
    except Exception as e:
        print("Error :-" , e)



def insert(json_data):
    try:
        conn = get_raspberry_connection()
        if conn:
            cursor = conn.cursor()
            # Get current columns in the table
            columns_in_table = set(x[0] for x in cursor.execute("SELECT name FROM pragma_table_info('RASPBERRY');").fetchall())
            columns_in_json = set(json_data.keys())

            # Identify missing columns (in json but not in table)
            missing_columns = set(columns_in_json - columns_in_table)
            for column in missing_columns:
                cursor.execute(f"ALTER TABLE RASPBERRY ADD COLUMN {column} TEXT")

            # Prepare the insert statement
            all_columns = columns_in_table.union(columns_in_json)
            key_string = ",".join(all_columns)
            placeholders = ",".join("?" for _ in all_columns)
            # Prepare values, using None for missing columns
            values = [json_data.get(col, None) for col in all_columns]
            cursor.execute(f"INSERT INTO RASPBERRY ({key_string}) VALUES ({placeholders})", values)
            conn.commit()
            conn.close()
            print("Data inserted into Database !!!")
        else:
            print("Connection could not be made!")
    except Exception as e:
        print("Error inserting: ", e)

if __name__ == "__main__":
    # insert(json_data=sample_json)
    # get_raspberry_connection()
    # all_rows = get_all_data()

    sample_json = {'applicationid': 722841168,
    'blocknumber': 44226419,
    'blocktimestamp': 1727343263,
    'device_id': 'Device_A',
    'device_status': 'stopped',
    'gasfees': 1000,
    'global_hash': 'aced371f8b249e38f29c147d9fc51aab',
    'global_humidity': '18',
    'global_moisture': '86',
    'global_temperature': '111',
    'global_uuid': '2206',
    'model_prediction': 'Normal',
    'region': 'Pune',
    'transactionid': 'ZZAU2LF4FHHEYNL7HIR53INNYWD2ZMLVE6CTWVKZ4UGXGE2SMWYA',
    'walletaddress': 'UKDE5GRYYUE6NHBGQUOPENWQPZQYTS5BWAKR7KV2JI3YBJD2NQAR4O64LI'}

    drop_table()
    # create_table(json_data=sample_json)
    # insert(json_data=sample_json)
    # print(get_all_data())
