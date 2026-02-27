from fastapi import FastAPI,HTTPException
from schemas import *
from services import create_note,update_note,delete_note,get_note_by_id,get_all_note
app = FastAPI(title="Internal Notes API")



# create a notes
@app.post('/notes/')
async def create_notes(note:NoteCreate):
    new_note = create_note(note)
    return {"status_code":200,
            "status":"success",
            "detail":new_note
            }


# get the notes
@app.get('/all_notes/')
async def get_all_notes():
    all_notes = get_all_note()
    return {"status_code":200,
            "status":"success",
            "details":all_notes
            }

# get the single notes
@app.get('/notes/{id}')
async def get_note(id:int):
    note = get_note_by_id(id)
    if not note:
        raise HTTPException(status_code=404,detail="note not found")
    return {
        "status_code": 200,
        "status":"success",
        "detail":note
    }


# update a note
@app.put('/update_notes/{id}')
async def notes(id:int,note:NoteUpdate):
    updated_note = update_note(id,note)
    if updated_note:
        return {
            "status_code": 200,
            "status":"success",
            "message":"note updated successfully",
        }
    raise HTTPException(status_code=404,detail="note not found")


@app.delete('/delete_notes/{id}')
async def notes(id:int):
    note  =  get_note_by_id(id)
    if not note:
        raise HTTPException(status_code=404,detail="note not found")
    delete_note(id)
    return {"status_code":200,"status":"success","message":"note deleted successfully"}