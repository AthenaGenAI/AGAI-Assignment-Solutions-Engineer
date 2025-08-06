import os
import time
from django.core.management.base import BaseCommand
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from records.utils.file_processors import process_email_file, process_form_file, process_invoice_file


class DataFileHandler(FileSystemEventHandler):
    """Handler for file system events in data directories"""
    
    def on_created(self, event):
        """Called when a new file is created"""
        if event.is_directory:
            return
            
        file_path = event.src_path
        print(f"New file detected: {file_path}")
        
        try:
            # Determine file type and process accordingly
            if file_path.endswith('.eml') and 'emails' in file_path:
                print(f"Processing email file: {file_path}")
                process_email_file(file_path)
                
            elif file_path.endswith('.html') and 'forms' in file_path:
                print(f"Processing form file: {file_path}")
                process_form_file(file_path)
                
            elif file_path.endswith('.html') and 'invoices' in file_path:
                print(f"Processing invoice file: {file_path}")
                process_invoice_file(file_path)
                
            else:
                print(f"Unknown file type or location: {file_path}")
                
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")


class Command(BaseCommand):
    help = 'Watch data directories for new files and automatically process them'

    def add_arguments(self, parser):
        parser.add_argument(
            '--path',
            type=str,
            help='Path to the data directory to watch (default: auto-detect)',
        )

    def handle(self, *args, **options):
        # Auto-detect the data directory path
        if options['path']:
            data_path = options['path']
        else:
            # Go up from manage.py to data_dashboard, then to TechFlow-Automation, then to data
            current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
            data_path = os.path.join(current_dir, '..', 'data')
            data_path = os.path.abspath(data_path)
        
        if not os.path.exists(data_path):
            self.stdout.write(
                self.style.ERROR(f'Data directory not found: {data_path}')
            )
            return
            
        self.stdout.write(
            self.style.SUCCESS(f'Starting file watcher for: {data_path}')
        )
        
        # Set up the file watcher
        event_handler = DataFileHandler()
        observer = Observer()
        observer.schedule(event_handler, data_path, recursive=True)
        
        observer.start()
        
        try:
            self.stdout.write(
                self.style.SUCCESS('File watcher is running. Press Ctrl+C to stop.')
            )
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
            self.stdout.write(
                self.style.SUCCESS('File watcher stopped.')
            )
            
        observer.join()
