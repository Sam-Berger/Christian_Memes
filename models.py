import os
from sqlalchemy import Column, String, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

# TODO: Makke sure the right database path is set for online vs local
# database_path = "postgresql://postgres:postgres@localhost:5432/postgres"
database_path = os.environ['DATABASE_URL']
# if database_path.startswith("postgres://"):
#   database_path = database_path.replace("postgres://", "postgresql://", 1)

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
    # db.create_all()

def db_drop_and_create_all():
    db.drop_all()
    db.create_all()
    # add demo row which is helping in POSTMAN test
    tag1 = Tag(name = "New Testament")
    tag2 = Tag(name = "Old Testament")   

    tag1.insert()
    tag2.insert() 

    meme1 = Meme(
      title="NT Funny", 
      url = "ntfunny.com",
    )
    meme2 = Meme(
      title="OT Funny", 
      url = "otfunny.com",
    )
    meme3 = Meme(
      title="Bible Funny", 
      url = "biblefunny.com",
    )
    meme1.tags.append(tag1)
    meme2.tags.append(tag2)
    meme3.tags.append(tag1)
    meme3.tags.append(tag2)

    meme1.insert()
    meme2.insert()
    meme3.insert() 


#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

meme_tag = db.Table('meme_tag',
                    db.Column('meme_id', db.Integer, db.ForeignKey('meme.id')),
                    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
                    )


class Meme(db.Model):

    id = Column(db.Integer, primary_key=True)
    title = Column(db.String, nullable=False)
    url = Column(db.String, nullable=False, unique=True)
    tags = db.relationship('Tag', secondary=meme_tag, backref='memes')


    '''
    insert()
        inserts a new model into a database
        the model must have a unique id or null id
        EXAMPLE
            meme = Meme(title=req_title, url=req_url, tags=[1,2])
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
            'url': self.url,
        }
      
    def __repr__(self):
      return f'<id: {self.id}, title: {self.title}, url:{self.url}>'

class Tag(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)

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

