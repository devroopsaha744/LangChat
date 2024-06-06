import os
import nbformat

# Directory containing the .ipynb files
input_directory = r'C:\Users\devro\OneDrive\Desktop\LangChat\data'
output_directory = r'C:\Users\devro\OneDrive\Desktop\LangChat\txt_data'

# Create the output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

# Iterate over all files in the input directory
for filename in os.listdir(input_directory):
    if filename.endswith('.ipynb'):
        # Read the notebook
        with open(os.path.join(input_directory, filename), 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=4)
        
        # Create a corresponding markdown file
        md_filename = os.path.splitext(filename)[0] + '.md'
        with open(os.path.join(output_directory, md_filename), 'w', encoding='utf-8') as f:
            # Iterate over all cells in the notebook
            for cell in nb.cells:
                if cell.cell_type == 'code':
                    f.write('```python\n')
                    f.write(cell.source + '\n')
                    f.write('```\n\n')
                elif cell.cell_type == 'markdown':
                    f.write(cell.source + '\n\n')


