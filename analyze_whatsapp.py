import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import glob

# Function to process the exported WhatsApp file
def process_whatsapp_export(file_paths, start_date_str, end_date_str):
    all_data = []

    for file_path in file_paths:
        print(f"Processing file: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        data = []
        current_message = ''
        current_sender = None
        current_date_time = None

        for line in lines:
            line = line.strip()
            if not line:
                continue

            if ' - ' in line:
                # Save the previous message if it exists
                if current_message and current_sender and current_date_time:
                    data.append({'date_time': current_date_time, 'sender': current_sender, 'message': current_message})
                    current_message = ''

                try:
                    # Extract date and time, and message part
                    date_time_str, message_part = line.split(' - ', 1)
                    try:
                        date_time = datetime.strptime(date_time_str, '%d/%m/%Y %H:%M')
                    except ValueError:
                        print(f"Skipping line: {line}. Invalid date and time format.")
                        continue
                
                    # Extract sender and message content
                    if ': ' in message_part:
                        current_sender, current_message = message_part.split(': ', 1)
                    else:
                        current_sender = message_part
                        current_message = ''
                    
                    current_date_time = date_time
                except Exception as e:
                    print(f"Error processing line: {line}. Error: {e}")
                    continue
            else:
                # Handle lines that are part of a multi-line message
                if current_message:
                    current_message += ' ' + line
                else:
                    if not line.startswith('📅'):
                        print(f"Line does not match expected format and is not part of a multi-line message: {line}")

        # Add the last message after the loop
        if current_message and current_sender and current_date_time:
            data.append({'date_time': current_date_time, 'sender': current_sender, 'message': current_message})

        # Append to all_data
        all_data.extend(data)

    # Create DataFrame
    df = pd.DataFrame(all_data)

    # Convert start and end date strings to datetime objects
    start_date = datetime.strptime(start_date_str, '%d/%m/%Y')
    end_date = datetime.strptime(end_date_str, '%d/%m/%Y')

    # Filter DataFrame by the specified date range
    df = df[(df['date_time'] >= start_date) & (df['date_time'] <= end_date)]

    # Define a list of senders to exclude
    excluded_senders = ['sender one, sender two']

    # Filter out excluded senders
    df = df[~df['sender'].isin(excluded_senders)]

    # List all unique senders
    unique_senders_list = df['sender'].unique()
    print("Unique senders in the dataset:")
    for sender in unique_senders_list:
        print(sender)

    # Check if 'sender' column exists
    if 'sender' not in df.columns:
        print("Column 'sender' not found in the DataFrame. Please check the input file format.")
        return
    
    # Count messages
    total_messages = len(df)
    
    # Count unique participants
    unique_senders = df['sender'].nunique()
    
    # Summary
    print(f"Total messages from {start_date_str} to {end_date_str}: {total_messages}")
    print(f"Number of unique participants from {start_date_str} to {end_date_str}: {unique_senders}")

    # # Visualization (optional)
    # df['date'] = df['date_time'].dt.date
    # daily_messages = df.groupby('date').size()

    # plt.figure(figsize=(10, 6))
    # daily_messages.plot(kind='bar')
    # plt.xlabel('Date')
    # plt.ylabel('Number of Messages')
    # plt.title(f'Daily Messages from {start_date_str} to {end_date_str}')
    # plt.xticks(rotation=45)
    # plt.tight_layout()
    # plt.show()

# Path to the exported files
file_paths = glob.glob('data/name.txt')  # Adjust the pattern to match your files

# Specify the start and end date for the analysis
start_date_str = '26/08/2024'  # Example start date
end_date_str = '01/09/2024'    # Example end date

process_whatsapp_export(file_paths, start_date_str, end_date_str)
