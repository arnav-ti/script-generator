#!/usr/bin/env python3
"""
Math Script Pipeline

This script implements a pipeline that:
1. Generates an initial math script using a generator prompt
2. Analyzes the script for issues using an analyzer prompt
3. Fixes the script based on the analysis using a fixer prompt
4. Repeats the process for three iterations

Each iteration produces a new version of the script that improves upon the previous version.
"""

import os
import sys
from openai import OpenAI

# Hardcoded file paths
GENERATOR_PROMPT_FILE = 'generator.txt'  
ANALYZER_PROMPT_FILE = 'analyser.txt'   
FIXER_PROMPT_FILE = 'fixer.txt'
CONTENT_FILE = 'output/lesson-content.md'

# Output file paths for each iteration
OUTPUT_DIRS = 'output/iterations'
INITIAL_SCRIPT_FILE = f'{OUTPUT_DIRS}/v1_initial_script.txt'
ANALYSIS_FILES = [f'{OUTPUT_DIRS}/v{i}_analysis.txt' for i in range(1, 4)]
FIXED_SCRIPT_FILES = [f'{OUTPUT_DIRS}/v{i}_fixed_script.txt' for i in range(1, 4)]

# OpenAI configuration
MODEL = 'gpt-4'
TEMPERATURE = 0.7
API_KEY = os.getenv("OPENAI_API_KEY")

def read_file_content(file_path):
    """
    Read and return the content of a file
    
    Args:
        file_path (str): Path to the file
        
    Returns:
        str: Content of the file
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read().strip()
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        sys.exit(1)

def save_to_file(content, file_path):
    """
    Save content to a file
    
    Args:
        content (str): Content to save
        file_path (str): Path to the output file
    """
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"Content saved to {file_path}")
    except Exception as e:
        print(f"Error saving to {file_path}: {e}")
        sys.exit(1)

def get_openai_response(system_prompt, user_prompt, model=MODEL, temperature=TEMPERATURE):
    """
    Get a response from the OpenAI API
    
    Args:
        system_prompt (str): The system prompt
        user_prompt (str): The user prompt
        model (str): The model to use
        temperature (float): The temperature for generation
        
    Returns:
        str: The generated response
    """
    # Use the hardcoded API key
    api_key = API_KEY
    
    # Initialize the OpenAI client
    client = OpenAI(api_key=api_key)
    
    try:
        # Create the chat completion
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=temperature
        )
        
        # Return the response content
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        sys.exit(1)

def generate_initial_script(content):
    """
    Generate the initial script using the generator prompt
    
    Args:
        content (str): The lesson content
        
    Returns:
        str: The generated script
    """
    print("Generating initial script...")
    generator_prompt = read_file_content(GENERATOR_PROMPT_FILE)
    
    return get_openai_response(generator_prompt, content)

def analyze_script(script, iteration):
    """
    Analyze the script using the analyzer prompt
    
    Args:
        script (str): The script to analyze
        iteration (int): Current iteration number
        
    Returns:
        str: The analysis
    """
    print(f"Analyzing script (iteration {iteration})...")
    analyzer_prompt = read_file_content(ANALYZER_PROMPT_FILE)
    
    return get_openai_response(analyzer_prompt, script)

def fix_script(script, analysis, iteration):
    """
    Fix the script based on the analysis using the fixer prompt
    
    Args:
        script (str): The script to fix
        analysis (str): The analysis of the script
        iteration (int): Current iteration number
        
    Returns:
        str: The fixed script
    """
    print(f"Fixing script (iteration {iteration})...")
    fixer_prompt = read_file_content(FIXER_PROMPT_FILE)
    
    # Combine the script and analysis into a single user prompt for the fixer
    user_prompt = f"Original Script:\n\n{script}\n\nReviewer's Feedback:\n\n{analysis}"
    
    return get_openai_response(fixer_prompt, user_prompt)

def run_pipeline():
    """
    Run the full pipeline for three iterations
    """
    # Ensure output directory exists
    os.makedirs(OUTPUT_DIRS, exist_ok=True)
    
    # Read the lesson content
    content = read_file_content(CONTENT_FILE)
    
    # Generate the initial script
    initial_script = generate_initial_script(content)
    save_to_file(initial_script, INITIAL_SCRIPT_FILE)
    
    current_script = initial_script
    
    # Run three iterations of analyze-fix
    for i in range(3):
        iteration = i + 1
        print(f"\n=== Iteration {iteration} ===\n")
        
        # Analyze the current script
        analysis = analyze_script(current_script, iteration)
        save_to_file(analysis, ANALYSIS_FILES[i])
        
        # Fix the script based on the analysis
        fixed_script = fix_script(current_script, analysis, iteration)
        save_to_file(fixed_script, FIXED_SCRIPT_FILES[i])
        
        # Update the current script for the next iteration
        current_script = fixed_script
        
        print(f"Completed iteration {iteration}\n")
    
    print("\nPipeline completed successfully!")
    print(f"Initial script: {INITIAL_SCRIPT_FILE}")
    for i in range(3):
        iteration = i + 1
        print(f"Version {iteration} analysis: {ANALYSIS_FILES[i]}")
        print(f"Version {iteration} script: {FIXED_SCRIPT_FILES[i]}")

def main():
    """
    Main function
    """
    print("Math Script Pipeline")
    print("===================")
    
    # Check if required files exist
    required_files = [GENERATOR_PROMPT_FILE, ANALYZER_PROMPT_FILE, FIXER_PROMPT_FILE, CONTENT_FILE]
    for file_path in required_files:
        if not os.path.exists(file_path):
            print(f"Error: Required file '{file_path}' does not exist.")
            sys.exit(1)
    
    # Run the pipeline
    run_pipeline()

if __name__ == "__main__":
    main() 