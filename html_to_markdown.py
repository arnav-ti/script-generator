#!/usr/bin/env python3
"""
HTML to Markdown Converter

This script extracts content from an HTML file with a section having class "l-measure"
and converts it to a well-formatted markdown file.
"""

import re
import os
from bs4 import BeautifulSoup

# Hardcoded file paths
HTML_FILE_PATH = 'input/lesson.html'
OUTPUT_FILE_PATH = 'output/lesson-content.md'

def extract_content_from_html(html_file_path, output_file_path):
    """
    Extract content from the HTML file and convert it to markdown
    
    Args:
        html_file_path (str): Path to the input HTML file
        output_file_path (str): Path to the output markdown file
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        print(f"Reading HTML file: {html_file_path}")
        # Read the HTML file
        with open(html_file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        
        # Parse the HTML using BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Find the section with class "l-measure"
        l_measure_section = soup.find('section', class_='l-measure')
        
        if not l_measure_section:
            print("Could not find section with class 'l-measure'")
            return False
        
        print("Extracting content from 'l-measure' section...")
        # Create markdown content
        markdown_content = process_html_to_markdown(l_measure_section)
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_file_path) or '.', exist_ok=True)
        
        # Write markdown content to file
        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.write(markdown_content)
        
        print(f"Markdown content saved to {output_file_path}")
        return True
    
    except Exception as e:
        print(f"Error processing HTML file: {e}")
        return False

def process_html_to_markdown(element):
    """
    Recursively convert HTML elements to markdown
    
    Args:
        element: BeautifulSoup element
    
    Returns:
        str: Markdown representation of the HTML
    """
    if element is None:
        return ""
    
    # Initialize the markdown text
    markdown_text = ""
    
    # Process based on element type
    if isinstance(element, str):
        return element.strip()
    
    # Process all children recursively
    if hasattr(element, 'children'):
        for child in element.children:
            if child.name:
                child_markdown = convert_element_to_markdown(child)
                markdown_text += child_markdown
            elif child.string and child.string.strip():
                markdown_text += child.string.strip() + "\n\n"
    
    return markdown_text

def convert_element_to_markdown(element):
    """
    Convert a single HTML element to its markdown equivalent
    
    Args:
        element: BeautifulSoup element
    
    Returns:
        str: Markdown representation of the element
    """
    if element is None:
        return ""
    
    # Process different HTML elements
    if element.name == 'h1':
        return f"# {element.get_text().strip()}\n\n"
    elif element.name == 'h2':
        return f"## {element.get_text().strip()}\n\n"
    elif element.name == 'h3':
        return f"### {element.get_text().strip()}\n\n"
    elif element.name == 'h4':
        return f"#### {element.get_text().strip()}\n\n"
    elif element.name == 'h5':
        return f"##### {element.get_text().strip()}\n\n"
    elif element.name == 'h6':
        return f"###### {element.get_text().strip()}\n\n"
    elif element.name == 'p':
        text = element.get_text().strip()
        if text:
            return f"{text}\n\n"
        return ""
    elif element.name == 'a':
        href = element.get('href', '')
        text = element.get_text().strip()
        return f"[{text}]({href})"
    elif element.name == 'strong' or element.name == 'b':
        return f"**{element.get_text().strip()}**"
    elif element.name == 'em' or element.name == 'i':
        return f"*{element.get_text().strip()}*"
    elif element.name == 'ul':
        markdown = "\n"
        for li in element.find_all('li', recursive=False):
            li_text = process_html_to_markdown(li).strip()
            markdown += f"- {li_text}\n"
        return markdown + "\n"
    elif element.name == 'ol':
        markdown = "\n"
        for i, li in enumerate(element.find_all('li', recursive=False), 1):
            li_text = process_html_to_markdown(li).strip()
            markdown += f"{i}. {li_text}\n"
        return markdown + "\n"
    elif element.name == 'li':
        # Process li contents as markdown
        markdown = ""
        for child in element.children:
            if hasattr(child, 'name'):
                markdown += convert_element_to_markdown(child)
            elif child.string and child.string.strip():
                markdown += child.string.strip()
        return markdown
    elif element.name == 'table':
        return convert_table_to_markdown(element)
    elif element.name == 'br':
        return "\n"
    elif element.name == 'hr':
        return "---\n\n"
    elif element.name == 'blockquote':
        quote_text = process_html_to_markdown(element).strip()
        quoted_lines = [f"> {line}" for line in quote_text.split('\n')]
        return '\n'.join(quoted_lines) + "\n\n"
    elif element.name == 'pre' or element.name == 'code':
        code_text = element.get_text().strip()
        if element.name == 'pre':
            return f"```\n{code_text}\n```\n\n"
        else:
            return f"`{code_text}`"
    elif element.name == 'img':
        alt = element.get('alt', '')
        src = element.get('src', '')
        return f"![{alt}]({src})\n\n"
    elif element.name in ['div', 'section', 'article', 'main', 'span', 'figure', 'figcaption']:
        # For container elements, process their children
        return process_html_to_markdown(element)
    else:
        # For other elements, just process their contents
        return process_html_to_markdown(element)

def convert_table_to_markdown(table):
    """
    Convert an HTML table to markdown format
    
    Args:
        table: BeautifulSoup table element
    
    Returns:
        str: Markdown representation of the table
    """
    if not table:
        return ""
    
    markdown_table = "\n"
    rows = table.find_all('tr')
    
    if not rows:
        return markdown_table
    
    # Process header row if it exists
    header_cells = rows[0].find_all(['th', 'td'])
    if header_cells:
        header_row = "| " + " | ".join([cell.get_text().strip() for cell in header_cells]) + " |\n"
        markdown_table += header_row
        
        # Add separator row
        separator_row = "| " + " | ".join(["---" for _ in header_cells]) + " |\n"
        markdown_table += separator_row
    
    # Process data rows
    for row in rows[1:] if header_cells else rows:
        cells = row.find_all(['td', 'th'])
        if cells:
            data_row = "| " + " | ".join([cell.get_text().strip() for cell in cells]) + " |\n"
            markdown_table += data_row
    
    return markdown_table + "\n"

def clean_markdown(markdown_text):
    """
    Clean up the generated markdown text
    
    Args:
        markdown_text (str): Raw markdown text
    
    Returns:
        str: Cleaned markdown text
    """
    # Replace multiple newlines with just two
    cleaned_text = re.sub(r'\n{3,}', '\n\n', markdown_text)
    
    # Clean up spaces before punctuation
    cleaned_text = re.sub(r'\s+([.,;:!?])', r'\1', cleaned_text)
    
    return cleaned_text

def main():
    """Main function to run the HTML to Markdown converter"""
    print("HTML to Markdown Converter")
    print("==========================")
    print(f"Input HTML file: {HTML_FILE_PATH}")
    print(f"Output markdown file: {OUTPUT_FILE_PATH}")
    
    # Validate input file
    if not os.path.exists(HTML_FILE_PATH):
        print(f"Error: The file '{HTML_FILE_PATH}' does not exist.")
        return
    
    # Extract content and convert to markdown
    success = extract_content_from_html(HTML_FILE_PATH, OUTPUT_FILE_PATH)
    
    if success:
        print("Conversion completed successfully!")
    else:
        print("Conversion failed.")

if __name__ == "__main__":
    main() 