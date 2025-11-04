

from dataclasses import dataclass,asdict
from datetime import date,time
from typing import Optional,List,Dict,Any
from enum import Enum


class Statuses(str,Enum): #ENUM AVOID TYPOS
    APPLIED = "APPLIED"
    ONLINE_TEST="ONLINE_TEST"
    HR_SCREEN="HR_SCREEN"
    TECH1="TECH1"
    TECH2="TECH2"
    OFFER="OFFER"
    REJECTED="REJECTED"

def _parse_date(d:str)->Optional[date]:
    if not d:
        return None
    try:
        datetime.strptime(d,"%y-%m-%d").date()
    except valueError:
        return  None



@dataclass
class Applications:
    id:int
    Company:str
    Role:str
    Location:str=""
    Source:str=""
    Deadline:str=""   #keep as YYYY-MM-DD ,OTHERWISE IT WON'T PARSE
    Status:Statuses=Statuses.APPLIED

    def update_status(self,new_Status:str)->None:
        s=new_status.strip().upper()
        if s not in Statuses.__members__:
            raise valueError(f'Invalid Status: {new_status}')
        self.Status=Statuses[s]

    def days_left(self)->Optional[int]:
        d=_parse_date(self.Deadline)
        return None if d is None else (d-date.today()).days

    def to_dict(self)->Dict[str,Any]:
        d=asdict(self)
        d["Status"]=self.Status.value
        return d
    @staticmethod
    def from_dict(d:Dict[str,Any])->"Application":
        return Applications(
            id=int(d["id"]),
            Company=d["Company"],
            Role=d["Role"],
            Location=d.get("Location",""),
            Source=d.get("Source",""),
            Deadline=d.get("deadline",""),
            Status=Statuses(d.get(Status,"APPLIED")).strip().upper()
        )
        

@dataclass
class Preparation:
    id:int
    Topic:str
    Subtopic:str
    Due_date:str=""
    Status:str="TODO"
    Score:Optional[float]=None
    Notes:str=""

    def mark_done(self)->None:
        self.Status="Done"

    def days_left(self,d)->Optional[int]:
        d=_parse_date(self.Due_date)
        return None if d is None else(d-Date.toaday()).days

    def to_dict(self)->Dict[str,Any]:
        return asdict(self)

    @staticmethod
    def from_dict(d:Dict[str,Any])->"Preparation":
        return Preparation(
            id=int(d["id"]),
            Topic=d["Topic"],
            Subtopic=d["Subtopic"],
            Due_date=d.get("Due_date",""),
            Status=d.get("Status","TODO"),
            Score=None if d.get("Score") in ("",None) else float(d["Score"]),
            Notes=d.get("Notes","")
        )
            
