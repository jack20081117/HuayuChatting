from flask import Flask,render_template
import os

app=Flask(__name__)

@app.route('/home',methods=['GET','POST'])
def home():
    return render_template('home.html')

@app.route('/week/chart/<schoolID>',methods=['GET','POST'])
def weekchart(schoolID):
    os.system('python weekchart_app.py --id %s'%schoolID)
    return render_template('weekchart.html',schoolID=schoolID)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

if __name__ == '__main__':
    app.run()