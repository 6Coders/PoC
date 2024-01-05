import torch
from transformers import AutoTokenizer, AutoModel
import json

class ChatSQL:

  #Attributi
  path = None
  tc_embs = None
  schema = None
  tokenizer = None
  model = None

  def __init__(self, path):
    
    self.path = path
    #Dizionario Dati
    with open(path, "r") as file:
        self.schema = json.load(file)

    #Inizializzazione modello
    model_name = "sentence-transformers/stsb-roberta-large"
    self.tokenizer = AutoTokenizer.from_pretrained(model_name)
    self.model = AutoModel.from_pretrained(model_name)
    
    #Embeddings
    self.tc_embs = {}

    for table_name, table_info in self.schema["tables_info"].items():
        #Tabelle
        table_description = table_info["table_description"]
        inputs = self.tokenizer(table_description, return_tensors="pt", truncation=True)
        outputs = self.model(**inputs)
        table_embedding = outputs.pooler_output
        self.tc_embs[table_name] = table_embedding

        #Colonne
        for column_info in table_info["columns"]:
            column_description = column_info["column_description"]
            inputs = self.tokenizer(column_description, return_tensors="pt", truncation=True)
            outputs = self.model(**inputs)
            column_embedding = outputs.pooler_output
            self.tc_embs[column_info["column_name"]] = column_embedding

  def request_processing(self, request):
    
    query_inputs = self.tokenizer(request, return_tensors="pt", truncation=True)
    query_outputs = self.model(**query_inputs)
    query_embedding = query_outputs.pooler_output

    # Calcolo similaritÃ  tramite cosine similarity, query e embeddings tab-col
    similarities = torch.nn.functional.cosine_similarity(
        query_embedding,
        torch.stack(list(self.tc_embs.values())),
        dim=-1
    )

    #Limite per considerare valido il match
    threshold = 0.75

    matches = [name for name, sim in zip(self.tc_embs.keys(), similarities) if sim.item() > threshold]

    #Salvataggio valori per stampa
    printed_tables = set()
    resultstr = "Prompt Generato per ChatGPT\n\nAct as an SQL Expert. Given the database structure below, generate a query to: " + request +"\n"
    for match in matches:
        if "." in match:
            #Colonne
            table_name, column_name = match.split(".")
            if table_name not in printed_tables and table_name in self.schema["tables_info"]:
                resultstr = self.retrieve_table_structure(table_name, resultstr)
                printed_tables.add(table_name)
        else:
            #Tabelle
            if match.lower() in self.schema["tables_info"]:
                table_name = match.lower()
                resultstr = self.retrieve_table_structure(table_name, resultstr)
                printed_tables.add(table_name)

    #Preparazione stampa tabella se match con colonna
    for table_name, table_info in self.schema["tables_info"].items():
        for column_info in table_info["columns"]:
            column_name = column_info["column_name"]
            if column_name in matches and table_name not in printed_tables and table_name in self.schema["tables_info"]:
                resultstr = self.retrieve_table_structure(table_name, resultstr)
                printed_tables.add(table_name)
    
    return resultstr

  def retrieve_table_structure(self, name, resultstr):
    table_info = self.schema["tables_info"][name]
    resultstr = resultstr + "Table name: " + name + "\n"

    columns_str = ", ".join(column["column_name"] for column in table_info["columns"])
    resultstr = resultstr + "- Columns: \n" + columns_str+"\n"

    foreign_keys = self.schema.get("foreign_keys", [])
    for fk in foreign_keys:
        if fk["table"] == name:
            resultstr = resultstr +"\nForeign Key: "+fk['foreign_key']+"\nAttribute: "+fk['attribute']+"\nReference Table: "+fk['reference_table']+"\nReference Attribute: "+fk['reference_attribute']+"\n"
    resultstr = resultstr+"\n"
    return resultstr

  def get_path(self):
    return self.path