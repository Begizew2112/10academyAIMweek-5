import pandas as pd
import re

# Load the CSV file into a DataFrame
df1 = pd.read_csv('path_to_your_file.csv')

# Define the tokenization function
def tokenize_message(message):
    if not isinstance(message, str) or message.strip() == "":
        return []
    
    tokenized_message = []
    if '\n' in message:
        first_line, remaining_message = message.split('\n', 1)
    else:
        first_line, remaining_message = message, ""

    first_line_tokens = re.finditer(r'\S+', first_line)
    
    for match in first_line_tokens:
        token = match.group()
        start_pos = match.start()
        end_pos = match.end()
        tokenized_message.append((token, start_pos, end_pos))

    if remaining_message:
        lines = remaining_message.split('\n')
        for line in lines:
            tokens = re.finditer(r'\S+', line)
            for match in tokens:
                token = match.group()
                start_pos = match.start()
                end_pos = match.end()
                tokenized_message.append((token, start_pos, end_pos))
    
    return tokenized_message

# Define the labeling function
def label_tokens(tokenized_message):
    labeled_tokens_with_positions = []
    first_token = True
    for token, start_pos, end_pos in tokenized_message:
        if first_token:
            label = "B-PRODUCT"
            first_token = False
        elif re.match(r'^\d{10,}$', token):
            label = "O"
        elif re.match(r'^\d+(\.\d{1,2})?$', token) or any(currency in token for currency in ['ETB', 'ዋጋ', '$', 'ብር']):
            label = "I-PRICE"
        elif any(loc in token for loc in ['Addis Ababa', 'ዘፍመሽ', 'መገናኛ', 'ግራንድ', '376', 'ሜክሲኮ']):
            label = "I-LOC"
        else:
            label = "O"
        labeled_tokens_with_positions.append(f"{token:<20} {start_pos:<10} {label}")
    return "\n".join(labeled_tokens_with_positions)

# Apply the tokenization and labeling functions
df1['tokenized_message'] = df1['cleaned_message'].apply(tokenize_message)
df1['labeled_message'] = df1['tokenized_message'].apply(label_tokens)

# Save the result to a new CSV file (optional)
df1.to_csv('tokenized_labeled_messages.csv', index=False)

# View the results
print(df1[['cleaned_message', 'tokenized_message', 'labeled_message']].head())
