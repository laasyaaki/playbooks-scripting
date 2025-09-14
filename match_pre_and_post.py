import csv

# Load postcondition descriptions in dictionary
postcondition_descs = {}
with open('descs.csv', newline='', encoding='utf-8') as desc_file:
    reader = csv.DictReader(desc_file)
    for row in reader:
        post_id = row['postcondition ID'].strip()
        desc = row['desc'].strip()
        postcondition_descs[post_id] = desc

# Expand each postcondition into own row with descriptions
output_rows = []
with open('lists.csv', newline='', encoding='utf-8') as in_file:
    reader = csv.DictReader(in_file)
    for row in reader:
        pre_id = row['ID'].strip()
        pre_desc = row['precondition'].strip()
        post_ids = [pid.strip() for pid in row['Matching Postconditions from GPT-4o'].split(',') if pid.strip()]

        for post_id in post_ids:
            output_rows.append({
                'precondition ID': pre_id,
                'precondition desc': pre_desc,
                'postcondition ID': post_id,
                'postcondition desc': postcondition_descs.get(post_id, '')
            })

# Write expanded output final
with open('final_output.csv', 'w', newline='', encoding='utf-8') as out_file:
    fieldnames = ['precondition ID', 'precondition desc', 'postcondition ID', 'postcondition desc']
    writer = csv.DictWriter(out_file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(output_rows)

print("Output written to 'final_output.csv'")
