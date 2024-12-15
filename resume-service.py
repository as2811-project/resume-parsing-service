import re
import json
from pypdf import PdfReader

def extract_sections(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    text = text.strip()

    # regex patterns for section headings
    section_patterns = {
        "Experience": r"(?i)(Experience|Work Experience|Professional Experience)",
        "Skills": r"(?i)(Skills|Technical Skills|Key Skills)",
        "Projects": r"(?i)(Projects|Key Projects|Professional Projects)"
    }
    all_section_heading_pattern = r"(?i)(Experience|Work Experience|Professional Experience|Education|Skills|Technical Skills|Key Skills|Projects|Certifications|Summary|Profile|Awards|References|Volunteering)"

    matches = list(re.finditer(all_section_heading_pattern, text))

    # Extract each section
    extracted_data = {}
    for section, pattern in section_patterns.items():
        for i, match in enumerate(matches):
            if re.match(pattern, match.group()):
                start = match.end()
                end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
                extracted_data[section] = text[start:end].strip()
                break
        else:
            extracted_data[section] = None

    return json.dumps(extracted_data, indent=4)

# usage
file_path = input("Enter file path: ")
extracted_sections = extract_sections(file_path)
print(extracted_sections)
