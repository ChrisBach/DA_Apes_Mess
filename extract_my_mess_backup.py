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

# Update the file path with unquote
file_path = unquote(r'D:/Projects/DA%20My%20Mess/your_activity_across_facebook/messages/inbox/krakowapes_5576407995811527/message_1.html')

# Extract all messages
all_messages = extract_all_messages(file_path)

# Save messages to JSON file
json_file_path = 'apes_messages.json'
with open(json_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(all_messages, json_file, ensure_ascii=False, indent=2)

# Save messages to text file
text_file_path = 'apes_messages.txt'
with open(text_file_path, 'w', encoding='utf-8') as text_file:
    for message in all_messages:
        text_file.write(f"{message['sender']}: {message['content']}\n")

print(f"All messages saved to {json_file_path} and {text_file_path}")
