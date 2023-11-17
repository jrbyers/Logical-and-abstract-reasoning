import json
import random as randomLib
import argparse
import os


"""
This file is a python script to generate a smaller subset of a particular database
for testing purposes.

Usage:
python generate-small-test.py --file_path <filepath.jsonl> --num_elements <integer> --random <boolean>

--file_path specifies the dataset jsonl file you wish to create a subset of
--num_elements specifies the total number of tests cases in your test dataset
--random True is a random sample, False is the first num_elements of test cases

Example for 250 random elements from ACRE
python generate-small-test.py --file_path data/ACRE/text/IID/test.jsonl --num_elements 250 --random True


"""

def load_JSON(file_path, num_elements, random):
    
    all_rows = []
    with open(file_path, "r") as read_file:
        for line in read_file:
                json_object = json.loads(line)
                all_rows.append(json_object)

    print("Total number of elements in input document: " + str(len(all_rows)))
    num_elements = int(num_elements)
    if num_elements > len(all_rows):
        print("Error specified number of rows is too high")
        return
    
    row_selection = []
    if random == 'False': 
        row_selection = all_rows[:num_elements]
    else: 
        randomLib.shuffle(all_rows)
        row_selection = all_rows[:num_elements]

    print("Done compiling jsonl file")

    create_new_document(row_selection, file_path, num_elements, random)

def create_new_document(selected_data, file_path, num_elements, random):
    file_name = file_path[5:]       # remove data/ from file_path name

    parts = file_name.split('/')
    dataset_name = parts[0]

    file_name = file_name.replace("/", "_")

    if random == 'True':
        file_name = str(num_elements) + "rand_" + file_name
    else:
        file_name = str(num_elements) + "first_" + file_name



    output_file_path = './testing/small-data/' + dataset_name + '/' + file_name
    try:
        with open(output_file_path, "w") as file:
            for json_line in selected_data:
                json_string = json.dumps(json_line)
                file.write(json_string + '\n')
    except Exception as e:
        print(f"an error e=occured: {str(e)}")

    print("Created new jsonl: " + output_file_path)
     


def main():
    parser = argparse.ArgumentParser()
    
    # Define command-line arguments
    parser.add_argument('--file_path', help='Input file path', required=True)
    parser.add_argument('--num_elements', help='Number of dataset rows', required=True)
    parser.add_argument('--random', help='If user wants random subsample or not', required=True)

    # Parse the command-line arguments
    args = parser.parse_args()

    # Access and use the parsed arguments
    file_path = args.file_path
    num_elements = args.num_elements
    random = args.random

    load_JSON(file_path, num_elements, random)

main()    

