from flask import Flask,render_template,request,redirect,url_for

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
    if request.method=='POST':
        status=request.form['status']
        if status=='Failed':
            return render_template('addUser.html')
        username = request.form['username']
        ID = request.form['userID']
        uerDepartment=request.form['uerDepartment']
        """add function"""
    return render_template('addUser.html')

@app.route('/admin/deleteUser',methods=["POST", "GET"])
def deleteUser():
    target_info=[' ',' ',' ']
    deleteSuccess = ' '
    if request.method=='POST':
        action_type=request.form['action_type']
        if action_type=='select':
            target_id=request.form['select_id']
            target_id=int(target_id)
            """
            ToDo:
            select by id
            """
            target_info=['name',target_id,'department']
            render_template('deleteUser.html', target_info=target_info,success=deleteSuccess)
            pass
        if action_type=='delete':
            delete_id=request.form['delete_id']
            """
            delete target
            """
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
    start_index=7*page-6
    end_index=7*page
    """
    应该还要获取数据库中有多少条记录，page过大时候显示最后一页
    select form start to end index
    userInfo格式：[[name1,id1,department1],[name2,id2,department2]...]
    """
    userInfo="your result"
    return render_template('userInfo.html', info=userInfo)

@app.route('/admin/checkRecord',methods=["POST", "GET"])
def checkRecord():
    """
    记录日志，不过建议使用一个txt文件记录每天的日志 这里就先不弄了
    """
    return render_template('checkRecord.html')

if __name__ == '__main__':
    app.run()
