# Define function to create chunks
def create_chunk(row):
    return '\n'.join([
            f"course:\n{row['course']}\n",
            f"question:\n{row['question']}\n",
            f"answer:\n{row['answer']}\n"
        ])