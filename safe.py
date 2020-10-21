import sqlite3
import base64
import imageio
import cv2
from click._compat import raw_input

PASSWORD = "123456"

connect = raw_input("What is your password?")

while connect != PASSWORD:
    connect = raw_input("What is your password?\n")
    if connect == "q":
        break

if connect == PASSWORD:
    conn = sqlite3.connect('mysafe.db')
    try:
        conn.execute('CREATE TABLE SAFE(FULL_NAME TEXT PRIMARY KEY, EXTENSION TEXT NOT NULL, FILES TEXT NOT NULL);')
        print("Your safe has been created!\nWhat would you like to store in it today?")
    except:
        print("You have a safe, what would you like to store in it today?")

    while True:
        print("\n" + "*" * 15)
        print("Commands:")
        print("q = quit program")
        print("o = open file")
        print("s = store file")
        print("*" * 15)
        input_ = raw_input(":")

        if input_ == "q":
            break
        if input_ == "o":
            file_type = raw_input("What is the filetype of the file you want to open?\n")
            file_name = raw_input("What is the name of the file you want to open?\n")
            FILE_ = file_name + "." + file_type

            cursor = conn.execute("SELECT * from SAFE WHERE FULL_NAME = " + "' + FILE_ + '")

            file_string = ""
            for row in cursor:
                file_string = row[3]
            with open(FILE_, 'wb') as f_output:
                print(file_string)
                f_output.write(base64.b64decode(file_string))

        if input_ == "s":
            PATH = raw_input("Type in the full path to the file you want to store\n")
            FILE_TYPES = {"txt": "TEXT", "java": "TEXT", "dart": "TEXT", "py": "TEXT", "jpg": "TEXT",
                          "png": "TEXT", "jpeg": "TEXT"}

            file_name = PATH.split("/")
            file_name = file_name[len(file_name) - 1]
            file_string = ""

            NAME = file_name.split(".")[0]
            EXTENSION = file_name.split(".")[1]

            try:
                EXTENSION = FILE_TYPES[EXTENSION]
            except:
                Exception()

            if EXTENSION == "IMAGE":
                IMAGE = cv2.imread(PATH)
                file_string = base64.b64encode(cv2.imencode('.jpg', IMAGE)[1]).decode()

            EXTENSION = file_name.split(".")[1]

            command = 'INSERT INTO SAFE (FULL_NAME, EXTENSION, FILES) VALUES (%s, %s, %s);'\
            %('"' + file_name + '"', '"' + EXTENSION + '"', '"' + file_string + '"')

            conn.execute(command)
            conn.commit()
