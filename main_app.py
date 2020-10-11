from flask import Flask,render_template
from flask import request
import json
import os

app_path = os.path.split(os.path.realpath(__file__))[0]
data_path = app_path + "/data/"

app  = Flask(__name__)

def have_id(id_):
    return os.path.isfile(data_path + id_ + ".json")

@app.route("/")
def index_hello():
    return render_template('index.html')

@app.route("/visit/<cid>")
def show_location_html(cid):
    print("[+]  ID:" + cid)
    return render_template('visit.html',cid=cid)

@app.route("/api/recv",methods=['POST'])
def recv_from_client():
    data =  request.get_data()
    #print(data)
    json_dic = json.loads(data)
    print(str(json_dic))

    id_ = json_dic['id']
    
    if id_ == "":
        return "NO ID"
    
    if have_id(id_):
        return "The id exists"
    
    #save to data folder
    try:
        f = open(data_path + id_ + ".json", "w")
        f.write(data.decode())
        f.close()
    except BaseException as e:
        print(e)
    
    return "ok"

@app.route("/api/list")
def list_logs():
    t = []

    for filename in os.listdir(data_path):
        #print(filename)
        t.append(filename.split('.')[0])
        
    return json.dumps(t)
        
@app.route("/api/readinfo/<cid>")
def read_id_info(cid):
    #get infomation from data 
    try:
        f = open(data_path + cid + ".json", "r")
        data = f.read()
        f.close()
    except BaseException as e:
        print(e)
    
    print(data)
    return json.loads(data)

if __name__ == "__main__":
    print(app_path)
    app.run()