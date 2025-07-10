import os, sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from call_function import available_functions, call_function
from prompts import system_prompt
from functions.get_files_info import get_files_info

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

    messages = [
        types.Content(
            role="user",
            parts=[types.Part(text=sys.argv[1])]
        )
    ]

    for i in range(0,20):
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions], system_instruction=system_prompt
                )
            )

            for candidate in response.candidates:
                messages.append(candidate.content)
            
            if(verbose):
                print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

            
            if not response.function_calls:
                print(response.text)
                break

            for function_call_part in response.function_calls:
                result = call_function(function_call_part, verbose)
                messages.append(result)

        except Exception as e:
            print (f"Error: {e}")


    
if __name__ == "__main__":
    main()
