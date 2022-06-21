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
    results : list
        A list containing the extracted PII.
    """
    # Check if the type is valid
    if not isinstance(type, str):
        raise TypeError("`type` should be a string")
    # Check if the type is valid
    if type != "pii" and type != "fii":
        raise ValueError("`type` should be either 'pii' or 'fii'")

    # Check if the confidence threshold is valid
    if not isinstance(conf_threshold, float) and not isinstance(conf_threshold, int):
        raise TypeError("`conf_threshold` should be either integer or float")
    # Check if the confidence threshold is between 0 and 1
    if conf_threshold < 0 or conf_threshold > 1:
        raise ValueError("`conf_threshold` should be between 0 and 1")

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
    # Base Case
    if not objs:
        return []
    if isinstance(objs, str):
        return _pii_extraction_from_text(objs, type, conf_threshold)
    
    filtered_results = []
    # Check if the object is a list
    if isinstance(objs, list):
        # Recursively call the function for each element in the list
        for obj in objs:
            filtered_results += _pii_extraction_from_json(obj, type, conf_threshold)
    # Check if the object is a dictionary
    elif isinstance(objs, dict):
        # Recursively call the function for each element in the dictionary
        for obj in objs.values():
            filtered_results += _pii_extraction_from_json(obj, type, conf_threshold)
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
