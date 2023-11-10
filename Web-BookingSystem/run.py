from flask import Flask, render_template,request
import pprint
import os
import datetime,time

app = Flask(__name__)
Route = os.getcwd()
# 初始頁面
@app.route("/Schedule/<Type>/<YearWeek>", methods=["GET"]) #/Schedule/BandPractice/2330
def Schedule(Type, YearWeek):
    data = []
    # Decide which file to load
    try:FileNames = os.listdir(f"{Route}/data_storage/{Type}")
    except:return f"<h1>No such File {Route}/data_storage/{Type}<h1>"

    if len(FileNames) == 1: FileName = f"{Route}/data_storage/{Type}/data_init.txt"
    else: FileName = f"{Route}/data_storage/{Type}/data_{len(FileNames)-1}.txt"
    
    with open(FileName, mode="r", encoding="utf-8") as f:
        
        data += f.readlines()
        data = data[0:8]
        for i in range(len(data)):
            data[i] = data[i].split()
        
        countx = 0
        county = 0
        for i in range(len(data)):
            for j in range(len(data[i])):
                if data[i][j] == '1':
                    data[i][j] = [1,f"{county}{countx}"]
                    countx +=1
                elif data[i][j] == '0':
                    data[i][j] = [0,f"{county}{countx}"]
                    countx +=1

                if countx == 7:
                    countx = 0
                    county +=1
    
    # 處理日期問題
    if YearWeek == "-1":
        Year = int(datetime.datetime.now().isocalendar()[0]) - 2000
        Week = int(datetime.datetime.now().isocalendar()[1])
    else:
        Year = int(YearWeek[:2])
        Week = int(YearWeek[2:])
    date = Week1toWeek7(Year, Week)
    date.insert(0,("YY", "MM", "DD"))

    return render_template("Schedule.html", data = data, Type=Type, Date = date, YearWeek = int(f"{Year}{Week}"))

# 提交
@app.route("/Submit/<Type>", methods=["POST", "GET"])
def Submit(Type):
    try:
        if request.form["name"]:
            data = [[0 for i in range(7)] for j in range(7)]

            # Find the appropriate time
            for i in range(7):
                for j in range(7):
                    if f"checkbox{i}{j}" in request.form:
                        data[i][j] = 1
            pprint.pprint(data)

            # 修改檔案
            # 處理檔案名稱
            FileNames = os.listdir(f"{Route}/data_storage/{Type}")
            NewFileName = f"{Route}/data_storage/{Type}/data_{len(FileNames)}.txt"

            #寫入檔案
            t = 16
            with open(NewFileName, "w", encoding="utf-8") as f:
                f.write("Time Mon Tue Wed Thu Fri Sat Sun\n")
                for i in range(7):
                    f.write(f"{t}:00 {data[i][0]} {data[i][1]} {data[i][2]} {data[i][3]} {data[i][4]} {data[i][5]} {data[i][6]}\n")
                    t+=1
                f.write(f"修改者 : {request.form['name']}")
            # 可加成功頁面
            return "<h1>Success<h1>"
        else:
            # 可加失敗頁面
            return "<h1>Please Enter Valid Name<h1>"
    except Exception as e:
        return str(e)
        
def Week1toWeek7(Year, Week):
    Year += 2000

    # first_day = (Year-01-01)
    first_day = datetime.date(Year, 1,1)
    
    # 計算first_day是星期幾
    first_day_Weekday = first_day.weekday()
    
    # 計算第一天距離該周第一天天數差距
    days_to_Week1 = 7 - first_day_Weekday

    #取得目標週的第一天
    target_week1 = first_day + datetime.timedelta(days= days_to_Week1 + 7*(Week-1))
    
    date = [target_week1 + datetime.timedelta(days= x) for x in range(7)]
    date = [(x.year, str(x.month).zfill(2), str(x.day).zfill(2)) for x in date]

    return(date)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug=True)