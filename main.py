from flask import Flask,request,render_template,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:testdb@localhost/noter'
db = SQLAlchemy(app)

class Notes(db.Model):
    __tablename__= 'notes_db'
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(25))
    content = db.Column(db.String(100))
    created_at = db.Column(db.DateTime)

    def __init__(self,title,content):
        self.title = title
        self.content = content
        self.created_at = datetime.now()

@app.route('/',methods=['POST','GET'])
def home():
    notes = db.session.query(Notes)
    return render_template('home.html',notes=notes)

@app.route('/create/',methods=['POST','GET'])   
def create(pk=None):
    if request.method == "POST" and pk==None:
        title = request.form['title']
        content = request.form['note_content']
        note = Notes(title,content)
        db.session.add(note)
        db.session.commit()
        return redirect('/')
    return render_template('notes.html',context = {})

@app.route('/update/<pk>',methods=['POST'])   
def update(pk=None):
    if request.method == "POST":
        context = {}
        context['title'] = request.form['title']
        context['content'] = request.form['note_content']
        notes = db.session.query(Notes).filter(Notes.id==pk).update(context)
        db.session.commit()
        return redirect('/')

@app.route('/notes/<pk>/',methods=['POST','GET'])
def notes(pk):
    context = {}
    notes = db.session.query(Notes).filter(Notes.id==pk)
    for note in notes:
        context['title'] = note.title
        context['content'] = note.content
        context['created_at'] = note.created_at
    return render_template('notes.html',context=context)

@app.route('/delete/<pk>',methods=['POST','GET'])
def delete(pk):
    if request.method == 'POST':
        db.session.query(Notes).filter(Notes.id==pk).delete()
        db.session.commit()
        return redirect('/')

if __name__=='__main__':
    app.run(host='0.0.0.0',debug = True)