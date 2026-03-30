# Import from modules in main loop to avoid loading data before login 
from edit import edit_entry as edit_entry
from log import log_entry as log_entry
from export import export_history as export_history
from view import view_history as view_history 
from view import load_history as load_history

def init_main_menu():
    return {
        'edit_entry': edit_entry,
        'log_entry': log_entry,
        'export_history': export_history,
        'view_history': view_history,
        'load_history': load_history
        }