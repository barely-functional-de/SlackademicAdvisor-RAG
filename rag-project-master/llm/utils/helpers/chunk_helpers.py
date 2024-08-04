# Define function to create chunks
def create_chunk(row):
    if 'Course' in row and 'Section' in row:
        return '\n'.join([
            f"course:\n{row['Course']}\n",
            f"section:\n{row['Section']}\n",
            f"question:\n{row['Question']}\n",
            f"answer:\n{row['Answer']}\n"
        ])
    else:
        return '\n'.join([
            f"question:\n{row['Question']}\n",
            f"answer:\n{row['Answer']}\n"
        ])