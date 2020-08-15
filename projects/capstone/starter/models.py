from sqlalchemy import Column, String, Integer, DateTime
from flask_sqlalchemy import SQLAlchemy
import os


#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

# database_name = "Casting_Agency"
# database_path = "postgres://{}/{}".format('localhost:5432', database_name)
database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()

'''
setup_db binds a flask application and a SQLAlchemy service
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

class Actor(db.Model):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)

    '''
    ISO/IEC 5218 ---> gender
    0 = Not known;
    1 = Male;
    2 = Female;
    9 = Not applicable.
    '''
    gender = Column(Integer, nullable=False)

    '''
    Movie class has not been created.
    use strings to refer to classes that are not created yet.

    Declarative initializer allows string arguments to be passed to relationship(). 
    These string arguments are converted into callables that evaluate the string as 
    Python code, using the Declarative class-registry as a namespace. This allows 
    the lookup of related classes to be automatic via their string name, and removes 
    the need for related classes to be imported into the local module space before 
    the dependent classes have been declared. 
    
    It is still required that the modules in which these related classes appear are 
    imported anywhere in the application at some point before the related mappings 
    are actually used, else a lookup error will be raised when the relationship() 
    attempts to resolve the string reference to the related class.
    '''
    movies = db.relationship('Movie', backref='protagonist', lazy=False)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender
    
    def __repr__(self):
        return f'<Actor No.{self.id} is {self.name}.>'
    
    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }



class Movie(db.Model):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    release_date = Column(DateTime, nullable=False)
    '''
    ForeignKey takes a single target column
    a column object or a column name as a string
    eg: db.ForeignKey(other_class.__tablename__.id)
    '''
    actor_id = Column(Integer, db.ForeignKey('actors.id'))

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date
    
    def __repr__(self):
        return f'<Movie No.{self.id} is {self.name}.>'
    
    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
            'actor_id': self.actor_id
        }


