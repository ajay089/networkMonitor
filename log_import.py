import os
import django
import asyncio
from concurrent.futures import ThreadPoolExecutor

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'networkMonitor.settings')

# Setup Django environment
django.setup()

from apps.backend.models import Logs

# Read the text file
file_path = os.path.join('media', 'raw_data.log')
with open(file_path, 'r') as file:
    log_entries = file.read().split('\n')

# Parse the log entries
def parse_log_entry(log_entry):
    log_data = {}
    for part in log_entry.split():
        if '=' in part:
            key, value = part.split('=', 1)  # Split only on the first '='
            log_data[key] = value.strip('"')
    return log_data

parsed_entries = [parse_log_entry(entry) for entry in log_entries if entry]

# List of fields defined in the Logs model
model_fields = [field.name for field in Logs._meta.fields]

# Function to save entries asynchronously
async def save_entries(entries):
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor(max_workers=4) as executor:
        await asyncio.gather(*[
            loop.run_in_executor(executor, save_entry, entry) for entry in entries
        ])

# Function to save a single entry
def save_entry(entry):
    print(entry)
    filtered_entry = {key: value for key, value in entry.items() if key in model_fields}
    try:
        Logs.objects.create(**filtered_entry)
    except Exception as e:
        pass

# Run the asynchronous saving process
if __name__ == "__main__":
    asyncio.run(save_entries(parsed_entries))
