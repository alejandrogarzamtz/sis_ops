
import re
from typing import Dict

categorias = {
    "Nombres": ["Conrad Reinell", "Jack Penny", "Martin Luther", "Parker", "Michael", "Arl", "Axel", "Otto",
        "Jenny", "Delia", "Daniel Lindin/Linden", "Billy", "Joel Jernberg", "Esther", "Anaïs",
        "Gustav", "Stina", "Greta", "Harold Lodge", "Curtis Carlson", "Nelson", "Harry West",
        "Charles", "Carl Olsson", "Oscar Leonard Peterson", "Inez", "Herman Hallström",
        "Alf Hallström", "Blum", "Rudy Perp", "Holmstrom", "Britta", "Solom", "Ellen", "Cui",
        "Sveth Svarendal", "Elvira", "Andrew"],
    "Paises": ["United States", "New York", "Sweden", "Canada", "America", "Belgium", "Germany", "Poland"],
    "Fechas_con_Formato": ["1st of May", "May the 1st", "10 de septiembre 1985", "second October 1987",
        "1915, 17th of October", "24th of October"],
    "Razones_Inmigracion": ["the quota, every country had a quota in those days",
        "they were going to come to America when he was 16 years of age...",
        "he did not want to be drafted",
        "they went there to work because there was work there",
        "There's no future over there much for boys and a girl"],
    "Niveles_Educacion": ["school", "high school", "college", "kindergarten"],
    "Escuelas_Mencionadas": ["Swedish school", "John Nelson School", "National College in Evanston",
        "Catholic school", "public school", "Pec school", "Drake University",
        "St. Catherine's in Davenport", "P.A. Peterson School"],
    "Lenguajes_Hablados": ["Swedish", "English", "Italian", "Polish", "German", "Norwegian", "Danish", "Spanish"],
    "Eventos_Historicos": ["Prohibition", "World War II", "Vietnam War", "the settlement", "Revolutionary times",
        "the depression", "Black Wednesday", "Dust Bowl", "the first world war", "Aquitennial",
        "Springfield Annual Meetings"],
    "Ocupaciones": ["pastor", "conductor", "tailor", "street cleaners", "boss over all the streets",
        "carpenter foreman", "workers", "agronomist", "farmer", "butcher", "slagfaktorist",
        "seed corn examiner", "foreman", "wood room worker", "paper mill worker", "hog feeder",
        "knives changer", "barking machines operator", "silage cutter", "engineer",
        "civil engineer", "county engineer", "office Signal Company worker", "machinery builder",
        "tool maker", "operator", "accountant", "typist", "secretary", "superintendent",
        "president", "financial advisor", "chairman of the board", "unionites",
        "engineering department worker", "pieceworker", "timer", "stock hauler", "cook",
        "cowboy", "cattle man", "branding cattle worker", "bricklayer", "mail carrier", "consul"],
    "Practicas_Culturales": ["soccer", "having a Swedish-American newspaper", "speaking Swedish at home",
        "celebrate on Christmas Eve", "the church service", "CPR", "mouth-to-mouth resuscitation",
        "dancing", "singing", "having family reunions"],
    "Destinos": ["Minneapolis, Iowa", "United States", "New York", "Göteborg", "Ellis Island", "Chicago",
        "Carolina", "Washington", "South", "Southeast", "Canada", "Buffalo", "Pontiac", "Detroit",
        "Duluth", "River Island", "Sweden", "Oakland, California", "San Francisco", "Boston",
        "St. Clair Shores", "Omaha", "Rockford", "Bangkok", "Wenatchee, Washington", "Seattle",
        "Lake Geneva", "Los Angeles", "Palm Springs", "Germany", "Lewistown", "Rockport",
        "California", "Iowa", "Stettin, Pomerania"],
    "Puertos_de_Entrada": ["New York", "Ellis Island"],
    "Fechas_de_Emigracion": ["1st of May", "the month of May", "2-3 months", "1921", "1927", "1910", "1887"],
    "Modos_de_Viaje": ["ships", "railroad cars", "trains", "bus", "ferry", "car"],
    "Afiliaciones_Iglesia": ["Lutheran", "Augustan church", "Bunker Hill Congregational Church", "Catholic Church",
        "Trinity Church", "Augustana Synod", "LCA", "ULC", "ELCA", "Pentecostal",
        "Assembly of God", "Swedish Methodist Church", "Mission Covenant Church", "Bethany Baptist"],
    "Problemas_de_Salud": ["feet froze", "amputate his feet", "examined your muscles", "Look in your eyes...",
        "sugar diabetes", "pain in my spine", "psychological breakdown", "cabin fever", "Parkinsonian",
        "cleft palates", "hair-lip"],
    "Ubicaciones_Geograficas": ["Minneapolis, Iowa", "United States", "New York", "Göteborg", "Ellis Island",
        "Chicago", "Carolina", "Washington", "South", "Southeast", "Canada", "Buffalo", "Pontiac",
        "Detroit", "Duluth", "River Island", "Sweden", "Oakland, California", "San Francisco",
        "Boston", "St. Clair Shores", "Omaha", "Rockford", "Lake Geneva", "Palm Springs",
        "Germany", "Lewistown", "Rockport", "California", "Iowa", "Stettin, Pomerania"],
    "Años_de_Graduacion": ["1985"],
    "Causas_de_Muerte": ["died"],
    "Empleadores": ["U.S. Steel", "International Harvester", "Ford Plant", "Office Signal Company",
        "Oscar Leonard Peterson contracting business"],
    "Titulos_de_Trabajo": ["pastor", "conductor", "tailor", "street cleaners", "boss over all the streets",
        "carpenter foreman", "agronomist", "butcher", "slagfaktorist", "seed corn examiner",
        "foreman", "wood room worker", "paper mill worker", "hog feeder", "knives changer",
        "barking machines operator", "silage cutter", "engineer", "civil engineer", "county engineer",
        "office Signal Company worker", "machinery builder", "tool maker", "operator", "accountant",
        "typist", "secretary", "superintendent", "president", "financial advisor",
        "chairman of the board", "unionites", "engineering department worker", "pieceworker",
        "timer", "stock hauler", "cook", "cowboy", "cattle man", "branding cattle worker",
        "bricklayer", "mail carrier", "consul"],
    "Participacion_Comunitaria": ["Springfield Annual Meetings", "the church service", "Sunday school",
        "Swedish Mission Sunday school", "Drake League Club", "family reunions", "Aquitennial"],
    "Actividades_Sociales": ["soccer", "dancing", "singing", "having family reunions", "Aquitennial", "church service"]
}

def parse_text(text: str) -> Dict:
    result = {}
    for categoria, valores in categorias.items():
        encontrados = []
        for valor in valores:
            if valor.lower() in text.lower():
                encontrados.append(valor)
        result[categoria] = ", ".join(encontrados) if encontrados else "no mencionado"
    return result

def parse_file(filepath: str, pid: str) -> Dict:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return {"pid": pid, "archivo": filepath.split('/')[-1], "error": str(e)}

    info = parse_text(content)
    info['pid'] = pid
    info['archivo'] = filepath.split('/')[-1]
    return info

