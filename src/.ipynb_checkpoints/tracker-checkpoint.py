
import models
importlib.reload(models)

from models import Applications, Preparation, Statuses
from typing import Optional, List

class Tracker:
    def __init__(self)->None:
        self.Applications:List[Applications]=[]
        self.preparation:List[Preparation]=[]

        self._next_app_id:int=1
        self._next_prep_id:int=1

        self._app_index:dict[int,Applications]={}

    #-------Application----------
    def add_app(self,company:str,role:str,location:str,source:str,deadline:str)->Applications:
        app=Applications(
            id=self.next_app_id,
            company=company.strip(),
            location=location.strip(),
            source=source.strip(),
            deadline=deadline.strip(),
            status=Statuses.APPLIED
        )
        self.Applications.appen(app)
        self._app_index[app.id]=app
        self._next_app_id+=1

        return app

