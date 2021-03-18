import sys
import os
import logging

# Connect to db_connector from parent directory
PARENT_DIR = ".."
CURRENT_DIR = os.path.dirname(
    os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__)))
)
sys.path.append(os.path.normpath(os.path.join(CURRENT_DIR, PARENT_DIR)))

from DatabaseConnector import db_malaysia_patient_cases, db_malaysia_states

import requests
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil import parser

class ScrapeMalaysia():
    TABLE = "test" # "prod"
    DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
    HEADER = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko)"}

    def __init__(self):
        db_malaysia_patient_cases.connect()
        db_malaysia_states.connect()

    def get_details(self):
        self._get_state_details()
        self._get_case_details()

    # state details
    def _get_state_details(self):
        url = "https://www.outbreak.my/"
        print("Scraping", url)
        res = requests.get(url, headers=ScrapeMalaysia.HEADER)
        page = BeautifulSoup(res.content, "html.parser")
        tables = page.find("table", {"class": "table"})
        tbody = tables.find("tbody")
        row = tbody.find("tr")

        state_details = []
        col = row.find("td")
        cur = []
        while col:
            text = col.text.strip()

            # increment count
            if not text:
                cur.append(int(text) if text else 0)
            # other counts
            elif text[0].isdigit() or text[0] == "-":
                if text == "-":
                    cur.append(0)
                else:
                    text = int(text) if text[0] != "-" else int(text[1:]) * -1
                    cur.append(text)
            # string
            else:
                if not cur:
                    cur.append(text)
                else:
                    if len(cur) <= 1 or cur[0] == "Total" or cur[0] == "Undisclosed":
                        break
                    state_details.append(cur)
                cur = [text]
            col = col.findNext(["td"])

        # output: [State name, increment count, total, hospital, recovered, death, last_updated]
        for data in state_details:
            db_malaysia_states.insert(
                {
                    "state": data[0],
                    "increment_count": data[1],
                    "total_count": data[2],
                    "hospital_count": data[3],
                    "recovered_count": data[4],
                    "death_count": data[5],
                    "last_updated": datetime.now().strftime(ScrapeMalaysia.DATETIME_FORMAT),
                },
                ScrapeMalaysia.TABLE,
            )


    # case details
    def _get_case_details(self):
        url = "https://www.outbreak.my/stats"
        print("Scraping", url)
        res = requests.get(url, headers=ScrapeMalaysia.HEADER)
        page = BeautifulSoup(res.content, "html.parser")
        tables = page.find("div", {"class": "col-md-6 col-xl-6"})

        col = tables.find(["td", "span", "strong", "div"])
        raw = []
        while col:
            text = col.get_text().strip()
            raw.append(text.split("\n"))
            col = col.findNext("div", {"class": "col-md-6 col-xl-6"})

        patients = []
        for data in raw:
            patient = {
                "case": None,
                "status": None,
                "status_date": None,
                "confirmed_date": None,
                "nationality": None,
                "age": None,
                "gender": None,
                "hospital": None,
                "description": None,
            }
            idx = 0
            seen_hospital = False
            while idx < len(data):
                val = data[idx].strip()

                if not val:
                    idx += 1
                    continue

                if idx == 0 and "case" in val.lower():
                    patient["case"] = int(val[val.index("#") + 1 :])
                elif "recovered" in val.lower() or "death" in val.lower():
                    status, date = val.split()
                    patient["status"] = status if status else None
                    patient["status_date"] = parser.parse(date).strftime(ScrapeMalaysia.DATETIME_FORMAT)
                elif "confirmed date" in val.lower():
                    date = val.replace("Confirmed Date:", "")
                    patient["confirmed_date"] = parser.parse(date.strip()).strftime(
                        ScrapeMalaysia.DATETIME_FORMAT
                    )
                elif val == "Nationality":
                    idx += 1
                    while idx < len(data) and data[idx].strip() == "":
                        idx += 1
                    patient["nationality"] = (
                        data[idx].strip() if data[idx].strip() else None
                    )
                elif val == "Age":
                    idx += 1
                    while idx < len(data) and data[idx].strip() == "":
                        idx += 1
                    patient["age"] = (
                        int(data[idx].strip()) if data[idx].strip().isdigit() else None
                    )
                elif val == "Gender":
                    idx += 1
                    while idx < len(data) and data[idx].strip() == "":
                        idx += 1
                    patient["gender"] = (
                        data[idx].strip()
                        if data[idx].strip() and data[idx].strip() != "?"
                        else None
                    )
                elif val == "Hospital":
                    idx += 1
                    while idx < len(data) and data[idx].strip() == "":
                        idx += 1
                    patient["hospital"] = data[idx].strip() if data[idx].strip() else None
                    seen_hospital = True
                else:
                    patient["description"] = (
                        "".join(data[idx:]).strip() if "".join(data[idx:]).strip() else None
                    )
                    break
                idx += 1
            patients.append(patient)
            db_malaysia_patient_cases.insert(patient, ScrapeMalaysia.TABLE)
        # print(patients)


if __name__ == "__main__":
    ScrapeMalaysia().get_details()
