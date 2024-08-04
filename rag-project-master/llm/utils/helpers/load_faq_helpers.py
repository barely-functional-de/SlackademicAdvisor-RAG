import json
import hashlib
import pandas as pd
from datetime import datetime

METADATA_FILE = 'processed_faq_metadata.json'

def load_json(filename):
    """Load JSON data from a file."""
    with open(filename, 'r') as file:
        data = json.load(file)
    return data

def generate_id(entry):
    """Generate a unique ID based on the entry's properties."""
    hash_input = (f"{entry['course']} - {entry['question']} - {entry['answer'][:10]}").encode()
    return hashlib.sha256(hash_input).hexdigest()[:10]

def add_id_column(data):
    """Add an ID column to each entry in the data."""
    for entry in data:
        entry['id'] = generate_id(entry)
    return data

def read_metadata(metadata_file_path):
    """Read processed metadata from the metadata file."""
    try:
        with open(metadata_file_path, 'r') as file:
            metadata = json.load(file)
    except FileNotFoundError:
        metadata = []
    return metadata

def update_metadata(new_entries, faq_metadata_file):
    """Update the metadata file with new entries."""
    metadata = read_metadata(faq_metadata_file)
    metadata.extend(new_entries)
    with open(faq_metadata_file, 'w') as file:
        json.dump(metadata, file)

def filter_new_entries(data, faq_metadata_file):
    """Filter out already processed entries based on the metadata file."""
    metadata = read_metadata(faq_metadata_file)
    processed_ids = {entry['id'] for entry in metadata}
    new_entries = [entry for entry in data if entry['id'] not in processed_ids]
    return new_entries
