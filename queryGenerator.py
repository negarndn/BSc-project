


def generate_sparql_query(entity, relation, is_entity_at_subject=True):
    if is_entity_at_subject:
        query = f"SELECT DISTINCT ?o WHERE {{ <http://fkg.iust.ac.ir/resource/{entity}> <http://fkg.iust.ac.ir/ontology/{relation}> ?o.}}"
    else:
        query = f"SELECT DISTINCT ?o WHERE {{  http://fkg.iust.ac.ir/ontology/<{relation}> <http://fkg.iust.ac.ir/resource/{entity}>. }}"

    print(query)
    return query

#
# print(generate_sparql_query(filtered_entity, predicted_label))