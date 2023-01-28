from flask import Flask,render_template,request
import os

app=Flask(__name__)

@app.route('/home',methods=['GET','POST'])
def home():
    return render_template('home.html')

@app.route('/month/chart/',methods=['GET'])
def monthchart():
    return render_template('monthchart.html')

@app.route('/month/chart/',methods=['POST'])
def monthchart_form():
    schoolID=request.form['schoolID']
    os.system('python monthchart_app.py --id %s'%schoolID)
    return render_template('monthchart.html',schoolID=schoolID)

@app.route('/month/chart/<schoolID>',methods=['GET','POST'])
def monthchart_id(schoolID):
    os.system('python monthchart_app.py --id %s'%schoolID)
    return render_template('monthchart.html',schoolID=schoolID)

@app.route('/week/chart/',methods=['GET'])
def weekchart():
    return render_template('weekchart.html')

@app.route('/week/chart/',methods=['POST'])
def weekchart_form():
    schoolID=request.form['schoolID']
    os.system('python weekchart_app.py --id %s'%schoolID)
    return render_template('weekchart.html',schoolID=schoolID)

@app.route('/week/chart/<schoolID>',methods=['GET','POST'])
def weekchart_id(schoolID):
    os.system('python weekchart_app.py --id %s'%schoolID)
    return render_template('weekchart.html',schoolID=schoolID)

@app.route('/day/chart/',methods=['GET'])
def daychart():
    return render_template('daychart.html')

@app.route('/day/chart/',methods=['POST'])
def daychart_form():
    schoolID=request.form['schoolID']
    os.system('python daychart_app.py --id %s'%schoolID)
    return render_template('daychart.html',schoolID=schoolID)

@app.route('/day/chart/<schoolID>',methods=['GET','POST'])
def daychart_id(schoolID):
    os.system('python daychart_app.py --id %s'%schoolID)
    return render_template('daychart.html',schoolID=schoolID)

@app.route('/week/pie/',methods=['GET','POST'])
def weekpie():
    return render_template('weekpie.html')

@app.route('/week/pie/<time>',methods=['GET','POST'])
def weekpie_time(time):
    os.system('python weekpie_app.py --time %s'%time)
    return render_template('weekpie.html',time=time)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

if __name__ == '__main__':
    app.run()