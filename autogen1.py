flesh out a github repot for this project: import re
import requests
import sys

#instructions = "you are a php code generator. without explanation, generate php code to: calculate what day of the week feb 3rd, 2075 is"
instructions = "you are a php code generator. without explanation, "

# Configuration for llama.cpp API
LLAMA_API_URL = "http://192.168.42.15:8080/completion"  # Update with your llama.cpp API endpoint

def generate_code(prompt):
    """
    Generates PHP code using the locally hosted llama.cpp model.
    """
    payload = {
        "prompt": f"{prompt}",
        "temperature": 0.7,
        "max_tokens": 500,
    }
    response = requests.post(LLAMA_API_URL, json=payload)
    if response.status_code == 200:
        return response.json().get("content", "").strip()
    else:
        raise Exception(f"Failed to generate code: {response.text}")

def remove_php_comments(code):
    """
    Removes PHP comments from a string of code.

    Args:
        code (str): The PHP code as a string.

    Returns:
        str: The code with comments removed.
    """
    # Remove single-line comments (starting with // or #)
    code = re.sub(r'//.*$', '', code, flags=re.MULTILINE)
    code = re.sub(r'#.*$', '', code, flags=re.MULTILINE)

    # Remove multi-line comments (/* ... */)
    code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)

    # Remove empty lines left after removing comments
    code = "\n".join([line for line in code.splitlines() if line.strip()])

    return code

def recursive_code_generation(initial_prompt, max_iterations=10):
    """
    Recursively generates and refines PHP code until the output meets the requirements.
    """
    iteration = 0
    current_prompt = initial_prompt

    while iteration < max_iterations:
#        print(f"Iteration {iteration + 1}: Generating code...")
        code = generate_code(current_prompt)

        # Clean up the generated code
        code = re.sub(r"```php\s*", "", code)
        code = re.sub(r"```\s*", "", code)
        code = remove_php_comments(code)

 #       print(f"Generated Code:\n{code}\n")

        # Output the generated PHP code
        print(code)
        return code

    print("Maximum iterations reached. Could not generate code that meets the requirements.")
    return None

if __name__ == "__main__":
    # Get the initial prompt from command-line arguments
    if len(sys.argv) < 2:
        print("Error: No prompt provided.")
        sys.exit(1)
    initial_prompt = sys.argv[1]

    # Start the recursive code generation process
    final_code = recursive_code_generation(instructions + initial_prompt)

    if final_code:
        print ('<pre>')
        print(htmlspecialchars(final_code))
        print ('</pre>')
        print(final_code)
