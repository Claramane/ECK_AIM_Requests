from flask import Flask, request, render_template, redirect, url_for
from bs4 import BeautifulSoup
import ECK_AIM_Requests
import ECK_Image_Requests

app = Flask(__name__)
@app.route('/', methods=['POST', 'GET'])
def index():
    patInfo = None
    Simple_data_df = None
    Complete_data_df = None
    if request.method == "POST":
        global ChartNo
        
        ChartNo = request.form["ChartNo"]
        ChartNo = ChartNo.zfill(10)
        # print(request.form["ChartNo"])
        print(ChartNo)
        
        patInfo = ECK_AIM_Requests.Pat_info(ChartNo)
        Simple_data_df, Complete_data_df = ECK_AIM_Requests.get_data(ChartNo)

        soup = BeautifulSoup(Complete_data_df, 'lxml')
        table = soup.find('table')
        tr = soup.select('tr:nth-of-type(2)')[0]
        tr.extract()
        # print(table)
        Complete_data_df = table
        # print(patInfo)
        # print(Simple_data_df, Complete_data_df)
    return render_template("AIM_result.html", patInfo = patInfo, Simple_data_df = Simple_data_df, Complete_data_df = Complete_data_df)
    

# @app.route('/', methods=['POST', 'GET'])
# def show_result():
#     title = "顆顆顆"
#     if request.method == "POST":
#         try:
#             ChartNo = ChartNo.zfill(10)
#             patInfo = ECK_AIM_Requests.Pat_info(ChartNo)
#             df1, df2 = ECK_AIM_Requests.get_data(ChartNo)
#             print(patInfo)
#             # print(df1, df2)
#             return render_template("show_result.html", html_result = patInfo)  
#             try:
#                 ECG_url = ECK_Image_Requests.ECG_url(ChartNo)
#                 CXR_url = ECK_Image_Requests.CXR_url(ChartNo)
#                 # print(ECG_url, CXR_url)
#                 # print(f"http://172.23.0.10/html5/index.html?patientID={ChartNo}")
#             except:
#                 print("Cannot find image!!!")
#         except:
#             print("Error!!!")


if __name__ == '__main__':
    app.run(host='10.1.5.88', port=5566, debug=True)