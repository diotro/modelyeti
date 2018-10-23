import json
import sys
import requests

"""

Call like:
 python3 model_cli.py model "credit" income 75000 credit_score 500
"""

def hit_api(args_dict):
    model_name = args_dict.pop('model')
    return requests.get(f"http://localhost:5000/model/{model_name}/predict/", data=json.dumps(args_dict)).content


def pretty_print_result(args_dict, api_result):
    def print_within_box(string=""):
        print(f"*{string.ljust(78, ' ')}*")

    def print_empty_line():
        print_within_box("")

    def print_delim_line():
        print_within_box("*" * 78)


    print_delim_line()
    print_within_box(" Asked model for prediction for data: ")

    for key, value in args_dict.items():
        print_within_box(f"    {key.title()}: {value}")

    print_empty_line()
    print_delim_line()
    print_within_box(" Received Prediction: ")
    print_empty_line()
    print_within_box(f"    {str(api_result, encoding='utf8')}")
    print_empty_line()
    print_delim_line()



if __name__ == '__main__':
    args = sys.argv[1:]

    args_dict = {}
    while args:
        key = args.pop(0)
        value = args.pop(0)
        # Convert CLI args to int if possible, otherwise store as string
        try:
            args_dict[key] = int(value)
        except:
            args_dict[key] = value

    pretty_print_result(args_dict, hit_api(args_dict))
