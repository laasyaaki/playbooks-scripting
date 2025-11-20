"""
script to turn the soundess and completeness results evaluation from my csv format to a json file


[
    { 
        "technique_id": "D3-XXX", //should be the same as technique_id column in the csv 
        "technique_name": "" //should correspond to the same column name in the csv, 
        "technique_desc": "" //should have the technique def and article (from mitre)
        "sound_preconditions": [ 
            { 
                "precondition_id": "D3-XXX-pre-01", //the ids should be sequential
                "precondition_desc": "", //should correspond to the 'condition' field in the list 
                "precondition_evidence": "", //should correspond to the 'evidence' field in the list - what evidence in the technique description made LLM pick this condition
                "precondition_rationale": "", //should correspond to the 'rationale' field in the list - why did the LLM say this condition is sound
            }, 
        ], 
        "sound_postconditions": [ 
            { 
                "poscondition_id": "D3-XXX-post-01", //the ids should be sequential, just number them and the D3-XXX should be the technique_id 
                "postcondition_desc": "", //should correspond to the 'condition' field in the list 
                "postcondition_evidence": "", //should correspond to the 'evidence' field in the list 
                "postcondition_rationale": "", //should correspond to the 'rationale' field in the list 
            }, 
        ]
        "preconditions_complete": "", //should be "yes" or "no", should correspond to the 'preconditions_complete' col 
        "preconditions_completeness_rationale": "", //should correspond to what's in 'preconditions_explanation' column 
        "postconditions_complete": "", //should be "yes" or "no", should correspond to the 'postconditions_complete' col 
        "postconditions_completeness_rationale": "", //should correspond to what's in 'postconditions_explanation' column] - why are the condition complete/incomplete
    }, 
]

"""

import csv
import json
import sys
from typing import List, Dict, Any


def parse_list_field(cell: str) -> List[Dict[str, Any]]:
    if not cell or not cell.strip():
        return []
    try:
        data = json.loads(cell)
        if isinstance(data, list):
            return data
        if isinstance(data, dict):
            return [data]
        return []
    except json.JSONDecodeError:
        return []


def load_d3fend_definitions(json_path: str) -> Dict[str, str]:
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    lookup: Dict[str, str] = {}

    def walk(obj: Any):
        if isinstance(obj, dict):
            d3fid = obj.get("d3f:d3fend-id")
            definition = obj.get("d3f:definition")
            kb_article = obj.get("d3f:kb-article")

            if d3fid:
                combined = ""

                if isinstance(definition, str):
                    combined += definition.strip()

                if isinstance(kb_article, str):
                    if combined:
                        combined += "\n\n" + kb_article.strip()
                    else:
                        combined = kb_article.strip()

                if combined:
                    lookup[d3fid] = combined

            for v in obj.values():
                walk(v)

        elif isinstance(obj, list):
            for item in obj:
                walk(item)

    walk(data)
    return lookup


def convert_csv_to_json(input_csv: str, output_json: str, d3fend_json: str) -> None:
    d3fend_lookup = load_d3fend_definitions(d3fend_json)
    results = []

    with open(input_csv, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            technique_id = row.get("technique_id", "").strip()
            technique_name = row.get("technique_name", "").strip()

            technique_desc = d3fend_lookup.get(technique_id, "")

            raw_sound_preconds = parse_list_field(row.get("sound_preconditions", ""))
            raw_sound_postconds = parse_list_field(row.get("sound_postconditions", ""))

            sound_preconditions = []
            for i, item in enumerate(raw_sound_preconds, start=1):
                sound_preconditions.append({
                    "precondition_id": f"{technique_id}-pre-{i:02d}",
                    "precondition_desc": item.get("condition", ""),
                    "precondition_evidence": item.get("evidence", ""),
                    "precondition_rationale": item.get("rationale", ""),
                })

            sound_postconditions = []
            for i, item in enumerate(raw_sound_postconds, start=1):
                sound_postconditions.append({
                    "poscondition_id": f"{technique_id}-post-{i:02d}",
                    "postcondition_desc": item.get("condition", ""),
                    "postcondition_evidence": item.get("evidence", ""),
                    "postcondition_rationale": item.get("rationale", ""),
                })

            technique_obj = {
                "technique_id": technique_id,
                "technique_name": technique_name,
                "technique_desc": technique_desc,
                "sound_preconditions": sound_preconditions,
                "sound_postconditions": sound_postconditions,
                "preconditions_complete": row.get("preconditions_complete", "").strip(),
                "preconditions_completeness_rationale": row.get("preconditions_explanation", "").strip(),
                "postconditions_complete": row.get("postconditions_complete", "").strip(),
                "postconditions_completeness_rationale": row.get("postconditions_explanation", "").strip(),
            }

            results.append(technique_obj)

    with open(output_json, "w", encoding="utf-8") as out_f:
        json.dump(results, out_f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    #usage: python 11_20_json_to_csv.py input.csv output.json
    if len(sys.argv) != 3:
        print("Usage: python 11_20_json_to_csv.py input.csv output.json")
        sys.exit(1)

    input_csv_path = sys.argv[1]
    output_json_path = sys.argv[2]

    d3fend_json_path = "" #download https://d3fend.mitre.org/ontologies/d3fend.json and set this to the path of your local version

    convert_csv_to_json(input_csv_path, output_json_path, d3fend_json_path)
    print(f"Converted {input_csv_path} -> {output_json_path}")


