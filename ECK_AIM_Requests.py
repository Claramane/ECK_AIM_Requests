import requests
import datetime
import json
import pandas as pd

def cal_age(Birthday):
  now = datetime.datetime.now()
  now.strftime("%Y/%m/%d")
  Birthday = datetime.datetime.strptime(Birthday, "%Y/%m/%d")
  age = now.year - Birthday.year
  # print(age)
  return age

# 取得當下時間 
datetime_format = datetime.datetime.today().strftime("%Y/%m/%d %H:%M")


def Pat_info(ChartNo):
  header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Cookie': 'IsLogin=IsLogin',
    'Authorization': 'Bearer eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJVc2VySUQiOiIwMjAwMyIsIlVzZXJOYW1lIjoi6Zmz54eB5pmoIiwiU3RhZmZLZXkiOiIwMjAwM1x1MDAyNumZs-eHgeaZqCIsIlBlcm1pc3Npb24iOiJSZW9wZW5DYXNlQW55UmVjb3JkLCBWaWV3QW55UmVjb3JkLCBFZGl0QW55UmVjb3JkLCBEZWxldGVBbnlSZWNvcmQifQ.jEXzWvmsbaBmzyZav10kAzkQKSnFaiVBY9NhPQiUvEVRqfjDKna--cIQwrBLYQl0WRvuzlCnQsIyQlKiKT03-g'
  }
  payload = {
    'ChartNo': ChartNo, # "0009370516" 測試用，之後要改成變數ChartNo
    'QueryDate': datetime_format
  }

  # 取得病人基本資料
  pat_info = requests.post('http://172.20.110.161/ECK_AIM_WEB/ShareComponent/GetHISPatientInfo', headers = header, data = payload)
  pat_info = json.loads(pat_info.text)
  PatientName = pat_info["PatientName"]
  Sex = pat_info["Sex"]
  Birthday = pat_info["Birthday"]
  
  if pat_info["Height"] == None:
    Hieght = "--"
    Weight = "--"
  else:
    Hieght = f'{pat_info["Height"]} cm'
    Weight = f'{pat_info["Weight"]} kg'


  PatientInfo = {"PatientInfo": [PatientName, Sex, Birthday, f'{cal_age(Birthday)}歲', Hieght, Weight]}
  PatientInfo = pd.DataFrame(PatientInfo)
  PatientInfo.index = ["PatientName", "Sex", "Birthday", "Age", "Hieght", "Weight"]
  # print(PatientInfo)
  return PatientInfo.to_html(index=True)


def get_data(ChartNo):
  header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Cookie': 'IsLogin=IsLogin',
    'Authorization': 'Bearer eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJVc2VySUQiOiIwMjAwMyIsIlVzZXJOYW1lIjoi6Zmz54eB5pmoIiwiU3RhZmZLZXkiOiIwMjAwM1x1MDAyNumZs-eHgeaZqCIsIlBlcm1pc3Npb24iOiJSZW9wZW5DYXNlQW55UmVjb3JkLCBWaWV3QW55UmVjb3JkLCBFZGl0QW55UmVjb3JkLCBEZWxldGVBbnlSZWNvcmQifQ.jEXzWvmsbaBmzyZav10kAzkQKSnFaiVBY9NhPQiUvEVRqfjDKna--cIQwrBLYQl0WRvuzlCnQsIyQlKiKT03-g'
  }
  payload = {
    'ChartNo': ChartNo, # "0009370516" 測試用，之後要改成變數ChartNo
    'QueryDate': datetime_format
  }
  blood_check = requests.post('http://172.20.110.161/ECK_AIM_WEB/PinPin/PIN/GetBloodCheckViewModel', headers = header, data = payload)
  blood_check = json.loads(blood_check.text)
  bioChem_check = requests.post('http://172.20.110.161/ECK_AIM_WEB/PinPin/PIN/GetBiochemistryCheckViewModel', headers = header, data = payload)
  bioChem_check = json.loads(bioChem_check.text)
  blood_check_df = pd.DataFrame(blood_check)
  bioChem_check_df = pd.DataFrame(bioChem_check)
  df = pd.concat([blood_check_df, bioChem_check_df], ignore_index=True)
  # print(df['LabDataList'])
  LabData_df = []
  for i in df['LabDataList']:
    if i['IsNormal'] == True:
      data = [i['ItemName'],i['ItemValue'],i['CheckDate']]
      LabData_df.append(data)
    else:
      data = [i['ItemName'],"*"+i['ItemValue'],i['CheckDate']]
      LabData_df.append(data)
  LabData_df = pd.DataFrame(LabData_df)
  LabData_df.columns = ["ItemName", "CheckValue", "CheckDate"]
  # LabData_df.set_index("ItemName", inplace=True)
  # LabData_df.columns = ["ItemValue", "CheckDate"]
  # print(LabData_df)

  df_c = LabData_df[(LabData_df["ItemName"]=="GPT (ALT)")|(LabData_df["ItemName"]=="Creatinine")|(LabData_df["ItemName"]=="K")|(LabData_df["ItemName"]=="Hb")|(LabData_df["ItemName"]=="Platelet")|(LabData_df["ItemName"]=="PT")|(LabData_df["ItemName"]=="APTT")]
  df_c.reset_index(inplace = True, drop = True)
  df_c.set_index("ItemName", inplace=True)
  # print(df_c)

  df1 = {"column": [0,0,0,0,0,0,0]}
  df1 = pd.DataFrame(df1)
  df1.index = ["GPT (ALT)", "Creatinine", "K", "Hb", "Platelet", "PT", "APTT"]

  DF = pd.concat([df1, df_c], axis=1)
  Simple_data_df = DF.drop(["column"], axis = 1)
  # print(Simple_data_df)

  Complete_data_df = LabData_df
  Complete_data_df.set_index("ItemName", inplace=True)

  # print(Complete_data_df)
  

  return Simple_data_df.to_html(index=True), Complete_data_df.to_html(index=True)

# 9370516

# while True:
#   # 病例號放這邊，補0到十個數字
#   ChartNo = input("請輸入病例號: ")
#   ChartNo = ChartNo.zfill(10)

#   main(ChartNo) 



