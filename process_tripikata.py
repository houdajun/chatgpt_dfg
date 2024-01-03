import os
import subprocess
import re
import pandas as pd
from opencc import OpenCC

# Initialize the converter
cc = OpenCC('t2s')

# List of words to be excluded
excluded_words = ['#', '打印', '大法鼓', 'the end', '陈月卿','各位观众','陈小姐','节目最后','您好','THE END','一集']

rootFolder = '/media/dajun/WD3T/sutra/data/cbeta-text'
# Remove the output file if it exists
if os.path.exists(f'{rootFolder}/tripikata.txt'):
    os.remove(f'{rootFolder}/tripikata.txt')
if os.path.exists(f'{rootFolder}/tripikata.csv'):
    os.remove(f'{rootFolder}/tripikata.csv')

extract_to = rootFolder

# Open the output file in append mode
i=0
with open(f'{rootFolder}/tripikata.txt', 'a') as f:
    # Walk through the extracted files and process .doc files
    for root, dirs, files in os.walk(extract_to):
        for file in files:
            if file.endswith('.txt'):
                i=i+1
                doc_path = os.path.join(root, file)
                print(f"{i},{doc_path}")

                # Read the .txt file
                with open(doc_path, 'r') as txt_file:
                    text = txt_file.read()

                # Convert traditional Chinese to simplified Chinese
                text = cc.convert(text)

                # Remove all '%' characters
                text = text.replace('%', '')
                
                # Remove all standalone numbers
                text = re.sub(r'\b\d+\b', '', text)

                # Add a comma at the end of each line, remove empty lines or lines with only a comma, and lines containing any of the excluded words
                lines = text.splitlines()
                lines = [line for line in lines if line.strip() and line.strip() != ',' and not any(word in line for word in excluded_words)]
                text = '\n'.join(lines)

                # Write the text to the output file
                f.write(text + '\n')

# Read the text file
df = pd.read_csv(f'{rootFolder}/tripikata.txt', sep='\t', header=None)

# Write the DataFrame to a CSV file
df.to_csv(f'{rootFolder}/tripikata.csv', index=False)



# Load the large CSV file
df = pd.read_csv(f'{rootFolder}/tripikata.csv')

# Calculate the halfway point
half = len(df) // 2

# Write the first half of the DataFrame to the first output file
df.iloc[:half].to_csv(f'{rootFolder}/tripikata_1.csv', index=False)

# Write the second half of the DataFrame to the second output file
df.iloc[half:].to_csv(f'{rootFolder}/tripikata_2.csv', index=False)