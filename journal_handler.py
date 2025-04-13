import os
import json
from datetime import datetime



DATA_FILE = "notes.json"  # same file name

# This class handles the note object
class JournalEntry:
    def __init__(self, header, body, created=None):
        self.header = header
        self.body = body
        self.created = created if created else datetime.now().isoformat()

    def serialize(self):
        return {
            "header": self.header,
            "body": self.body,
            "created": self.created
        }

    @staticmethod
    def deserialize(obj):
        return JournalEntry(
            header=obj["header"],
            body=obj["body"],
            created=obj["created"]
        )



# Read journal entries from the file
def fetch_entries():
    if not os.path.isfile(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as handle:
        items = json.load(handle)
        return [JournalEntry.deserialize(x) for x in items]

# Write entries to the file
def save_entries(entries):
    with open(DATA_FILE, "w") as handle:
        json.dump([entry.serialize() for entry in entries], handle, indent=4)


# Create a new entry
def create_entry(header, body):
    collection = fetch_entries()
    new_entry = JournalEntry(header, body)
    collection.append(new_entry)
    save_entries(collection)
    print(f"Saved entry: {header}")



# List all journal entries
def show_entries():
    collection = fetch_entries()
    if not collection:
        print("No entries yet.")
        return
    for i, entry in enumerate(collection, 1):
        print(f"{i}. {entry.header} ({entry.created})")


# Show detailed entry content
def show_detail(index):
    collection = fetch_entries()
    if 0 <= index < len(collection):
        entry = collection[index]
        print("\n--- Entry Details ---")
        print("Header:", entry.header)
        print("Date:", entry.created)
        print("Body:\n" + entry.body)
    else:
        print("Entry not found.")


# Menu controller
def start_interface():
    while True:
        print("\n== Journal ==")
        print("1) New Entry")
        print("2) List Entries")
        print("3) View Entry")
        print("4) Quit")

        action = input("Action: ")

        if action == "1":
            header = input("Header: ")
            body = input("Body: ")
            create_entry(header, body)

        elif action == "2":
            show_entries()

        elif action == "3":
            num = int(input("Entry #: ")) - 1
            show_detail(num)

        elif action == "4":
            break

        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    start_interface()
