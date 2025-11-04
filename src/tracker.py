
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
        self.Applications.append(app)
        self._app_index[app.id]=app
        self._next_app_id+=1

        return app

    def find_app(self,app_id:int)->Optional[Applications]:
        return self.app_index[app_id] if app_id in self._app_index else None


    def update_status(self,app_id:int,new_status:str)->Applications:
        app.self.find_app(app_id)
        if app is None:
            raise valueError("Not Found")
        app.update_status(new_status)
        return app

    def list_app(self,status_filter:str,sort_by_deadline:bool=False)->List[Applications]:
        sf=status_filter.strip().upper()
        if sf:
            rows=[a for a in self.applications if a.status.value.startswith(sf)]
        else:
            rows=self.applications[:]

        if sort_by_deadline:
            rows.sort(key=lambda a:(a["deadline"] if a["deadline"] else "9999-99-99"))

        return rows

    #----------Preparation--------------
    def add_task(self,topic:str,subtopic:str,due_date:str="",notes:str="")->Preparation:
        t=Preparation(
            id = self._next_prep_id,
            topic=topic.strip(),
            subtopic=subtopic.strip(),
            due_date=due_date.strip(),
            status="TODO",
            score=None,
            notes=notes.strip()
        )
        self.Preaparation.append(t)
        self._next_prep_id+=1
        return t
    

    def list_tasks(self,topic_filter:str="",status_filter:str="")->List[Preparation]:
        tf=topic_filter.strip().lower()
        sf=status_filter.strip().upper()
        rows=[]
        for t in self.tasks:
            ok_topic=(not tf) or (t.topic.lower()==tf)
            ok_status=(not sf) or (t.status.upper()==sf)
            if (ok_topic and ok_status):
                rows.append(t)
        return rows

    def mark_task_done(self,task_id):
        for t in self.tasks:
            if t.id==task_id:
                t.mark_done()
                return t
        raise valueError("Task ID not found")
                        
            
