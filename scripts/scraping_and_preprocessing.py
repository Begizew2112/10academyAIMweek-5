import asyncio
import os
import re
import pandas as pd
from telethon import TelegramClient
from telethon.tl.types import PeerChannel

# Step 1: Set up Telegram Client
api_id = '29354999'  
api_hash = 'edc4bfe62ee519a3259bbdb92ba66aae'  # Replace with your own API Hash
username = '@kuluamekeru' 

client = TelegramClient(username, api_id, api_hash)

async def scrape_messages(channel_username):
    messages = []
    async with client:
        channel = await client.get_entity(channel_username)
        async for message in client.iter_messages(channel, limit=10000):
            messages.append({
                'date': message.date,
                'message': message.message,
            })
    return messages

# Step 2: Run the scraping function
async def main():
    channel_username = 'MerttEka'
    messages = await scrape_messages(channel_username)
    
    # Create DataFrame
    df = pd.DataFrame(messages)
    
    # Step 3: Save raw messages to CSV
    raw_csv_path = r'C:\Users\Yibabe\Desktop\10academyAIMweek-5\notebook\telegram_channel_messages.csv'
    df.to_csv(raw_csv_path, index=False)
    print(f"Raw messages saved to {raw_csv_path}")

# Execute scraping
asyncio.run(main())

# Step 4: Load and preprocess the data
df = pd.read_csv(raw_csv_path)

# Step 5: Convert 'date' Column to Datetime
df['date'] = pd.to_datetime(df['date'])

# Step 6: Clean the messages
def remove_emojis(text):
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F700-\U0001F77F"  # alchemical symbols
        u"\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
        u"\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
        u"\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
        u"\U0001FA00-\U0001FA6F"  # Chess Symbols
        u"\U00002702-\U000027B0"  # Dingbats
        "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)

def clean_text(text):
    # Remove emojis
    text = remove_emojis(text)  
    # Allow letters, numbers, spaces, and the '/' character
    text = re.sub(r'[^a-zA-Z0-9\s/]', '', text)  
    # Replace multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text)  
    return text.strip()  # Remove leading and trailing whitespace

# Step 7: Apply cleaning function to messages
df['cleaned_message'] = df['message'].apply(clean_text)

# Step 8: Save cleaned DataFrame to new location
cleaned_csv_path = r'C:\Users\Yibabe\Desktop\10academyAIMweek-5\data\telegram_channel_messages.csv'
os.makedirs(os.path.dirname(cleaned_csv_path), exist_ok=True)
df.to_csv(cleaned_csv_path, index=False)

print(f"Cleaned messages saved to {cleaned_csv_path}")
