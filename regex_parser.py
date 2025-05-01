import re
from typing import Dict

def parse_text(text: str) -> Dict:
    result = {}
    result['fechas'] = re.findall(r'\b\d{4}-\d{2}-\d{2}\b|\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b', text)
    result['nombres'] = re.findall(r'\b[A-Z][a-z]+\s[A-Z][a-z]+\b', text)
    result['palabras_suecas'] = re.findall(r'\b(?:Göteborg|Drottningholm|Kungsholm|Fritidsbeteget|Utvandlingsbeteget)\b', text)
    result['lugares'] = re.findall(r'\b(?:New York|Chicago|Buffalo|Ellis Island|Minnesota|Wisconsin)\b', text)
    result['transportes'] = re.findall(r'\b(?:train|ship|ferry|bus)\b', text, re.IGNORECASE)
    result['dinero'] = re.findall(r'\$\d+|\btwenty dollars\b', text, re.IGNORECASE)
    return result

def parse_file(filepath: str, pid: str) -> Dict:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    info = parse_text(content)
    info['pid'] = pid
    info['archivo'] = filepath.split('/')[-1]
    return info
