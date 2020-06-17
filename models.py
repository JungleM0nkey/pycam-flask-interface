from pycam import db


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String, index=True, unique=True)
    date = db.Column(db.String, index=True, unique=True)

    def __repr__(self):
        return '<User {}>'.format(self.filename)    

class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    res_x = db.Column(db.Integer, index=True)
    res_y = db.Column(db.Integer, index=True)
    rotation = db.Column(db.Integer, index=True)
    effect = db.Column(db.String, index=True)
    #theme = db.Column(db.String, index=True)