import os
from sqlalchemy import Column, String, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
database_path = "postgresql://postgres:postgres@localhost:5432/postgres"
# TESTCOMMENT
# database_path = os.environ['DATABASE_URL']
if database_path.startswith("postgres://"):
  database_path = database_path.replace("postgres://", "postgresql://", 1)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

meme_tag = db.Table('meme_tag',
                    db.Column('meme_id', db.Integer, db.ForeignKey('meme.id')),
                    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
                    )


class Meme(db.Model):
    # __tablename__ = 'meme'

    id = Column(db.Integer, primary_key=True)
    title = Column(db.String, nullable=False)
    url = Column(db.String, nullable=False, unique=True)
    tags = db.relationship('Tag', secondary=meme_tag, backref='memes')


    '''
    insert()
        inserts a new model into a database
        the model must have a unique id or null id
        EXAMPLE
            meme = Meme(title=req_title, url=req_url)
            meme.insert()
    '''

    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete()
        deletes a model into a database
        the model must exist in the database
        EXAMPLE
            meme = Meme(title=req_title, url=req_url)
            meme.delete()
    '''

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    update()
        updates a new model into a database
        the model must exist in the database
        EXAMPLE
            meme = Meme.query.filter(Meme.id == id).one_or_none()
            meme.title = 'John on a Horse'
            meme.update()
    '''

    def update(self):
        db.session.commit()

    '''
    view()
        creates a representation of the Meme model
    '''
    def view(self):
        return {
            'id': self.id,
            'title': self.title,
            'url': self.url
        }
      
    def __repr__(self):
      return f'<id: {self.id}, title: {self.title}, url:{self.url}>'

class Tag(db.Model):
    # __tablename__ = 'tag'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    # meme_id = db.Column(db.Integer, db.ForeignKey('meme.id'))

    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete()
        deletes a model into a database
        the model must exist in the database
        EXAMPLE
            tag = Tag(name=req_name)
            meme.delete()
    '''

    def delete(self):
        db.session.delete(self)
        db.session.commit()


    '''
    update()
        updates a new model into a database
        the model must exist in the database
        EXAMPLE
            tag = Tag.query.filter(Tag.id == id).one_or_none()
            tag.title = 'Black Coffee'
            tag.update()
    '''

    def update(self):
        db.session.commit()

    '''
    view()
        creates a representation of the Tag model
    '''
    def view(self):
        return {
            'id': self.id,
            'name': self.name
        }

    def __repr__(self):
      return f'<id: {self.id}, name: {self.name}>'


# '''
# Person
# Have title and release year
# '''
# class Person(db.Model):  
#   __tablename__ = 'People'

#   id = Column(db.Integer, primary_key=True)
#   name = Column(String)
#   catchphrase = Column(String)

#   def __init__(self, name, catchphrase=""):
#     self.name = name
#     self.catchphrase = catchphrase

#   def format(self):
#     return {
#       'id': self.id,
#       'name': self.name,
#       'catchphrase': self.catchphrase}
