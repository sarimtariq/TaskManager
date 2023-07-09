from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_detail = db.Column(db.String(150), nullable=False)
    task_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_detail = request.form['content']
        new_task = Task(task_detail=task_detail)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'Sorry, there was a problem with the addition of that task.'

    else:
        items = Task.query.order_by(Task.task_date).all()
        return render_template('index.html', items=items)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Task.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'Sorry, there was a problem deleting that item.'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Task.query.get_or_404(id)

    if request.method == 'POST':
        task.task_detail = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Sorry, there was an issue updating that item.'

    else:
        return render_template('update.html', item=task)


if __name__ == "__main__":
    app.run(debug=True, port=8000)