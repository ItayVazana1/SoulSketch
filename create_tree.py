import os

def generate_folder_tree(start_path='.', output_file='Seg_Service_folder_tree.txt'):
    """
    Generates a folder and file tree starting from 'start_path'
    and writes it into 'output_file' in a readable format.
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        for root, dirs, files in os.walk(start_path):
            level = root.replace(start_path, '').count(os.sep)
            indent = '    ' * level
            f.write(f'{indent}📁 {os.path.basename(root)}/\n')
            sub_indent = '    ' * (level + 1)
            for file in files:
                f.write(f'{sub_indent}📄 {file}\n')

if __name__ == "__main__":
    generate_folder_tree()
    print("✅ Folder tree generated successfully into 'Seg_Service_folder_tree.txt'")
