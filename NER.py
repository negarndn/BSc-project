from transformers import TFAutoModelForTokenClassification, AutoTokenizer, pipeline
# from RelationPrediction import new_sentence

def NER(new_sentence):

    tokenizer2 = AutoTokenizer.from_pretrained("HooshvareLab/bert-fa-base-uncased-ner-peyma")
    model2 = TFAutoModelForTokenClassification.from_pretrained("HooshvareLab/bert-fa-base-uncased-ner-peyma")
    twiner_mtl2 = pipeline('ner', model=model2, tokenizer=tokenizer2, ignore_labels=[])

    # print(new_sentence)
    predictions2 = twiner_mtl2(new_sentence)

    # for prediction in predictions:
    #     print(f"Entity: {prediction['word']}, Label: {prediction['entity']}, Score: {prediction['score']}")


    model_save_path = "NERmodel"
    model2.save_pretrained(model_save_path)
    tokenizer2.save_pretrained(model_save_path)

    # Load the saved model for inference
    loaded_tokenizer = AutoTokenizer.from_pretrained(model_save_path)
    loaded_model = TFAutoModelForTokenClassification.from_pretrained(model_save_path)
    twiner_mtl2 = pipeline('ner', model=loaded_model, tokenizer=loaded_tokenizer, ignore_labels=[])

    # Use the loaded model for inference
    # print(new_sentence)
    predictions2 = twiner_mtl2(new_sentence)

    non_o_entities2 = [(prediction['word'], prediction['entity']) for prediction in predictions2 if prediction['entity'] != 'O']

    for entity, label in non_o_entities2:
        print(f"Entity: {entity}, Label: {label}")

    result_string = '_'.join(entity for entity, label in non_o_entities2)
    print(result_string)
    concatenated_entities = ''.join([f"{entity}" for entity, label in non_o_entities2])
    print(concatenated_entities)
    filtered_entity = '_'.join(char for char in concatenated_entities if char.isalpha())
    print(filtered_entity)
    return result_string

# NER("علی دایی اهل کجاست")