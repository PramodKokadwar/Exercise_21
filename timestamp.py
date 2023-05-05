import json
import csv
from datetime import datetime

start_time = datetime.now()

# Load input.json
with open('input.json') as json_file:
    data = json.load(json_file)

# Find earliest frame date and time
earliest_date = datetime.now().date()
earliest_time = datetime.now().time()
for frame in data:
    frame_date = datetime.strptime(frame["@timestamp"], '%Y-%m-%d %H:%M:%S.%f').date()
    frame_time = datetime.strptime(frame["@timestamp"], '%Y-%m-%d %H:%M:%S.%f').time()
    if frame_date < earliest_date:
        earliest_date = frame_date
        earliest_time = frame_time
    elif frame_date == earliest_date and frame_time < earliest_time:
        earliest_time = frame_time

# Find latest frame time
latest_time = datetime.now().time()
for frame in data:
    frame_date = datetime.strptime(frame["@timestamp"], '%Y-%m-%d %H:%M:%S.%f').date()
    frame_time = datetime.strptime(frame["@timestamp"], '%Y-%m-%d %H:%M:%S.%f').time()
    if frame_date == earliest_date and frame_time > latest_time:
        latest_time = frame_time

# Extract data from frames and write to csv
output_file_name = "{}_{}_{:%H%M}_{:%H%M}.csv".format(
    data[0]["@message"]["message"].split("/")[5],
    earliest_date.strftime("%Y%m%d"),
    earliest_time,
    latest_time
)
with open(output_file_name, mode='w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["machineId", "contributionId", "startDate", "endDate"])
    for frame in data:
        message_parts = frame["@message"]["message"].split("/")
        if len(message_parts) >= 10:
            writer.writerow([
                message_parts[5],
                message_parts[9],
                message_parts[7],
                message_parts[8]
            ])


# Print execution time
print("Execution time:", datetime.now() - start_time)