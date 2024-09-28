import pandas as pd
import re

# Function to tokenize and label the message
def label_message_utf8_with_birr(message):
    # Split the message at the first occurrence of '\n'
    if '\n' in message:
        first_line, remaining_message = message.split('\n', 1)
    else:
        first_line, remaining_message = message, ""
    
    labeled_tokens = []
    
    # Tokenize the first line
    first_line_tokens = re.findall(r'\S+', first_line)
    
    # Label the first token as B-PRODUCT and the rest as I-PRODUCT
    if first_line_tokens:
        labeled_tokens.append(f"{first_line_tokens[0]} B-PRODUCT")  # First token as B-PRODUCT
        for token in first_line_tokens[1:]:
            labeled_tokens.append(f"{token} I-PRODUCT")  # Remaining tokens as I-PRODUCT
    
    # Process the remaining message normally
    if remaining_message:
        lines = remaining_message.split('\n')
        for line in lines:
            tokens = re.findall(r'\S+', line)  # Tokenize each line while considering non-ASCII characters
            
            for token in tokens:
                # Check if token is a price (e.g., 500 ETB, $100, or ብር)
                if re.match(r'^\d{10,}$', token):
                    labeled_tokens.append(f"{token} O")  # Label as O for "other" or outside of any entity
                elif re.match(r'^\d+(\.\d{1,2})?$', token) or 'ETB' in token or 'ዋጋ' in token or '$' in token or 'ብር' in token:
                    labeled_tokens.append(f"{token} I-PRICE")
                # Check if token could be a location (e.g., cities or general location names)
                elif any(loc in token for loc in ['Addis Ababa','መገናኛ', '376', 'ሜክሲኮ']):
                    labeled_tokens.append(f"{token} I-LOC")
                # Assume other tokens are part of a product name or general text
                else:
                    labeled_tokens.append(f"{token} O")
    
    return "\n".join(labeled_tokens)

# Load your dataset (replace with the path to your dataset)
df = pd.read_csv('your_dataset.csv')

# Apply the function to the 'cleaned_message' column
df['Labeled_Message'] = df['cleaned_message'].apply(label_message_utf8_with_birr)

# Save the labeled data to a CSV file
df[['cleaned_message', 'Labeled_Message']].to_csv('labeled_messages.csv', index=False)

# Optional: Save the labeled data to a TXT file
with open('labeled_messages.txt', 'w', encoding='utf-8') as file:
    for message in df['Labeled_Message']:
        file.write(message + '\n\n')  # Add a blank line between messages

print("Tokenization and labeling completed. Files saved as 'labeled_messages.csv' and 'labeled_messages.txt'.")
