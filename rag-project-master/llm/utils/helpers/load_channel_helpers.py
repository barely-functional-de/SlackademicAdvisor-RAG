import json
import glob
import os
import hashlib
import pandas as pd

# Function to read and parse JSON files
def read_json_files(file_paths):
    all_data = []
    for file_path in file_paths:
        with open(file_path, 'r') as f:
            data = json.load(f)
            all_data.extend(data)
    return all_data

def process_messages_bkp(data):
    questions = []
    question_askers = []
    question_timestamps = []
    answers = []
    answered_by = []
    answer_timestamps = []
    ids = []

    # Dictionary to map thread_ts to the original question message
    thread_dict = {}
    message_dict = {msg["ts"]: msg for msg in data}

    for message in data:
        if "subtype" not in message and message.get("text"):
            # Check if the message is a question or an answer
            if "thread_ts" not in message or message["ts"] == message["thread_ts"]:
                # This is a question
                question_id = generate_alphanumeric_id(message["ts"])
                if question_id not in ids:
                    questions.append(message["text"])
                    question_askers.append(message["user_profile"]["real_name"])
                    question_timestamps.append(message["ts"])
                    ids.append(question_id)
                    
                    # Map the thread_ts to the question's timestamp
                    thread_dict[message["ts"]] = {
                        "question_text": message["text"],
                        "question_user": message["user_profile"]["real_name"],
                        "question_ts": message["ts"],
                        "question_id": question_id
                    }
    
    # Find answers to the questions
    for message in data:
        if "subtype" not in message and message.get("text"):
            # Only process messages with a valid thread_ts that is in thread_dict
            thread_ts = message.get("thread_ts")
            if thread_ts and thread_ts in thread_dict:
                question_info = thread_dict[thread_ts]
                if message["user_profile"]["real_name"] != question_info["question_user"]:
                    answer, answer_by, answer_ts = find_answer(message, message_dict)
                    answers.append(answer)
                    answered_by.append(answer_by)
                    answer_timestamps.append(answer_ts)

    return ids, questions, question_askers, question_timestamps, answers, answered_by, answer_timestamps

def find_answer_bkp(message, message_dict):
    # Check for replies
    if "replies" in message:
        # First, look for replies by Alexey Grigorev
        for reply in message["replies"]:
            reply_message = message_dict.get(reply["ts"])
            if reply_message:
                if reply_message["user_profile"]["real_name"] == "Alexey Grigorev":
                    return reply_message["text"], reply_message["user_profile"]["real_name"], reply_message["ts"]
        
        # If no reply from Alexey Grigorev, take the first reply
        if message["replies"]:
            first_reply = message_dict.get(message["replies"][0]["ts"])
            if first_reply:
                return first_reply["text"], first_reply["user_profile"]["real_name"], first_reply["ts"]
    
    # If there are no replies or no relevant replies, return None
    return None, None, None


# Function to process messages and extract questions
def process_messages(data):
    questions = []
    question_askers = []
    question_timestamps = []
    answers = []
    answered_by = []
    answer_timestamps = []
    ids = []

    message_dict = {msg["ts"]: msg for msg in data}

    for message in data:
        if "subtype" not in message and message.get("text"):
            if "thread_ts" not in message or message["ts"] == message["thread_ts"]:
                question_id = generate_alphanumeric_id(message["ts"])
                if question_id not in ids:
                    questions.append(message["text"])
                    question_askers.append(message["user_profile"]["real_name"])
                    question_timestamps.append(message["ts"])
                    ids.append(question_id)

                    # Look for answers to the question in replies
                    answer, answer_by, answer_ts = find_answer(message, message_dict)
                    answers.append(answer)
                    answered_by.append(answer_by)
                    answer_timestamps.append(answer_ts)

    return ids, questions, question_askers, question_timestamps, answers, answered_by, answer_timestamps

# Function to find an answer to a question
def find_answer(message, message_dict):
    if "replies" in message:
        for reply in message["replies"]:
            reply_message = message_dict.get(reply["ts"])
            if reply_message:
                if reply_message["user_profile"]["real_name"] == "Alexey Grigorev":
                    return reply_message["text"], reply_message["user_profile"]["real_name"], reply_message["ts"]
        # If no reply from Alexey Grigorev, take the first reply
        first_reply = message_dict.get(message["replies"][0]["ts"])
        if first_reply:
            return first_reply["text"], first_reply["user_profile"]["real_name"], first_reply["ts"]
    return None, None, None

# Function to generate alphanumeric ID (dummy implementation for illustration)
def generate_alphanumeric_id(timestamp):
    """Generate a unique alphanumeric ID from the timestamp."""
    # Convert the timestamp to a string
    timestamp_str = str(timestamp)
    # Create a hash of the timestamp
    hash_object = hashlib.md5(timestamp_str.encode())
    # Convert the hash to a hexadecimal string and use the first 8 characters as the ID
    return hash_object.hexdigest()[:10]

# Function to create a DataFrame from the extracted data
def create_dataframe(ids, questions, question_askers, question_timestamps, answers, answered_by, answer_timestamps):
    df = pd.DataFrame({
        "id": ids,
        "question": questions,
        "answer": answers,
        "question_asked_by": question_askers,
        "answered_by": answered_by,
        "question_timestamp": question_timestamps,
        "answer_timestamp": answer_timestamps
    })
    return df

# Function to load existing metadata
def load_existing_metadata(metadata_file):
    if os.path.exists(metadata_file):
        with open(metadata_file, 'r') as f:
            return json.load(f)
    return []

# Function to update metadata
def update_metadata(processed_files, metadata_file):
    with open(metadata_file, 'w') as f:
        json.dump(processed_files, f)

# Function to scan for new files
def scan_for_new_files(data_path, processed_files):
    all_files = glob.glob(data_path)
    new_files = [file for file in all_files if file not in processed_files]
    return new_files
