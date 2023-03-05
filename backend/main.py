from fastapi import FastAPI,Path
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

class Student(BaseModel):
    name:str
    age : int

class update(BaseModel):
    name:Optional[str]=None
    age : Optional[int]=None

names={
    1:{
    "name":"anmar",
    "age":23,
    },
    2:{
    "name":"nemo",
    "age":50,
    },
}
@app.get("/")
def index():
    return "anmar"

# # the none here is to catch the error if the field is empty
# # path parameter
# # http://localhost:8000/get-name/1
@app.get("/get-name-byid/{id}")
def get_names(id:int=Path(None,description= "write id number here",gt=0)):
    return names[id]

# # optional to make the field not required to enter by the user
# # qurey parameter
# # http://localhost:8000/get-student-names?name=anmar&age=23
@app.get("/get-student-names-byname")
def get_student_names(*,name:Optional [str]=None,age : int):
    for student_id in names:
        if names[student_id]["name"] == name or names[student_id]["age"] == age:
            return names[student_id]
    return "not found"

# # both qurey and path parameter
# # http://localhost:8000/get-student-names/2?name=nemo
# @app.get("/get-student-names/{id}")
# def get_student_names(*,name:Optional [str]=None,age : Optional[int]=None,id:int):
#     for id in names:
#         if names[id]["name"] == name or names[id]["age"] == age:
#             return names[id]
#     return "not found"


@app.post("/create-students/{id}")
def create(id:int,student:Student):
    if id in names:
        return "already there"
    names[id]=student
    return "added"


# # names[id]["name"]=student.name wont work because names[id] isn't a dict
# # for some reason fastAPI convert it into an object 
# # names is a dictionary, but that's not what we're doing on .name in names[id].name, the .name is getting the attribute named name of names[id], which isn't a dictionary
@app.put("/update-students/{id}")
def update(id:int,student:update):
    if id not in names:
        return "does not exitis"
    if student.name != None:
        names[id].name=student.name
    if student.age != None:
        names[id].age=student.age

    return names[id]

@app.delete("/delete-student")
def delete(id:int):
    if id not in names:
        return "not found"
    del names[id]
    return "student deleted"