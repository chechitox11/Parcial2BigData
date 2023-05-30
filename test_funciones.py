from consumidor1 import lower_band
from unittest.mock import patch

precio = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220]

def test_lower_band1():
    with patch('statistics.stdev') as mock_stdev:
        mock_stdev.return_value = 10.0
        expected_result = 105.0
        actual_result = lower_band(precio)
        assert actual_result == expected_result
        
def test_lower_band2():
    with patch('statistics.stdev') as mock_stdev:
        mock_stdev.return_value = 20.0
        expected_result = 85.0
        actual_result = lower_band(precio)
        assert actual_result == expected_result

def test_lower_band3():
    with patch('statistics.stdev') as mock_stdev:
        mock_stdev.return_value = 50.0
        expected_result = 25.0
        actual_result = lower_band(precio)
        assert actual_result == expected_result
