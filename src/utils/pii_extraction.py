from presidio_analyzer import AnalyzerEngine
from bs4 import BeautifulSoup
import json

# Set up the engine, loads the NLP module (spaCy model by default)
# and other PII recognizers
analyzer = AnalyzerEngine()
pii = [
    "PERSON",
    "LOCATION",
    "NRP",
    "EMAIL_ADDRESS",
    "MEDICAL_LICENSE",
    "IP_ADDRESS",
]
fii = ["CREDIT_CARD", "CRYPTO", "IBAN_CODE", "US_BANK_NUMBER", "US_ITIN", "US_SSN"]

def pii_extraction(text, type="pii", conf_threshold=0.5):
    """
    Extracts PII from a text.
    Parameters
    ----------
    text : str
        The text to be analyzed.
    type : str
        The type of PII to be extracted.
    conf_threshold : float
        The confidence threshold.
    Returns
    -------
    filtered_results : list
        A list containing the extracted PII.
    """
    results = []
    text = str(text)
    # Check if the text is html or xml
    if bool(BeautifulSoup(text, "html.parser").find()):
        html = BeautifulSoup(text, "html.parser").text
        results += _pii_extraction_from_text(html, type, conf_threshold)
    # Check if the text is json
    elif _validateJSON(text):
        texts = json.loads(text)
        results += _pii_extraction_from_json(texts, type, conf_threshold)
    # Check if the text is plain text
    else:
        results += _pii_extraction_from_text(text, type, conf_threshold)
    return results

def _pii_extraction_from_text(text, type="pii", conf_threshold=0.5):
    """
    Extracts PII from a text.
    Parameters
    ----------
    text : str
        The text to be analyzed.
    type : str
        The type of PII to be extracted.
    conf_threshold : float
        The confidence threshold.
    Returns
    -------
    filtered_results : list
        A list containing the extracted PII.
    """
    filtered_results = []

    if type == "pii":
        results = analyzer.analyze(text=text, entities=pii, language="en")
    else:
        results = analyzer.analyze(text=text, entities=fii, language="en")

    for result in results:
        if result.score >= conf_threshold:
            filtered_results.append(result)
            
    return filtered_results


def _pii_extraction_from_json(objs, type="pii", conf_threshold=0.5):
    """
    Extracts PII from a json.
    Parameters
    ----------
    objs : list
        The json to be analyzed.
    type : str 
        The type of PII to be extracted.
    conf_threshold : float
        The confidence threshold.
    Returns
    -------
    filtered_results : list
        A list containing the extracted PII.
    """
    filtered_results = []
    # Check if the object is a list
    if isinstance(objs, list):
        # Recursively call the function for each element in the list
        for obj in objs:
            filtered_results += _pii_extraction_from_json(obj, type, conf_threshold)
    # Check if the object is a dictionary
    elif isinstance(objs, dict):
        for obj in objs.values():
            # For list type
            if isinstance(obj, list):
                for item in obj:
                    filtered_results += _pii_extraction_from_text(str(item), type, conf_threshold)
            # For string type
            else:
                filtered_results += _pii_extraction_from_text(str(obj), type, conf_threshold)
    else:
        filtered_results += _pii_extraction_from_text(str(objs), type, conf_threshold)
    return filtered_results


def _validateJSON(jsonData):
    """
    Validates the JSON data.
    Parameters
    ----------
    jsonData : str
        The JSON data to be validated.
    Returns
    -------
    valid : bool
        True if the JSON data is valid, False otherwise.
    """
    try:
        json.loads(jsonData)
    except ValueError as err:
        return False
    return True