import os
import time
from multiprocessing import Process
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from save_forms_to_excel import create_contact_from_form, create_form_record
from parsers.form_parser import parse_html_form

def process_new_form(file_path):
    """
    Process a new form file: extract data, save to database.

    Args:
        file_path (str): Path to the new form file.
    """
    print(f"Processing new form: {file_path}")
    form_data = parse_html_form(file_path)

    if form_data:
        # Save to database
        contact = create_contact_from_form(form_data)
        form_record = create_form_record(form_data)

        if contact:
            print(f"Contact saved: {contact}")
        if form_record:
            print(f"Form record saved: {form_record}")

class FormHandler(FileSystemEventHandler):
    """
    Custom event handler for new form files.
    """
    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith('.html'):
            process_new_form(event.src_path)

def watch_forms_directory(directory):
    """
    Watch the forms directory for new files.

    Args:
        directory (str): Path to the forms directory.
    """
    print(f"Watching directory: {directory}")
    event_handler = FormHandler()
    observer = Observer()
    observer.schedule(event_handler, directory, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    forms_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../dummy_data/forms/'))

    # Run the file watcher in a separate process
    watcher_process = Process(target=watch_forms_directory, args=(forms_dir,))
    watcher_process.start()

    print("File watcher is running in the background.")

    try:
        # Keep the main process running (e.g., for your server)
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping file watcher...")
        watcher_process.terminate()
        watcher_process.join()
