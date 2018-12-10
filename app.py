import sqlite
from flask import Flask, render_template, request
import base

app = Flask(__name__)


@app.route('/')
def st():
    return render_template('index.html', state='')


@app.route('/do', methods=['POST'])
def index():
    userName = request.form['userName']
    passWord = request.form['passWord']
    print(userName + passWord)
    # 校验
    if not str(userName).isdigit() or len(userName) != 8:
        return render_template('index.html', state='<script>alert("学号错误")</script>')
    if sqlite.select_sno(userName) > 0:
        return render_template('index.html', state='<script>alert("您已经在本系统进行过评教，不能重复评教")</script>')

    try:
        base.mission(userName, passWord)
        sqlite.put_sno(userName)
        return render_template('index.html', state='<script>alert("评教成功")</script>')
    except BaseException as e:
        print(e)
        return render_template('index.html', state='<script>alert("系统异常,可能是密码错了")</script>')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
