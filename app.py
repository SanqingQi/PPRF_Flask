from flask import Flask,render_template,request,redirect,url_for
import util
import math
import os
import datetime

app = Flask(__name__)


@app.route('/', methods=["POST", "GET"])
def mainPage():
    """
    为了方便就直接确定用户名和密码了
    """
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'sjtu123.+':
            return redirect(url_for('admin'))
        else:
            return render_template('index.html')
    else:
        return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/admin/addUser', methods=["POST", "GET"])
def addUser():
    successInfo=""
    if request.method=='POST':
        status=request.form['status']
        if status=='Failed':
            return render_template('addUser.html')
        username = request.form['username']
        ID = request.form['userID']
        Age=request.form['userAge']
        userDepartment=request.form['userDepartment']
        if(util.select_by_id(int(ID))=="无"):
            util.insert(int(ID),username,int(Age),userDepartment)
            successInfo = "插入成功"
        else:
            successInfo="ID重复，插入失败"
    return render_template('addUser.html',successInfo=successInfo)

@app.route('/admin/deleteUser',methods=["POST", "GET"])
def deleteUser():
    target_info=("无","无","无","无")
    deleteSuccess = ' '
    if request.method=='POST':
        action_type=request.form['action_type']
        if action_type=='select':
            target_id=request.form['select_id']
            print(target_id)
            print(type(target_id))
            target_id=int(target_id)
            target_info=util.select_by_id(target_id)
            if(target_info=="无"):
                target_info=("无","无","无","无")
            render_template('deleteUser.html', target_info=target_info,success=deleteSuccess)
        if action_type=='delete':
            delete_id=request.form['delete_id']
            if(delete_id=="无"):
                render_template('deleteUser.html', target_info=target_info, success=deleteSuccess)
            else:
                pass
            deleteSuccess='删除成功'
            render_template('deleteUser.html', target_info=target_info, success=deleteSuccess)
    return render_template('deleteUser.html', target_info=target_info, success=deleteSuccess)

@app.route('/admin/userInfo/<page>',methods=["POST", "GET"])
def userInfo(page=1):
    """
    select user info
    每页只能展示8个用户
    """
    page=int(page)
    if(page<1):
        page = 1
    start_index=8*page-8
    count=(util.get_count()[0])
    total_page=math.ceil(count/8)
    if start_index>count:
        page=total_page
        userInfo=util.select_by_index(8*total_page-8)
    else:
        userInfo=util.select_by_index(start_index)
    return render_template('userInfo.html', infos=userInfo, page=page)

@app.route('/admin/checkRecord',methods=["POST", "GET"])
def checkRecord():
    """
    记录日志
    """
    if request.method=='POST':
        year=request.form['year']
        month=str(int(request.form['month']))
        day=request.form['day']
    else:
        now_time = str(datetime.datetime.now())
        now_time = now_time.split(' ')[0].split('-')
        year=now_time[0]
        month=str(int(now_time[1]))
        day=now_time[2]
    fileName ='record/'+ year+'_'+month+'_'+day+ '.txt'
    date = year+'年'+month+'月'+day+'日 '
    successInfo="暂时无人认证"
    info = []
    if not os.path.exists(fileName):
        f = open(fileName, 'w')
        f.close()
        successInfo = "暂时无人认证"
        info = [['NULL', 'NULL', 'NULL', 'NULL', 'NULL!']]
    else:
        with open(fileName, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.split('-')
                info.append(line)
                successInfo = ''
        if len(info)==0:
            info = [['NULL', 'NULL', 'NULL', 'NULL', 'NULL!']]
    return render_template('checkRecord.html', date=date,successInfo=successInfo,infos=info)

if __name__ == '__main__':
    app.run()
