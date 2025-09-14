import pandas as pd

# Load csvs
preconditions_df = pd.read_csv('preconditions.csv', header=None)
lists_df = pd.read_csv('lists.csv', header=None)

valid_preconditions = set(preconditions_df[0].str.strip())

# Check each precondition list against the original generated preconditions
for row_index, item_list in enumerate(lists_df[0]):
    items = [item.strip() for item in item_list.split(',')]
    if not all(item in valid_preconditions for item in items):
        print(f"Row {row_index} triggers False")
        for item in items:
            if item not in valid_preconditions:
                print(f"Item '{item}' is not in valid_preconditions")
        print(False)
        exit()

# Return true if all preconditions are valid
print(True)


#script checks if all of the matched postconditions are in the original master postcondition list
# hallucination checking step
