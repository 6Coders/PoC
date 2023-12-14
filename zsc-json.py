import json
from transformers import pipeline

# Estrazione da File JSON
def extract_tables_columns(json_data):
    tables = []
    columns = []

    for table_name, table_info in json_data["tables_info"].items():
        tables.append(table_name)
        columns.extend(table_info["columns"])

    return tables + columns

def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# Stampa Risultati Rilevanti
def print_relevant_tables(user_request, results, json_data, threshold=0.5):
    relevant_tables = set()

    for label, score in zip(results["labels"], results["scores"]):
        if score > threshold and label in json_data["tables_info"]:
            relevant_tables.add(label)
        #MANCA CHECK su ATTRIBUTI SE SCORE > THRESHOLD

    print("Database Schema (tables, columns and foreign keys):")
    for table in relevant_tables:
        columns_str = ', '.join(json_data['tables_info'][table]['columns'])
        print(f"{table}: {columns_str}")

        for fk in json_data["foreign_keys"]:
            if fk["table"] == table:
                print(f"  - Foreign Key: {fk['foreign_key']}")
                print(f"    - Attribute: {fk['attribute']}")
                print(f"    - Reference Table: {fk['reference_table']}")
                print(f"    - Reference Attribute: {fk['reference_attribute']}")

# File JSON
json_data = read_json_file('dbs.json')
dbs = extract_tables_columns(json_data)

# Richiesta in Linguaggio Naturale
user_request = input("Inserisci la richiesta in linguaggio naturale (in Inglese): ")
print("Attendi la generazione del Prompt")

# Zero Shot Classification
zsc = pipeline("zero-shot-classification")
results = zsc(user_request, dbs, multi_label=True)

print("\nPROMPT GENERATO PER ChatGPT\n** \n")
print("Act as an SQL Expert. Given the database structure below, generate a query to")
print(user_request)
print("\n")

# Stampa Risultati - Necessario adattare lo score manualmente
print_relevant_tables(user_request, results, json_data, threshold=0.8)

print("\n**")
