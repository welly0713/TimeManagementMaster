from flask import Flask, render_template,request
import pprint
import os

app = Flask(__name__)

# http://3.26.117.8/Schedule/BandPractice
"/home/ubuntu/Web-BookingSystem/data_storage"
@app.route("/Schedule/<Type>", methods=["GET"])
def Schedule(Type):
    data = []
    # Decide which file to load
    try:FileNames = os.listdir(f"/home/ubuntu/Web-BookingSystem/data_storage/{Type}")
    except:return "<h1>No such File<h1>"

    if len(FileNames) == 1: FileName = f"/home/ubuntu/Web-BookingSystem/data_storage/{Type}/data_init.txt"
    else: FileName = f"/home/ubuntu/Web-BookingSystem/data_storage/{Type}/data_{len(FileNames)-1}.txt"
    
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

    return render_template("Schedule.html", data = data, Type=Type)

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
            FileNames = os.listdir(f"/home/ubuntu/Web-BookingSystem/data_storage/{Type}")
            NewFileName = f"/home/ubuntu/Web-BookingSystem/data_storage/{Type}/data_{len(FileNames)}.txt"

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
        


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)