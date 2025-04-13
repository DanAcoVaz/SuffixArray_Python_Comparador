import os
import json
from datetime import datetime

NOTES_FILE = "notes.json"

class Note:
    def __init__(self, title, content, timestamp=None):
        self.title = title
        self.content = content
        self.timestamp = timestamp or datetime.now().isoformat()

    def to_dict(self):
        return {
            "title": self.title,
            "content": self.content,
            "timestamp": self.timestamp
        }

    @staticmethod
    def from_dict(data):
        return Note(
            title=data["title"],
            content=data["content"],
            timestamp=data["timestamp"]
        )

def load_notes():
    if not os.path.exists(NOTES_FILE):
        return []
    with open(NOTES_FILE, "r") as file:
        data = json.load(file)
        return [Note.from_dict(note) for note in data]

def save_notes(notes):
    with open(NOTES_FILE, "w") as file:
        json.dump([note.to_dict() for note in notes], file, indent=4)

def add_note(title, content):
    notes = load_notes()
    note = Note(title, content)
    notes.append(note)
    save_notes(notes)
    print(f"Note '{title}' saved.")

def list_notes():
    notes = load_notes()
    if not notes:
        print("No notes available.")
        return
    for idx, note in enumerate(notes, 1):
        print(f"{idx}. {note.title} ({note.timestamp})")

def view_note(index):
    notes = load_notes()
    if 0 <= index < len(notes):
        note = notes[index]
        print(f"Title: {note.title}\nDate: {note.timestamp}\nContent:\n{note.content}")
    else:
        print("Invalid note index.")

def main():
    while True:
        print("\nNotes Manager")
        print("1. Add Note")
        print("2. List Notes")
        print("3. View Note")
        print("4. Exit")

        choice = input("Choose an option: ")
        if choice == "1":
            title = input("Title: ")
            content = input("Content: ")
            add_note(title, content)
        elif choice == "2":
            list_notes()
        elif choice == "3":
            index = int(input("Note number: ")) - 1
            view_note(index)
        elif choice == "4":
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
