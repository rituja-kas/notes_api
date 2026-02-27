**Internal Notes API**
This project provides a simple CRUD API for managing internal notes.
You can create, update, read, and delete notes using FastAPI.


**How to run the project.**
1.clone the repository.
2.create the virtual environment and install dependencies.
3.start the fastapi server:uvicorn main:app --reload
4.open swagger UI to check the API's working:http://127.0.0.1:8000/docs
**API endpoint**
1.To create a new notes use (http://127.0.0.1:8000/notes/)endpoint
2.To get all the notes use (http://127.0.0.1:8000/all_notes/)endpoint
3.To get the selected notes use (http://127.0.0.1:8000/notes/{id})endpoint
4.To update the notes by title or content use (http://127.0.0.1:8000/update_notes/{id})
5.To delete the specific note use (http://127.0.0.1:8000/update_notes/{id})

**Example**
1.create a new notes
{"title":"AI",
"content":"Artificial Intelligence helps to do the task"
2.get all notes-no params required,it will automatically give all the notes detail
3.get the notes by id we need to give an id number in parameter
4.update the either content or title in notes we have to provide id in params and update any of content or title of the notes.
5.delete the notes detail we need to give an id number in parameter after that it will delete all the detail of notes