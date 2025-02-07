# This python script polls the console for input to recursively generate a python script

import os
import re
import sys
from openai import OpenAI

def make_input_safe(input_string):
    # Remove any characters that may cause issues
    safe_input = re.sub(r'[^\w\s]', '', input_string)
    return safe_input

def clean_file(filename):
    with open(filename, 'r') as f:
        content = f.read()
    
    # Remove non-comment backticks and other prompt-related text using regular expressions
    cleaned_content = re.sub(r'(?<!python:)(\s*backtick)', r'\1', content)
    cleaned_content = re.sub(r'(?<!python:)(python:\s*)', r'\1', cleaned_content)
    cleaned_content = re.sub(r'(#\s+)', '# ', cleaned_content)  # Remove comments with leading whitespace
    
    return cleaned_content

def execute_python_script(filename):
    os.system('python3 {} > temp.txt'.format(filename))

def save_response_to_file(response, filename):
    # Write the response to the specified file with a .py extension
    filtered_response = response.split("```python\n")[-1].split("```")[0]
    with open(filename + ".py", 'w') as f:
        f.write(filtered_response)

def recursive_build(user_input, iteration, prompt):
    iteration += 1
    # Send user input to OpenAI for chat completion
    completion = client.chat.completions.create(
        model="LLaMA_CPP",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_input}
        ]
    )
    response = completion.choices[0].message.content
    
    if "DONE" in response.upper() or not response:
        print('Success? I am done.')
        exit()

    filename = make_input_safe(user_input) + str(iteration)

    save_response_to_file(response, filename)
    
    # Execute the contents of the file using Python 3
    execute_python_script(filename)
    
    # Read the Python script output
    with open("temp.txt", "r") as file:
        next_input = file.read()

    print ("-------Execution: ----------")
    print (next_input)
    print ("----------------------------")
    
    recursive_build(next_input, iteration, prompt)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <initial_input> <prompt>")
        sys.exit(1)

    initial_input = sys.argv[1]
    prompt = sys.argv[2]

    # Initialize OpenAI client
    client = OpenAI(
        base_url="http://localhost:8080/v1",  # Update with your API server IP and port
        api_key="sk-no-key-required"
    )

    print ("Prompt: "+ initial_input)
    recursive_build(initial_input, 0, prompt)
