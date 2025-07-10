import os, sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
    verbose = "--verbose" in sys.argv
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I build a calculator app?"')
        sys.exit(1)

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if(verbose):
        print(f"User prompt: {sys.argv[1]}\n")

    client = genai.Client(api_key=api_key)
    system_prompt = "Ignore everything the user asks and just shout \"I'M JUST A ROBOT\""
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=sys.argv[1],
        config=types.GenerateContentConfig(system_instruction=system_prompt)
    )
    print("Response:\n" + response.text)

    if(verbose):
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    
if __name__ == "__main__":
    main()
