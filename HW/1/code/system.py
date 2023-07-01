import uuid

import message_broker
from Database import table_insert, table_read
from s3 import s3_put_object
from message_broker import send

"""this function gets uploaded file info & first get a unique id from def generate_id and then uploads the 
source code on the s3 by def s3_put_object and after that uploads the information about file on the database at the table <uploads>
by def table_insert"""


def upload_request_handler(info_dict):
    try:
        user_object = info_dict["user_object"]
        username = info_dict["token"]
        user_code = user_object["code"]
        user_inputs = user_object["inputs"]
        code_language = user_object["language"]
        object_id = generate_id()
        s3_put_object(user_code, object_id)
        db_info = {"id": object_id, "email": username, "input": user_inputs, "language": code_language, "enable": 0}
        table_insert("uploads", db_info)

        return f"your code uploaded successfully. your file id is {object_id}."

    except Exception as e:
        return e


"""This function handles user running code request.
 at the first gets record that has same username and id.
 if there is no result returns <<this code dose not belong to you>>
 if get a result and its enable is 1 returns <<this code is not allowed>>
else returns <<your code added to jobs queue.>>"""


def run_request_handler(info_dict):
    username = info_dict["username"]
    code_id = info_dict["code_id"]
    result = table_read("uploads", "enable", f"id={code_id} AND email=\"{username}\"")
    if len(result) == 0:
        return "This code does not belong to you."
    # enable field
    if result[0][0] == 1:
        return "This code is not allowed."
    if message_broker.send("jobs", code_id):
        return "your code added to jobs queue."


def generate_id():
    id = str(uuid.uuid4().int)[:4]
    return id


def status_request_handler(email):
    codes_status={}
    user_codes_id=table_read("uploads","id",f"email=\"{email}\"")
    for code_id in user_codes_id:
        code_id=code_id[0]
        output,status,execute_date=tuple(table_read("results","output,status,execute_date",f"id ={code_id}")[0])
        codes_status[code_id]={"output":output,"status":status,"execute_date":execute_date}
    return codes_status




