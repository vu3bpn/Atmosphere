import os
import re
import subprocess

src_dir = '/mnt/nvme1n1/Bipin/Scripts/Atmosphere'
markdown_dir = os.path.join(src_dir, 'src')
index_file = os.path.join(markdown_dir, 'index.md')
output_dir = os.path.join(src_dir, 'output')
os.makedirs(output_dir, exist_ok=True)

def clean_filename(name):
    # Remove special characters, replace spaces with underscores, lowercase
    name = re.sub(r'[^\w\s-]', '', name)
    name = name.strip().replace(' ', '_')
    return name.lower() + '.md'

def clean_html_filename(name):
    return clean_filename(name).replace('.md', '.html')

def extract_sections(index_path):
    sections = []
    with open(index_path, 'r') as f:
        for line in f:
            line = line.strip()
            # Match top-level and sub-level headings and list items
            if line.startswith('#'):
                heading = line.lstrip('#').strip()
                if heading.lower() != 'index':
                    sections.append(heading)
            elif line.startswith('-'):
                # If line contains a markdown link, extract the text inside [ ]
                match = re.search(r'\[([^\]]+)\]', line)
                if match:
                    item = match.group(1).strip()
                else:
                    item = line.lstrip('-').strip()
                sections.append(item)
    return sections

def create_md_files(sections, out_dir):
    for section in sections:
        filename = clean_filename(section)
        filepath = os.path.join(out_dir, filename)
        heading_level = 1 if section.isupper() or section.istitle() else 2
        with open(filepath, 'w') as f:
            f.write(f"{'#' * heading_level} {section}\n\n")

def convert_md_to_html_pandoc(md_folder, html_folder):
    os.makedirs(html_folder, exist_ok=True)
    for fname in os.listdir(md_folder):
        if fname.endswith('.md'):
            md_path = os.path.join(md_folder, fname)
            html_fname = fname.replace('.md', '.html')
            html_path = os.path.join(html_folder, html_fname)
            subprocess.run(['pandoc', md_path, '-o', html_path])

def update_index_with_links(index_path, sections, html_folder):
    new_lines = []
    with open(index_path, 'r') as f:
        for line in f:
            stripped = line.strip()
            if stripped.startswith('-'):
                # If already a markdown link, skip editing
                if re.search(r'\[.*\]\(.*\)', stripped):
                    new_lines.append(line)
                else:
                    item = stripped.lstrip('-').strip()
                    html_file = clean_html_filename(item)
                    link = f"[{item}]({html_file})"
                    new_lines.append(f"- {link}\n")
            else:
                new_lines.append(line)
    # Write updated index.md
    with open(index_path, 'w') as f:
        f.writelines(new_lines)

if __name__ == '__main__':
    sections = extract_sections(index_file)
    create_md_files(sections, markdown_dir)
<<<<<<< HEAD
    update_index_with_links(index_file, sections, output_dir)
    convert_md_to_html_pandoc(markdown_dir, output_dir)
    
=======
    convert_md_to_html_pandoc(markdown_dir, output_dir)
    update_index_with_links(index_file, sections, output_dir)
>>>>>>> 7f44ad1... initial commit
    print(f"Created {len(sections)} markdown files in {src_dir} and HTML files in {output_dir}, and updated index.md with hyperlinks.")