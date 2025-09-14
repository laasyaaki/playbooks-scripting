#formats prompts for readability and easy copy and paste for the API

import pandas as pd

# Load spreadsheet
file_path = '/content/MITRE_JSONS.csv'  # Rename after uploading in Colab
df = pd.read_csv(file_path)

# Function to format a single paragraph from a row
def format_paragraph(tech_id, tech_name, postconditions):
    # Clean and split postconditions into a numbered list
    items = [item.strip().split(") ", 1)[-1] for item in postconditions.split(";") if item.strip()]
    numbered_postconds = [f"{i+1}) {pc}" for i, pc in enumerate(items)]
    postcond_text = " ".join(numbered_postconds)

    paragraph = f"""We will provide you with a list of preconditions of the MITRE DEFENSE techniques (attached), where the Precondition of a technique is labelled with a unique ID and description. I will give you a specific technique and its postconditions. Your goal is to look through the list of all preconditions, and return to me a sublist of preconditions that match one of each postcondition. For example, if we provide a postcondition like “system is on”, then you should look through the list of preconditions and find all similar preconditions, which are similar/have the same meaning as the postcondition, such as precondition “system running”. Then return the precondition IDs in a comma separated list. This task will be completed for all of the postconditions of the technique, and will have a separate list for each postcondition. Make sure you only refer to techniques and ID from the spreadsheet (no other outside information is allowed). The spreadsheet is uploaded in this prompt. Ensure that the precondition IDs belong to different techniques.

The technique we will be focusing on is:
ID: {tech_id}
Name: {tech_name}
Postcondition of {tech_id}: {postcond_text}
"""
    return paragraph

# Generate and print formatted paragraphs
for index, row in df.iterrows():
    paragraph = format_paragraph(row['Tech ID'], row['Tech Name'], row['List of PostCond'])
    print(paragraph)
    print("=" * 80)  # separator for readability


#example output:
"""
We will provide you with a list of preconditions of the MITRE DEFENSE techniques (attached), where the Precondition of a technique is labelled with a unique ID and description. I will give you a specific technique and its postconditions. Your goal is to look through the list of all preconditions, and return to me a sublist of preconditions that match one of each postcondition. For example, if we provide a postcondition like “system is on”, then you should look through the list of preconditions and find all similar preconditions, which are similar/have the same meaning as the postcondition, such as precondition “system running”. Then return the precondition IDs in a comma separated list. This task will be completed for all of the postconditions of the technique, and will have a separate list for each postcondition. Make sure you only refer to techniques and ID from the spreadsheet (no other outside information is allowed). The spreadsheet is uploaded in this prompt. Ensure that the precondition IDs belong to different techniques.

The technique we will be focusing on is:
ID: D3-SVCDM
Name: Service Dependency Mapping
Postcondition of D3-SVCDM: 1) Dependencies between services have been documented and linked. 2) A model of service dependencies is now available to the organization.

================================================================================
We will provide you with a list of preconditions of the MITRE DEFENSE techniques (attached), where the Precondition of a technique is labelled with a unique ID and description. I will give you a specific technique and its postconditions. Your goal is to look through the list of all preconditions, and return to me a sublist of preconditions that match one of each postcondition. For example, if we provide a postcondition like “system is on”, then you should look through the list of preconditions and find all similar preconditions, which are similar/have the same meaning as the postcondition, such as precondition “system running”. Then return the precondition IDs in a comma separated list. This task will be completed for all of the postconditions of the technique, and will have a separate list for each postcondition. Make sure you only refer to techniques and ID from the spreadsheet (no other outside information is allowed). The spreadsheet is uploaded in this prompt. Ensure that the precondition IDs belong to different techniques.

The technique we will be focusing on is:
ID: D3-SYSDM
Name: System Dependency Mapping
Postcondition of D3-SYSDM: 1) System-level dependencies between components have been mapped. 2) A system dependency model is now available to support organizational analysis and decision-making.

================================================================================
We will provide you with a list of preconditions of the MITRE DEFENSE techniques (attached), where the Precondition of a technique is labelled with a unique ID and description. I will give you a specific technique and its postconditions. Your goal is to look through the list of all preconditions, and return to me a sublist of preconditions that match one of each postcondition. For example, if we provide a postcondition like “system is on”, then you should look through the list of preconditions and find all similar preconditions, which are similar/have the same meaning as the postcondition, such as precondition “system running”. Then return the precondition IDs in a comma separated list. This task will be completed for all of the postconditions of the technique, and will have a separate list for each postcondition. Make sure you only refer to techniques and ID from the spreadsheet (no other outside information is allowed). The spreadsheet is uploaded in this prompt. Ensure that the precondition IDs belong to different techniques.

The technique we will be focusing on is:
ID: D3-SYSVA
Name: System Vulnerability Assessment
Postcondition of D3-SYSVA: 1) System-wide vulnerabilities and risks have been assessed and documented. 2) A system-level vulnerability profile is now available for mitigation planning.

================================================================================
"""
