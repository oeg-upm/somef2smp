import os
import json
import sys
from datetime import datetime

def generate_jsonld(somef_object):
    doc = { }

    context = {
        "schema": "http://schema.org/",
        "bs": "https://bioschemas.org/terms/",
        "codemeta": "https://w3id.org/codemeta/",
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "maSMP:": "https://discovery.biothings.io/view/maSMP/"
    }



    graph = []

    for key,value in mapping.items():
        property_object = next((entry for entry in jsonld_schema.get("@graph", []) if entry.get("@id") == key), None)
        if  "direct" in value:
            property_object["@value"]= value["direct"]
        graph.append(property_object)

    doc["@context"] = context

    doc["@graph"] = graph

    return doc

def generate_jsonld_v2(somef_object, jsonld):
    for entry in jsonld["@graph"]:
        if entry["@id"] in mapping:
            value = mapping[entry["@id"]]
            try:
                if value["type"] == "direct":
                    entry[value["attribute_name"]] = value["attribute_value"]
                elif value["type"] == "somef":
                    if value["attribute_value"] in somef_object:
                        entry[value["attribute_name"]] = somef_object[value["attribute_value"]][0]["result"]["value"]
            except:
                print ("Problem to get value from "+str(entry["@id"]))

    return jsonld


def load_mappings():
    try:
        mappings_file = open("mappings.json","r")
        return json.load(mappings_file)
    except Exception as ex:
        print (ex)

def load_maSMP_schema():
    try:
        #return jsonld.set_document_loader("https://raw.githubusercontent.com/zbmed-semtec/maSMPs/main/schema/maSMP_schema_v2.0.0/types/maSMP.jsonld")
        schema_file = open("maSMP.jsonld","r")
        return json.load(schema_file)
    except Exception as ex:
        print (ex)

# Get the total number of arguments
num_args = len(sys.argv)
if num_args != 2:
    print("Wrong number of parameters")
    print("somef2smp <name_directory>")
    sys.exit(-1)


directory = sys.argv[1]
print("Exploring directory: "+directory)

mapping = load_mappings()

jsonld_schema = load_maSMP_schema()

current_date = datetime.now()
formatted_date = current_date.strftime("%Y-%m-%d")

jsonld_schema["@context"]["@dateModified"]= formatted_date

# Convert the original JSON object to a JSON-formatted string
json_string = json.dumps(jsonld_schema)

files = os.listdir(directory)
for file in files:
    # Open the file
    json_file = open(directory+"/"+file, 'r')

    somef_json = json.load(json_file)

    json_file.close()

    # Parse the JSON-formatted string back into a new JSON object
    cloned_json_object = json.loads(json_string)

    jsonld = generate_jsonld_v2(somef_json, cloned_json_object)


    output_file = open("output_test/"+file.replace(".json",".jsonld"), 'w')
    json.dump(jsonld, output_file, indent=2)
    output_file.close()
