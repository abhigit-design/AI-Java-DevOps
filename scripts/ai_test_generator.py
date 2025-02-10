import openai
import os
import sys

# Load API Key
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_tests():
    # Get the absolute path of the repository root
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Construct the full path to HelloWorld.java
    java_file_path = os.path.join(repo_root, "HelloWorld.java")

    # Check if the Java file exists
    if not os.path.exists(java_file_path):
        print("❌ HelloWorld.java not found in the repository.")
        return

    # Open the Java file
    with open(java_file_path, "r") as f:
        code_snippet = f.read()

    # Customize the prompt for JUnit test generation
    prompt = f"""
    You are an AI that generates JUnit test cases. Generate JUnit test cases for the following Java code.
    Ensure the tests use assertions and include basic coverage for all public methods in the code.
    Do not include any additional explanation or comments.
    ```
    {code_snippet}
    ```
    """

    # Request the test code from OpenAI API (Updated for ChatCompletion)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": prompt}]
    )


    # Extract the generated test code
    test_code = response.choices[0].message.content.strip()  # Clean any extra whitespace or unwanted text

    # Clean up any markdown formatting (like ```java)
    test_code = test_code.replace("```java", "").replace("```", "").strip()

    # Create the tests directory if it doesn't exist
    tests_dir = os.path.join(repo_root, 'tests')
    os.makedirs(tests_dir, exist_ok=True)

    # Save the generated test code to a file
    test_filename = "HelloWorldTest.java"
    with open(os.path.join(tests_dir, test_filename), "w") as f:
        f.write(test_code)

    print(f"✅ AI-Generated Unit Tests for HelloWorld.java: Saved to {test_filename}")

if __name__ == "__main__":
    generate_tests()
