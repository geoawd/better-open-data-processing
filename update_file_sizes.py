'''
This will update the files sizes of the json payload. Useful for when the data is converted from lzw to deflate.
Matches the download url and updates the filesize.
'''
import json
import re
import sys

def update_file_sizes(json_file_path, sizes_file_path, output_file_path):
    # Read the JSON data
    with open(json_file_path, 'r') as f:
        try:
            json_data = json.load(f)
        except json.JSONDecodeError:
            # Try to parse JSON with a workaround for the provided format
            with open(json_file_path, 'r') as f2:
                content = f2.read()
                # Fix the missing array brackets and commas between objects
                content = '[' + content.replace('}\n {', '}, {') + ']'
                json_data = json.loads(content)

    # Read the file sizes
    file_sizes = {}
    with open(sizes_file_path, 'r') as f:
        for line in f:
            match = re.match(r'\s*(\d+),\s*\'([^\']+)\'', line)
            if match:
                size, path = match.groups()
                file_sizes[path] = size

    # Update file sizes in JSON data
    for item in json_data:
        download_url = item.get('downloadUrl', '')
        if download_url in file_sizes:
            item['fileSize'] = file_sizes[download_url]

    # Write the updated JSON data to the output file
    with open(output_file_path, 'w') as f:
        json.dump(json_data, f, indent=2)

    print(f"Updated JSON data written to {output_file_path}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python update_file_sizes.py <json_file> <sizes_file> <output_file>")
        sys.exit(1)
    
    json_file = sys.argv[1]
    sizes_file = sys.argv[2]
    output_file = sys.argv[3]
    
    update_file_sizes(json_file, sizes_file, output_file)
    
