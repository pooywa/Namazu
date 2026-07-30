from sqlalchemy import Select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.database.configuration import session,engine
from app.database.models import Earthquake

#create table in database
Earthquake.metadata.create_all(engine)

#create manager for crud operation
class ManageDB:
    def __init__(self,session:Session):
        self.session = session
    
    def create(self,instanse):
        try:
            self.session.add(instanse)
            self.session.commit()
        except IntegrityError as e:
            print("dublication error: the object already existed")
            self.session.rollback()
            raise
        except Exception as e:
            print(f"error: {e}")
            self.session.rollback()
            return None

    def read(self,stmt:Select,method="one_or_none"):
        obj = self.session.execute(stmt)
        methods = {
        "one": obj.scalar_one,
        "one_or_none": obj.scalar_one_or_none,
        "first": obj.scalars().first,
        "all": lambda: obj.scalars().all(),
        }
        return methods[method]()

    def update(self,attr,new_value,stmt:Select="",method="one",object=None):
        try:
            if not object:
                obj = self.read(stmt,method)
            else:
                obj = object

            if obj == None:
                print("object not found")
                return
            
            if isinstance(getattr(obj,attr),list) :
                getattr(obj,attr).append(new_value)
            else:
                setattr(obj,attr,new_value)
            self.session.commit()
        except:
            self.session.rollback()

    def delete(self,stmt=None,object=None):
        if object :
            obj = object
        else:
            obj = self.read(stmt,"one")

        self.session.delete(obj)
        self.session.commit()

managedb = ManageDB(session=session)

