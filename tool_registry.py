from tools.calculator import calculator
from tools.current_time import current_time
from tools.current_date import current_date
from tools.weather import weather
from tools.geocoder import geocoder
from tools.files import read_file, write_file, list_files_in_directory, delete_file
from tools.search import search
from tools.save_memory import save_memory
from tools.retrieve_memory import retrieve_memory

tool_registry = {
    "calculator": calculator,
    "current_time": current_time,
    "current_date": current_date,
    "weather": weather,
    "geocoder": geocoder,
    "read_file": read_file,
    "write_file": write_file,
    "list_files_in_directory": list_files_in_directory,
    "delete_file": delete_file,
    "search": search,
    "save_memory": save_memory,
    "retrieve_memory": retrieve_memory
}