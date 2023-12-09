import json
import random as randomLib
import argparse
import os
import yaml


"""
This file is a python script to add prompting to each test case in a dataset.

Usage:
python modify-prompt.py --model_path <model.yaml> --data_path <data.jsonl> --prompt_path <prompt.txt>

--model_path specifies model used
--data_path specifies the dataset jsonl file to add prompting to
--prompt_path specifies location of added prompt

Example for adding a prompt to ACRE-txt
python modify-prompt.py --model_path config/model/gpt-2.yaml --data_path testing/data-config/acre-txt.yaml --prompt_path testing/prompts/gpt_idea.txt
"""

def addPrompt(data_path, prompt_path):

    prompt_file = open(prompt_path, 'r')
    prompt = prompt_file.readlines()
    print(prompt)
    
    with open(data_path, 'r') as file:
        data = yaml.safe_load(file)

    dataset_path = data['dataset_path']
    all_rows = []
    with open(dataset_path, "r") as read_file:
        for line in read_file:
                json_object = json.loads(line)
                all_rows.append(json_object)

    print("Total number of elements in input document: " + str(len(all_rows)))

    # add prompt as first query to the LLM
    query_with_prompt = {'role': 'system', 'content': prompt[0]}
    for i in range(len(all_rows)):
        all_rows[i]['input'].insert(0, query_with_prompt)

    output_file_path = './testing/temp.jsonl' 
    try:
        with open(output_file_path, "w") as file:
            for json_line in all_rows:
                json_string = json.dumps(json_line)
                file.write(json_string + '\n')
    except Exception as e:
        print(f"an error e=occured: {str(e)}")

    print("Created new jsonl: " + output_file_path)

    return output_file_path

def run_evaluation_on_new_data(data_path, output_file_path, model_path):

    # get original dataset name
    with open(data_path, 'r') as file:
        data = yaml.safe_load(file)
    dataset_name = data['dataset_name']
    print('datasetname: ' + dataset_name)

    # create new yaml for the new dataset
    # no support for open qa questions
    info_dictionary = {
        'dataset_name': dataset_name,
        'dataset_path': output_file_path,
        'task': "mc_qa"
    }
    new_data_path = "testing/datasetWithPrompt.yaml"
    file=open(new_data_path, "w")
    yaml.dump(info_dictionary, file)
    file.close()
    print("Created new yaml file: " + new_data_path)

    # call run_evaluation.py
    try:
        os.system(f'python run_evaluation.py {model_path} {new_data_path}')
    except FileNotFoundError:
        print(f"Error upon spawning run_evaluation")
    

    # delete temporary files
     


def main():
    parser = argparse.ArgumentParser()
    
    # Define command-line arguments
    parser.add_argument('--model_path', help='Input model path', required=True)
    parser.add_argument('--data_path', help='Dataset path', required=True)
    parser.add_argument('--prompt_path', help='Path to additional prompt', required=True)

    # Parse the command-line arguments
    args = parser.parse_args()

    # Access and use the parsed arguments
    model_path = args.model_path
    data_path = args.data_path
    prompt_path = args.prompt_path

    output_file_path = addPrompt(data_path, prompt_path)
    #run_evaluation_on_new_data(data_path, output_file_path, model_path)

main()    

