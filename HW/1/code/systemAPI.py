from fastapi import FastAPI, Request
from system import upload_request_handler, run_request_handler, status_request_handler

app = FastAPI()


@app.post("/upload")
async def root(request: Request):
    try:
        """ http request contains a json like this :
         json = { "token":"user_email" , "user_object":{"code":user_code , "language":code_language}}"""""

        infos = await request.json()
        user_object = infos["user_object"]
        user_token = infos["token"]
        info_dict = {"user_object": user_object, "token": user_token}
        response_message = upload_request_handler(info_dict)
        return response_message
    except Exception:
        return "bad request."


@app.post("/run")
async def root(request: Request):
    try:
        info = await request.json()
        info_dict = {"username": info["token"], "code_id": info["code_id"]}
        response_message = run_request_handler(info_dict)
        return response_message
    except Exception:
        return Exception


@app.post("/status")
async def root(request: Request):
    try:
        info = await request.json()
        username = info["token"]
        response = status_request_handler(username)
        return response

    except Exception:
        return Exception
