from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///catsci_edbo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Project(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    project_name = db.Column(db.VARCHAR(200), nullable = True)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)


    def __repr__(self) -> str:
        return f"{self.sno} - {self.project_name}"



@app.route('/')
def hello_world():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug= True)