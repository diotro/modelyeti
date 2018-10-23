import json
import sys
import requests

"""

Call like python3 model_cli.py model "credit" income 75000 credit_score 500
"""

def hit_api(args_dict):
    model_name = args_dict.pop('model')
    return requests.get(f"http://localhost:5000/model/{model_name}/predict/", data=json.dumps(args_dict)).content


def pretty_print_result(args_dict, api_result):
    print("-" * 80)
    print("| Asked model for prediction for data: ")

    for key, value in args_dict.items():
        print(f"| {key.title()}: {value}")

    print("-" * 80)
    print("| Received Prediction: ")
    print(f"| {str(api_result, encoding='utf8')}")
    print("-" * 80)


if __name__ == '__main__':
    args = sys.argv[1:]

    args_dict = {}
    while args:
        key = args.pop(0)
        value = args.pop(0)
        try:
            args_dict[key] = int(value)
        except:
            args_dict[key] = value
    print(args_dict)
    pretty_print_result(args_dict, hit_api(args_dict))
