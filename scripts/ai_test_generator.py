import openai
import os
import sys

# Load API Key
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_tests():
    # Move up one directory to get the actual repo root
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Correct file path for HelloWorld.java inside src/main/java
    app_file_path = os.path.join(repo_root, "src", "main", "java", "HelloWorld.java")

    # Read Java file
    try:
        with open(app_file_path, "r") as f:
            code_snippet = f.read()
    except FileNotFoundError:
        print(f"⚠️ File {app_file_path} not found. Please check the path.")
        return

    # Automatically determine the package for the test class based on the project's src/test/java structure
    test_dir = os.path.join(repo_root, "src", "test", "java")
    if os.path.isdir(test_dir):
        # Assuming the test package structure mirrors the main Java package structure
        package_name = os.path.basename(test_dir)
    else:
        package_name = "your.package.name"  # Default placeholder if no test package structure exists

    # Customize the prompt for JUnit test generation
    prompt = f"""
    You are an AI that generates JUnit test cases for a simple Java class. The class does not use any web-related features or frameworks like Spring. Generate JUnit test cases that test the public methods of the class provided below. Ensure the tests use assertions and provide basic coverage for all public methods in the code.

    - Ensure the generated test class is **public**.
    - Ensure the generated test method is **public**.
    - Include a **package declaration** that matches the directory structure.
    - The test class should be named following the convention `ClassNameTest` (where `ClassName` is the class being tested).
    - For methods that print output (like `System.out.println()`), capture the output using `ByteArrayOutputStream` and `PrintStream`, then assert the output using `assertEquals`.
    - Ensure the code restores `System.out` after capturing output.

    Do not include any additional explanation or comments.

    ```
    {code_snippet}
    ```

    The generated test class should have the following package declaration:
    `package {package_name};`
    """

    # Request the test code from OpenAI API (Updated for ChatCompletion)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": prompt}]
    )

    # Extract the generated test code
    test_code = response.choices[0].message.content.strip()

    # Clean up any markdown formatting (like ```java)
    test_code = test_code.replace("```java", "").replace("```", "").strip()

    # Ensure src/test/java directory exists
    tests_dir = os.path.join(repo_root, "src", "test", "java")
    os.makedirs(tests_dir, exist_ok=True)

    # Save the generated test code to a file
    test_filename = "HelloWorldTest.java"
    with open(os.path.join(tests_dir, test_filename), "w") as f:
        f.write(test_code)

    print(f"✅ AI-Generated Unit Tests for HelloWorld.java: Saved to {test_filename}")

if __name__ == "__main__":
    generate_tests()
