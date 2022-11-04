###################################
# Find Revealed PII on User Forms #
###################################
import re
import json
import uvicorn
from jotform import *
from typing import Optional
from fastapi import FastAPI
from setuptools import setup
from pydantic import BaseModel
from urllib.request import urlopen
from jotform import JotformAPIClient
from starlette.responses import Response
from fastapi.templating import Jinja2Templates
from starlette.templating import Jinja2Templates
import urllib.request, urllib.parse, urllib.error
from fastapi import FastAPI, Request, HTTPException


templates = Jinja2Templates(directory="templates")


app = FastAPI(title="Jotform Form Validation")

# Private Regex Code(Masked) 

def check(control):
    data = {}
    if (re.search(regex_email, control)):
        valid_mail = re.search('[\w.+-]+@[\w-]+.[\w.-]+', control)
        match_data = valid_mail.group(0)
        if match_data not in data.values():
            data['Email'] = match_data
    if (re.search(regex_card, control)):
        valid_card = re.search(regex_card, control)
        data['Credit Card Number'] = valid_card.group(0)
    if (re.search(regex_phone, control)):
        valid_phone = re.search(regex_phone, control)
        data['Phone Number'] = valid_phone.group(0)
    if re.search(regex_ssn, control):
        valid_ssn = re.search(regex_ssn, control)
        data['Social Security Number'] = valid_ssn.group(0)
    if re.search(regex_zip, control):
        valid_zip = re.search(regex_zip, control)
        data['Zip Code'] = valid_zip.group(0)
    if re.search(regex_ip4, control):
        valid_ip4 = re.search(regex_ip4, control)
        data['IP'] = valid_ip4.group(0)
    if re.search(regex_ip6, control):
        valid_ip6 = re.search(regex_ip6, control)
        data['IP'] = valid_ip6.group(0)
    if re.search(regex_passport, control):
        valid_passport = re.search(regex_passport, control)
        data['Passport Number'] = valid_passport.group(0)
    return data


def get_form_content(id):
    questions = jotformAPI.get_form_questions(id)
    data_list = []
    for value in questions.values():
        valid_info = check(str(value))
        if valid_info:
            data_list.append(valid_info)
        else:
            continue
    print(data_list)
    return data_list


@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})


@app.get("/check/")
async def get_data(request: Request, FormID):
    result = get_form_content(FormID)
    return templates.TemplateResponse("check.html", {"request": request, "FormID": FormID, "result":result})


if __name__ == '__main__':
    uvicorn.run(app, port=8000, host="127.0.0.1")
