# Math Script Generator Pipeline

This repository contains a pipeline for generating educational math scripts from lesson content through an iterative refinement process.

## Overview

The pipeline consists of two main components:

1. **HTML to Markdown Converter** - Extracts lesson content from HTML files
2. **Script Pipeline** - Generates and refines teaching scripts through multiple iterations

## Prerequisites

- Python 3.6+
- OpenAI API key
- The page source of the lesson you want to generate. eg. https://access.openupresources.org/curricula/our6-8math-v3/en/default/grade-6/unit-1/section-a/lesson-2/index.html#warm-up

## Installation

1. Clone this repository
2. Install required dependencies:
```
pip install openai beautifulsoup4
```
3. Set your OpenAI API key as an environment variable:
```
export OPENAI_API_KEY="your-api-key-here"
```
4. Save the page source in `input/lesson.html`

## Usage

### 1. Convert HTML Lesson to Markdown

First step is to convert your HTML page to markdown:

```bash
python html_to_markdown.py
```

This will:
- Read the HTML file from `input/lesson.html`
- Extract content from the section with class "l-measure"
- Convert it to markdown format
- Save the output to `output/lesson-content.md`

### 2. Generate Math Script

Once you have the lesson content in markdown format, run the script pipeline:

```bash
python script_pipeline.py
```

This will:
1. Generate an initial script based on the lesson content
2. Analyze the script for issues
3. Fix the script based on the analysis
4. Repeat steps 2-3 for three iterations, with each iteration improving upon the previous

## Directory Structure

```
├── input/
│   └── lesson.html            # Input HTML lesson file
├── output/
│   ├── lesson-content.md      # Converted markdown content
│   └── iterations/            # Generated scripts and analyses
│       ├── v1_initial_script.txt
│       ├── v1_analysis.txt
│       ├── v1_fixed_script.txt
│       ├── v2_analysis.txt
│       ├── v2_fixed_script.txt
│       ├── v3_analysis.txt
│       └── v3_fixed_script.txt
├── generator.txt              # Prompt for initial script generation
├── analyser.txt               # Prompt for script analysis
├── fixer.txt                  # Prompt for script fixing
├── html_to_markdown.py        # HTML to Markdown converter
└── script_pipeline.py         # Script generation pipeline
```

## Customization

You can customize the process by modifying:

- The prompt files (`generator.txt`, `analyser.txt`, `fixer.txt`)
- The model parameters in `script_pipeline.py` (model, temperature)
- File paths in both Python scripts

## Example

1. Place your HTML lesson in `input/lesson.html`
2. Run `python html_to_markdown.py`
3. Run `python script_pipeline.py`
4. Find your final refined script in `output/iterations/v3_fixed_script.txt` 