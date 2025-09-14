import json

def extract_d3fend_info(json_file, d3fend_id):
    with open(json_file, 'r', encoding='utf-8') as file:
        try:
            data = json.load(file)  # Load the JSON file
        except json.JSONDecodeError:
            print("Error: Invalid JSON format.")
            return None

    # Ensure the JSON has "@graph" key
    if "@graph" not in data:
        print("Error: '@graph' key not found in JSON.")
        return None

    for entry in data["@graph"]:
        if isinstance(entry, dict) and entry.get("d3f:d3fend-id") == d3fend_id:
            extracted_info = {
                "d3f:d3fend-id": entry.get("d3f:d3fend-id", "N/A"),
                "d3f:definition": entry.get("d3f:definition", "N/A"),
                "d3f:synonym": entry.get("d3f:synonym", "N/A"),
                "d3f:kb-article": entry.get("d3f:kb-article", "N/A"),
                "@id": entry.get("@id", "N/A")
            }

            synonyms = extracted_info['d3f:synonym']
            # syns_to_print = ""
            # for syn in synonyms:
            #     syns_to_print += syn + ", "

            return f"""
{extracted_info['@id'].split(':')[-1]} - {extracted_info['d3f:d3fend-id']}
I plan to develop a knowledge graph of defense actions defined in MITRE D3FEND, which will map the logical relationships between these actions based on their preconditions and postconditions. If a precondition is not met, the corresponding action cannot be successfully executed. The precondition of an action consists of a set of conditions that must be satisfied to execute the defensive action. These conditions can be defined by two main factors: 1.The required input for executing the action, which could be system resources, system status, or other variables. For example, obtaining the IP address is necessary for the “host isolation” action, or acquiring the file hash is required for the “file inspection” action. 2.The required configurations for executing the action, such as firewall access control rules permitting traffic to a specific host to enable the “host inspection” action. Another example is the necessity for two-factor authentication (2FA) to be enabled in order to perform the “enforce authentication” action. The postcondition consists of a set of logical conditions that represent at least two factors: (1) the expected changes in system state, or (2) configurations resulting from executing the action. These postconditions can also serve as preconditions for other actions. Now can you please identify the precondition and postconditions of the following defense action, state which factor it belongs to, and write them in logical predicates that I can use in logic programming.
Action Definition: {extracted_info['d3f:definition']}
Synonyms: {synonyms}
{extracted_info['d3f:kb-article']}\n
                   """

    return "D3FEND ID not found in the JSON file."

# Example
json_file = "/content/d3fend.json"  
d3fend_id = "D3-FCDC" 
result = extract_d3fend_info(json_file, d3fend_id)

if result:
    print(result)
