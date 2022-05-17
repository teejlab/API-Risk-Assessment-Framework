from presidio_analyzer import AnalyzerEngine

# Set up the engine, loads the NLP module (spaCy model by default)
# and other PII recognizers
analyzer = AnalyzerEngine()
pii = [
    "PERSON",
    "LOCATION",
    "NRP",
    "EMAIL_ADDRESS",
    "MEDICAL_LICENSE",
    "MEDICAL_LICENSE",
    "IP_ADDRESS",
]
fii = ["CREDIT_CARD", "CRYPTO", "IBAN_CODE", "US_BANK_NUMBER", "US_ITIN", "US_SSN"]


def pii_extraction(text, conf_threshold=0.5):
    """
    Extracts PII from a text.
    Parameters
    ----------
    text : str
        The text to be analyzed.
    conf_threshold : float
        The confidence threshold.
    Returns
    -------
    filtered_results : dict
        A dictionary containing the extracted PII.
    """
    text = str(text)
    filtered_results = []
    results = analyzer.analyze(text=text, entities=pii, language="en")
    for result in results:
        if result.score >= conf_threshold:
            filtered_results.append(result)
    return filtered_results


def fii_extraction(text, conf_threshold=0.5):
    """
    Extracts FII from a text.
    Parameters
    ----------
    text : str
        The text to be analyzed.
    conf_threshold : float
        The confidence threshold.
    Returns
    -------
    filtered_results : dict
        A dictionary containing the extracted FII.
    """
    text = str(text)
    filtered_results = []
    results = analyzer.analyze(text=text, entities=fii, language="en")
    for result in results:
        if result.score >= conf_threshold:
            filtered_results.append(result)
    return filtered_results
