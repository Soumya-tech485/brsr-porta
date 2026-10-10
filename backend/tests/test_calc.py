import pytest
from app.services.calc_engine import calc_ltifr

def test_no_averaging_ratios():
    """
    Test explicitly proves that averaging ratios gives a mathematically wrong result 
    compared to recalculating from consolidated sums (MASTER PROMPT requirement).
    """
    # Site A: 1 injury, 10,000 hours -> LTIFR = 100
    ltifr_a = calc_ltifr(1, 10000)
    assert ltifr_a == 100.0
    
    # Site B: 3 injuries, 100,000 hours -> LTIFR = 30
    ltifr_b = calc_ltifr(3, 100000)
    assert ltifr_b == 30.0
    
    # Incorrect method: Averaging the ratios directly
    average_ltifr = (ltifr_a + ltifr_b) / 2
    assert average_ltifr == 65.0
    
    # Correct method: Consolidation of components, then ratio calculation
    total_injuries = 1 + 3
    total_hours = 10000 + 100000
    correct_ltifr = calc_ltifr(total_injuries, total_hours)
    
    # Correct LTIFR is 36.36, not 65.0!
    assert round(correct_ltifr, 2) == 36.36
    assert correct_ltifr != average_ltifr
