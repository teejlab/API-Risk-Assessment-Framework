from utils.pii_extraction import pii_extraction
from pytest import raises

def test_wrong_parameters():
    # Test if the function raises an error when the type is not a string
    with raises(TypeError):
        pii_extraction("raw_text", type=True, conf_threshold=0.5)

    # Test if the function raises an error when the type is not pii or fii
    with raises(ValueError):
        pii_extraction("raw_text", type="test", conf_threshold=0.5)

    # Test if the function raises an error when the confidence threshold is not a float or an int
    with raises(TypeError):
        pii_extraction("raw_text", type="pii", conf_threshold='123')

    # Test if the function raises an error when the confidence threshold is not between 0 and 1
    with raises(ValueError):
        pii_extraction("raw_text", type="pii", conf_threshold=-7)
        
    with raises(ValueError):
        pii_extraction("raw_text", type="pii", conf_threshold=100)
 
def test_normal_text():
    results = pii_extraction("raw_text", type="pii", conf_threshold=0.5)
    assert isinstance(
        results, list
    ), "A List should be returned."

def test_json():
    results = pii_extraction("{email:'abc@test.com'}", type="pii", conf_threshold=0.5)
    assert isinstance(
        results, list
    ), "A List should be returned."

def test_html():
    results = pii_extraction("<html><body>Test123</body></html>", type="pii", conf_threshold=0.5)
    assert isinstance(
        results, list
    ), "A List should be returned."
