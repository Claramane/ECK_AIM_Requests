import requests
import json
import datetime

def get_now():
    now = datetime.datetime.now()
    datetime_format = now.strftime("%Y/%m/%d %H:%M")
    return datetime_format

def ECG_url(ChartNo):
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'Cookie': 'IsLogin=IsLogin',
        'Authorization': 'Bearer eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJVc2VySUQiOiIwMjAwMyIsIlVzZXJOYW1lIjoi6Zmz54eB5pmoIiwiU3RhZmZLZXkiOiIwMjAwM1x1MDAyNumZs-eHgeaZqCIsIlBlcm1pc3Npb24iOiJSZW9wZW5DYXNlQW55UmVjb3JkLCBWaWV3QW55UmVjb3JkLCBFZGl0QW55UmVjb3JkLCBEZWxldGVBbnlSZWNvcmQifQ.jEXzWvmsbaBmzyZav10kAzkQKSnFaiVBY9NhPQiUvEVRqfjDKna--cIQwrBLYQl0WRvuzlCnQsIyQlKiKT03-g'
    }

    # ChartNo = "9370516"
    ChartNo = ChartNo.zfill(10)
    payload = {
        "AssessmentDoctor": "02003&陳燁晨",
        "ChartNo": ChartNo,
        "QueryDate" : get_now()
    }

    rs = requests.session()
    r = rs.post("http://172.20.110.161/ECK_AIM_WEB/PinPin/PIN/GetECGReport", headers = header, data = payload)
    r = json.loads(r.text)
    # print(r)
    # print(r["ExamineReportUrl"])
    ECG_url = r["ExamineReportUrl"]
    return ECG_url

def CXR_url(ChartNo):
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'Cookie': 'IsLogin=IsLogin',
        'Authorization': 'Bearer eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJVc2VySUQiOiIwMjAwMyIsIlVzZXJOYW1lIjoi6Zmz54eB5pmoIiwiU3RhZmZLZXkiOiIwMjAwM1x1MDAyNumZs-eHgeaZqCIsIlBlcm1pc3Npb24iOiJSZW9wZW5DYXNlQW55UmVjb3JkLCBWaWV3QW55UmVjb3JkLCBFZGl0QW55UmVjb3JkLCBEZWxldGVBbnlSZWNvcmQifQ.jEXzWvmsbaBmzyZav10kAzkQKSnFaiVBY9NhPQiUvEVRqfjDKna--cIQwrBLYQl0WRvuzlCnQsIyQlKiKT03-g'
    }

    ChartNo = ChartNo.zfill(10)
    payload = {
        "AssessmentDoctor": "02003&陳燁晨",
        "ChartNo": ChartNo,
        "QueryDate" : get_now()
    }


    rs = requests.session()
    r = rs.post("http://172.20.110.161/ECK_AIM_WEB/PinPin/PIN/GetCXRReport", headers = header, data = payload)
    r = json.loads(r.text)
    # print(r)
    # print(r["ExamineReportUrl"])
    CXR_url = r["ExamineReportUrl"]
    return CXR_url

    # r = rs.get(ECK_url, headers = header)
    # print(r.text)

def all_image(ChartNo):
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'Cookie': 'IsLogin=IsLogin',
        'Authorization': 'Bearer eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJVc2VySUQiOiIwMjAwMyIsIlVzZXJOYW1lIjoi6Zmz54eB5pmoIiwiU3RhZmZLZXkiOiIwMjAwM1x1MDAyNumZs-eHgeaZqCIsIlBlcm1pc3Npb24iOiJSZW9wZW5DYXNlQW55UmVjb3JkLCBWaWV3QW55UmVjb3JkLCBFZGl0QW55UmVjb3JkLCBEZWxldGVBbnlSZWNvcmQifQ.jEXzWvmsbaBmzyZav10kAzkQKSnFaiVBY9NhPQiUvEVRqfjDKna--cIQwrBLYQl0WRvuzlCnQsIyQlKiKT03-g'
    }
    payload = {
        "patientID": ChartNo,
    }
    ChartNo = ChartNo.zfill(10)
    rs = requests.session()
    r = rs.get(f"http://172.23.0.10/html5/index.html?patientID={ChartNo}", headers = header)
    r.encoding = "BIG5"
    print(r.text)

# all_image("0000914200")






