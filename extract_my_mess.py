import os
import json
from bs4 import BeautifulSoup
from urllib.parse import unquote

def extract_all_messages(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')

    all_messages = []

    for message_elem in soup.find_all('div', class_='_3-95 _a6-g'):
        sender_elem = message_elem.find('div', class_='_2ph_ _a6-h _a6-i')
        content_elem = message_elem.find('div', class_='_2ph_ _a6-p')
        timestamp_elem = message_elem.find('div', class_='_3-94 _a6-o')

        # Check if sender_elem, content_elem, and timestamp_elem are not None before accessing text attribute
        sender = sender_elem.text.strip() if sender_elem else 'Unknown Sender'
        content = content_elem.text.strip() if content_elem else 'No Content'
        timestamp = timestamp_elem.text.strip() if timestamp_elem else 'No Timestamp'

        all_messages.append({
            'sender': sender,
            'content': content,
            'timestamp': timestamp
        })

    return all_messages

def save_messages_to_files(messages, output_folder, subfolder_name):
    # Save messages to JSON file
    json_file_path = os.path.join(output_folder, f'{subfolder_name}_messages.json')
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(messages, json_file, ensure_ascii=False, indent=2)

    # Save messages to text file
    text_file_path = os.path.join(output_folder, f'{subfolder_name}_messages.txt')
    with open(text_file_path, 'w', encoding='utf-8') as text_file:
        for message in messages:
            text_file.write(f"{message['sender']}: {message['content']}\n")

    print(f"All messages from {subfolder_name} saved to {json_file_path} and {text_file_path}")

def combine_json_files(input_folder, output_file):
    combined_messages = []

    # Iterate through files in the input folder
    for file in os.listdir(input_folder):
        # Check if the file is a JSON file
        if file.endswith('_messages.json'):
            file_path = os.path.join(input_folder, file)

            # Load messages from the JSON file
            with open(file_path, 'r', encoding='utf-8') as json_file:
                messages = json.load(json_file)

            # Append messages to the combined list
            combined_messages.extend(messages)

    # Save combined messages to a single JSON file
    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(combined_messages, json_file, ensure_ascii=False, indent=2)

    print(f"Combined messages saved to {output_file}")

def scrape_and_save_all_messages(input_folder, output_folder):
    # Iterate through subfolders in the input folder
    for subfolder_name in os.listdir(input_folder):
        subfolder_path = os.path.join(input_folder, subfolder_name)

        # Check if it's a directory
        if os.path.isdir(subfolder_path):
            # Iterate through files in the subfolder
            for file in os.listdir(subfolder_path):
                # Check if the file is an HTML file named "message_1.html"
                if file == "message_1.html":
                    file_path = os.path.join(subfolder_path, file)

                    # Extract all messages from the HTML file
                    all_messages = extract_all_messages(file_path)

                    # Save messages to files in the output folder
                    save_messages_to_files(all_messages, output_folder, subfolder_name)

# Update the input and output folder paths
input_folder_path = unquote(r'D:/Projects/DA%20My%20Mess/your_activity_across_facebook/messages/inbox')
output_folder_path = unquote(r'D:/Projects/DA%20My%20Mess/my_mess_data')

# Scrape all messages and save them in the specified output folder
scrape_and_save_all_messages(input_folder_path, output_folder_path)

# Combine all JSON files into a single file
combine_json_files(output_folder_path, 'combined_messages.json')
