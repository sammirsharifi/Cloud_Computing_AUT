import pika, os, requests
from urllib.parse import quote
from dotenv import load_dotenv
from s3 import s3_download_object
from Database import table_insert, table_read
from message_broker import receive
from urllib.parse import urlencode

load_dotenv()

"""jobMicro.py is our job Microservice that manages the runcode requests has sent by users."""

"""this function is provided to pass s3 receive function that gets jobs requests."""


def job_receive_callback(ch, method, properties, body):
    print(body)
    code_id = body.decode()
    add_job(code_id)

"""
add_job function:
1 - gets a code_id from jobs_queue
2 - gets source code from s3 by code_id
3 - creates queryString by codeToQuerystring
4 - insert to jobs table new recorde
5 - insert to results table new recorde that will complete after running - status is in progress and at the end will become done.
"""
def add_job(code_id):
    try:
        code = s3_download_object(code_id)
        inputs, language = table_read("uploads", "input , language", f"id = {code_id}")[0]
        query = codeToQuerystring(code, inputs, language)
        info = {"id": code_id, "upload": code_id, "job": query, "status": "none"}
        # update jobs table & then executorMicro will work on it.
        table_insert("jobs", info)
        #first we add a record to results table with id , job and status then when code run , we will add output and execute_date
        result_info = {"id": code_id, "job": query, "status": "in progress"}
        table_insert("results", result_info)
        return True
    except Exception:
        return Exception


def codeToQuerystring(code, inputs, language):
    return urlencode({"code": code, "language": language, "input": inputs})


"""this function will run to get new requests in the moment."""
receive("jobs", job_receive_callback)
