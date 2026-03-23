from fastapi import FastAPI, HTTPException
from app.models import Book, BookUpdate

app = FastAPI(title="DevOps Book API", version="1.0")

# In-memory storage for books
books_db = {}

@app.get("/")
def read_root():
    return {"status": "Online",  "message": "Welcome to the DevOps Book API!", "version": "1.0.0"}

@app.post("/books/", response_model=Book)
def create_book(book: Book):
    if book.id in books_db:
        raise HTTPException(status_code=400, detail="Book with this ID already exists.")
    books_db[book.id] = book
    return book 

@app.get("/books/{book_id}", response_model=Book)
def read_book(book_id: int):
    if book_id not in books_db:
        raise HTTPException(status_code=404, detail="Book not found.")
    return books_db[book_id]

@app.put("/books/{book_id}", response_model=Book)
def update_book(book_id: int, book_update: BookUpdate):
    if book_id not in books_db:
        raise HTTPException(status_code=404, detail="Book not found.")
    existing_book = books_db[book_id]
    updated_book = existing_book.copy(update=book_update.dict(exclude_unset=True))
    books_db[book_id] = updated_book
    return updated_book 

@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    if book_id not in books_db:
        raise HTTPException(status_code=404, detail="Book not found.")
    del books_db[book_id]
    return {"detail": "Book deleted successfully."} 
