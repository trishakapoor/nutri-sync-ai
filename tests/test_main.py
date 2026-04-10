from backend.main import calculate_bmi

def test_bmi_logic():
    # Test for accuracy
    result = calculate_bmi(70, 1.75)
    assert round(result, 2) == 22.86

def test_high_bmi_threshold():
    # Test for safety logic trigger
    weight = 100
    height = 1.6
    bmi = calculate_bmi(weight, height)
    assert bmi > 25
