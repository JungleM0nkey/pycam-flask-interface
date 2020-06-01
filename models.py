from pycam import db


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String, index=True, unique=True)
    date = db.Column(db.String, index=True, unique=True)

    def __repr__(self):
        return '<User {}>'.format(self.filename)    