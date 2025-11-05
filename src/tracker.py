import importlib,models
importlib.reload(models)

from models import Applications, Preparation, Statuses
from typing import Optional, List


class Tracker:
    def __init__(self)->None:
        self.applications=[]
        self.tasks=[]

        self._next_app_id:int=1
        self._next_prep_id:int=1

        self._app_index:dict[int,Applications]={}

    #-------Application----------
    def add_app(self,Company:str,Role:str,Location:str,Source:str,Deadline:str)->Applications:
        app=Applications(
            Id=self._next_app_id,
            Company=Company.strip(),
            Role=Role.strip(),
            Location=Location.strip(),
            Source=Source.strip(),
            Deadline=Deadline.strip(),
            Status=Statuses.APPLIED
        )
        self.applications.append(app)
        self._app_index[app.Id]=app
        self._next_app_id+=1

        return app

    def find_app(self,app_id:int)->Optional[Applications]:
        return self._app_index[app_id] if app_id in self._app_index else None


    def update_status(self,app_id:int,new_status:str)->Applications:
        app=self.find_app(app_id)
        if app is None:
            raise valueError("Not Found")
        app.update_status(new_status)
        return app

    def list_app(self,status_filter:str,sort_by_deadline:bool=False)->List[Applications]:
        sf=status_filter.strip().upper()
        if sf:
            rows=[a for a in self.applications if a.Status.value.startswith(sf)]
        else:
            rows=self.applications[:]

        if sort_by_deadline:
            rows.sort(key=lambda a:(a["Deadline"] if a["Deadline"] else "9999-99-99"))

        return rows

    #----------Preparation--------------
    def add_task(self,Topic:str,Subtopic:str,Due_date:str="",Notes:str="")->Preparation:
        t=Preparation(
            Id = self._next_prep_id,
            Topic=Topic.strip(),
            Subtopic=Subtopic.strip(),
            Due_date=Due_date.strip(),
            Status="TODO",
            Score=None,
            Notes=Notes.strip()
        )
        self.tasks.append(t)
        self._next_prep_id+=1
        return t
    

    def list_tasks(self,topic_filter:str="",status_filter:str="")->List[Preparation]:
        tf=topic_filter.strip().lower()
        sf=status_filter.strip().upper()
        rows=[]
        for t in self.tasks:
            ok_topic=(not tf) or (t.Topic.lower()==tf)
            ok_status=(not sf) or (t.Status.upper()==sf)
            if (ok_topic and ok_status):
                rows.append(t)
        return rows

    def mark_task_done(self,task_id):
        for t in self.tasks:
            if t.Id==task_id:
                t.mark_done()
                return t
        raise valueError("Task ID not found")
                        
            
