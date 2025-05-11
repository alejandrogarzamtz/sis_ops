import re
from typing import Dict

def parse_text(text: str) -> Dict:
    result = {}
  
    result['fechas'] = re.findall(r'\b\d{4}-\d{2}-\d{2}\b|\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b', text)
    
  
    result['nombres'] = re.findall(r'\b[A-Z][a-z]+\s[A-Z][a-z]+(?:\s[A-Z][a-z]+)*\b', text) # Permitir más de un apellido

  
    result['palabras_suecas'] = re.findall(r'\b(?:Göteborg|Drottningholm|Kungsholm|Fritidsbeteget|Utvandlingsbeteget)\b', text, re.IGNORECASE) 

   
    result['lugares'] = re.findall(r'\b(?:New York|Chicago|Buffalo|Ellis Island|Minnesota|Wisconsin)\b', text, re.IGNORECASE) 

    # Transportes
    result['transportes'] = re.findall(r'\b(?:train|ship|ferry|bus|car|airplane|boat)\b', text, re.IGNORECASE) 

   
    result['dinero'] = re.findall(r'\$\s*\d+(?:\.\d{2})?|\b(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|thousand)?\s*dollars?\b', text, re.IGNORECASE) #


    result['correos'] = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', text)

    result['direcciones'] = re.findall(
        r'\b(?:[A-Z][a-zäöüßáéíóúñ\s]+)(?:Street|St|Road|Rd|Avenue|Av|Ave|Boulevard|Blvd|Drive|Dr|Lane|Ln|Court|Ct)\.?\s+\d+\b(?:,\s*[A-Z][a-zA-Z\s]+)?',
        text,
        re.IGNORECASE
    )




    result['hashtags'] = re.findall(r'#\w+', text)

 
    for key, value in result.items():
        if not value:
            result[key] = "N/A" 
        elif isinstance(value, list):
            result[key] = ", ".join(value) 
    return result

def parse_file(filepath: str, pid: str) -> Dict:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
       
        error_info = {key: "Archivo no encontrado" for key in ["fechas", "nombres", "palabras_suecas", "lugares", "transportes", "dinero", "correos", "direcciones", "hashtags"]}
        error_info['pid'] = pid
        error_info['archivo'] = filepath.split('/')[-1] if filepath else "Desconocido"
        return error_info
    except Exception as e:
  
        error_info = {key: f"Error al leer archivo: {e}" for key in ["fechas", "nombres", "palabras_suecas", "lugares", "transportes", "dinero", "correos", "direcciones", "hashtags"]}
        error_info['pid'] = pid
        error_info['archivo'] = filepath.split('/')[-1] if filepath else "Desconocido"
        return error_info

    info = parse_text(content)
    info['pid'] = pid
    info['archivo'] = filepath.split('/')[-1] if filepath else "Desconocido"
    return info
