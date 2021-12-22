import json

# Load the string dictionary from the JSON file
StringRscs = {}
with open('stringfile.json') as json_file:
    StringRscs = json.load(json_file)

# Function to evaluate the loaded f-strings. This is necessary because you can't include
# dictionary keys if doing it inline due to interference with single and double quotes.
# Taken from: https://stackoverflow.com/questions/47597831/python-fstring-as-function
def fstr(fstring_text, locals, globals=None):
    # Dynamically evaluate the provided fstring_text. Passing in locals and globals allows us
    # to access variables to insert into the f string.
    locals = locals or {}
    globals = globals or {}
    ret_val = eval(f'f"{fstring_text}"', locals, globals)
    return ret_val
