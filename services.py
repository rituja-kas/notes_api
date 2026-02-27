# Written the business logic for all the CRUD operations
from storage import notes
from schemas import NoteCreate, NoteUpdate


def create_note(note: NoteCreate):
    new_id = len(notes)+1
    note_dict = {"id": new_id, "title": note.title,"content": note.content}
    notes.append(note_dict)
    return note_dict

def get_all_note():
    return notes

def get_note_by_id(note_id:int):
    for note in notes:
        if note["id"] == note_id:
            return note
    return None

def update_note(note_id:int,note: NoteUpdate):
    for existing_note in notes:
        if existing_note["id"] == note_id:
            if note.title is not None:
                existing_note['title'] = note.title
            if note.content is not None:
                existing_note["content"] = note.content
        return existing_note
    return None


def delete_note(note_id:int):
    for index,note in enumerate(notes):
        if note["id"] == note_id:
            deleted_note = notes.pop(index)
            return deleted_note
    return None

