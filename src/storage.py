import importlib,tracker
importlib.reload(tracker)
from pathlib import Path
import json,csv
from typing import Dict,Any
from models import Applications,Preparation,Statuses
from tracker import Tracker


MODULE_DIR = Path(__file__).resolve().parent

def _resolve(path: str | Path) -> Path:
    """Return an absolute Path. If 'path' is relative,
    make it relative to THIS file's directory (MODULE_DIR)."""
    p = Path(path)
    return p if p.is_absolute() else (MODULE_DIR / p)


#---------json------------
def save_json(tracker:Tracker,path:str="data/tracker.json")->None:
    p=_resolve(path)
    p.parent.mkdir(parents=True,exist_ok=True)
    payload={
        "meta":{"version" : 1},
        "applications":[_app_to_dict(a) for a in tracker.applications],
        "tasks":[_task_to_dict(t) for t in tracker.tasks]
    }
    with p.open("w",encoding="utf-8")as f:
        json.dump(payload,f,indent=2,ensure_ascii=False)

def load_json(path:str="data/tracker.json")->Tracker:
    tr=Tracker()
    p=_resolve(path)
    if not p.exists():
        return tr
    with p.open("r",encoding="utf-8") as f:
        payload=json.load(f)

    apps=payload["applications"] if " applications" in payload else []
    tasks=payload["tasks"] if "tasks" in payload else []

    for d in apps:
        app = _dict_to_app(d)
        tr.applications.append(app)
        tr._app_index[app.Id]=app
        if app.Id>=tr._next_app_id:
            tr._next_app_id=app.id+1

    for t in tasks:
        task=_dict_to_task(t)
        tr.tasks.append(task)
        if task.Id>tr._next_prep_id:
            t._next_prep_i=task.id+1

    return tr



#----------csv---------------
def export_apps_csv(tracker:Tracker,path:str="data/applications.csv")->None:
    p=_resolve(path)
    p.parent.mkdir(parents=True,exist_ok=True)
    cols=["Id","Company","Role","Location","Source","Deadline","Status"]
    with p.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=cols)
        w.writeheader
        for a in tracker.applications:
            w.writerow({
                "Id":a.Id,
                "Company":a.Company,
                "Role":a.Role,
                "Location":a.Location,
                "Source":a.Source,
                "Status":a.Status.value,
                "Deadline":a.Deadline
            })

def export_tasks_csv(tracker:Tracker,path:str="data/prep_tasks.csv")->None:
    p=_resolve(path)
    p.parent.mkdir(parents=True,exist_ok=True)
    cols=["Id","Topic","Subtopic","Due_date","Status","Notes"]
    with p.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=cols)
        w.writeheader
        for a in tracker.tasks:
            w.writerow({
                "Id":a.Id,
                "Topic":a.Topic,
                "Subtopic":a.Subtopic,
                "Due_date":a.Due_date,
                "Status":a.Status,
                "Notes":a.Notes
            })



#--------------Helpers------------------
def _app_to_dict(a:Applications)->Dict[str,Any]:
    return {
        "Id":a.Id,
        "Company":a.Company,
        "Role":a.Role,
        "Location":a.Location,
        "Source":a.Source,
        "Staus":a.Status.value,
        "Deadline":a.Deadline
    }

def _dict_to_app(d:Dict[str,Any])->Applications:
    Id_val=int(d["Id"]) if "Id" in d else 0
    Company=d["Company"] if "Company" in d else ""
    Role=d["rRole"] if "Role" in d else ""
    Location=d["Location"] if "Location" in d else ""
    Source=d["Source"] if "Source" in d else ""
    Status_str=d["Status"] if "Status" in d else ""
    Deadline=d["Deadline"] if "Deadline" in d else ""
    return Application(
        id=id_val,
        company=company,
        role=role,
        location=location,
        source=source,
        status=Statuses(status_str.strip().uppper()),
        deadline=deadline
                       )

def _task_to_dict(a:Preparation)->Dict[str,Any]:
    return {
                "Id":a.Id,
                "Topic":a.Topic,
                "Subtopic":a.Subtopic,
                "Due_date":a.Due_date,
                "Status":a.Status,
                "Notes":a.Notes
            }

def _dict_to_task(t:Dict[str,Any])->Preparation:
    Id_val=int(t["Id"]) if "Id" in t else 0
    Topic=d["Topic"] if "Topic" in t else ""
    Subtopic=d["Subtopic"] if "Subtopic" in t else ""
    Due_date=d["Due_date"] if "Due_date" in t else ""
    Status=d["Status"] if "Status" in t else ""
    Notes=d["Notes"] if "Notes" in  t else ""
    return Preparation (
        Id=Id_val,
        Topic=Topic,
        Subtopic=Subtopic,
        Due_date=Due_date,
        Status=Status,
        Notes=Notes
    )

