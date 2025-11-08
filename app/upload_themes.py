import google.generativeai as genai
from google.generativeai import types
import os
import time
from pathlib import Path

# Configure the client
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def get_or_create_file_search_store():
    """Gets or creates a file search store."""
    store_name_file = Path("app/file_search_store.txt")
    if store_name_file.exists():
        store_name = store_name_file.read_text().strip()
        try:
            return genai.file_search_stores.get(name=store_name)
        except Exception:
            pass  # If it fails, create a new one

    for store in genai.file_search_stores.list():
        if store.display_name == 'obs-styla-themes':
            store_name_file.write_text(store.name)
            return store

    store = genai.file_search_stores.create(
        config={'display_name': 'obs-styla-themes'}
    )
    store_name_file.write_text(store.name)
    return store


def upload_themes():
    """Uploads all theme files to a File Search store."""
    file_search_store = get_or_create_file_search_store()

    # Upload and import files
    for file_path in Path(".").glob("*.*"):
        if file_path.suffix in [".ovt", ".obt", ".json"]:
            print(f"Uploading {file_path.name}...")
            operation = genai.file_search_stores.upload_to_file_search_store(
                file=str(file_path),
                file_search_store_name=file_search_store.name,
                config={'display_name': file_path.name}
            )
            while not operation.done:
                time.sleep(5)
                operation = genai.operations.get(operation)

    print("All theme files have been uploaded.")

if __name__ == "__main__":
    upload_themes()
