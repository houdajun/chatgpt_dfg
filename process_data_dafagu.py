import os
import subprocess
import re
import pandas as pd
from opencc import OpenCC

# Initialize the converter
cc = OpenCC('t2s')

# List of words to be excluded
excluded_words = ['打印',  'the end', '陈月卿','各位观众','陈小姐','节目最后','您好','THE END','一集']

# Remove the output file if it exists
if os.path.exists('/media/dajun/WD3T/sutra/data/output.txt'):
    os.remove('/media/dajun/WD3T/sutra/data/output.txt')

extract_to = '/media/dajun/WD3T/sutra/data'

# Open the output file in append mode
i=0
with open('/media/dajun/WD3T/sutra/data/output.txt', 'a') as f:
    # Walk through the extracted files and process .doc files
    for root, dirs, files in os.walk(extract_to):
        for file in files:
            if file.endswith('.doc'):
                i=i+1
                doc_path = os.path.join(root, file)
                print(f"{i},{doc_path}")

                # Call antiword on the .doc file
                text = subprocess.run(['antiword', doc_path], capture_output=True, text=True).stdout

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
df = pd.read_csv('/media/dajun/WD3T/sutra/data/output.txt', sep='\t', header=None)

# Write the DataFrame to a CSV file
df.to_csv('/media/dajun/WD3T/sutra/data/output.csv', index=False)