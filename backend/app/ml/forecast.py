import numpy as np

def forecast_run_rate(time_series: list[float], months_elapsed: int) -> float:
    """
    Forecast the year-end total using a simple run-rate.
    (Sum to date / months_elapsed) * 12
    """
    if months_elapsed <= 0 or months_elapsed > 12:
        return 0.0
        
    current_total = sum(time_series)
    return (current_total / months_elapsed) * 12
