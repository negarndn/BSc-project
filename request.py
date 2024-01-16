import requests
import json

from NER import NER
from RelationPrediction import RP
from queryGenerator import generate_sparql_query

import xml.etree.ElementTree as ET

def process_sparql_response(response):
    try:
        result = json.loads(response)
        bindings = result['results']['bindings']
        if bindings:
            return [binding['o']['value'] for binding in bindings]
        else:
            return None
    except (KeyError, json.JSONDecodeError) as e:
        print(f"Error decoding or extracting information from SPARQL response: {e}")
        return None

def execute_sparql_query(query):
    api_endpoint = "http://farsbase.net:8890/sparql/"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    params = {"query": query}

    response = requests.post(api_endpoint, headers=headers, params=params)

    if response.status_code == 200:
        return response.text
    else:
        print(f"Error: {response.status_code}")
        return None


def request2(sentence):

    # # Example usage
    # entity = "ایران"  # Replace with your entity
    # relation = "capital"  # Replace with your relation
    is_entity_at_subject = True  # Adjust based on your system's logic

    # Generate SPARQL query
    filtered_entity = NER(sentence)
    print(filtered_entity)
    relation = RP(sentence)
    print(relation)
    parts = relation.split('_')
    sparql_query = generate_sparql_query(filtered_entity, parts[len(parts)-1], is_entity_at_subject)
    print(sparql_query)
    # sparql_query = "SELECT DISTINCT ?o WHERE { <http://fkg.iust.ac.ir/resource/ایران> <http://fkg.iust.ac.ir/ontology/capital> ?o.}"
    # print(sparql_query)
    # Execute the SPARQL query
    sparql_response = execute_sparql_query(sparql_query)
    print(sparql_response)

    # Print the SPARQL Response
    # print("SPARQL Response:")
    # print(sparql_response)
    return sparql_response


# request2("محل تولد حافظ کجاست")


