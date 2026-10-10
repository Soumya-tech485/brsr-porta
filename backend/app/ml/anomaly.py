import numpy as np

def detect_anomalies_zscore(time_series: list[float], threshold: float = 3.0) -> list[int]:
    """
    Basic Z-Score anomaly detection.
    Returns a list of indices where an anomaly was detected.
    """
    if len(time_series) < 3:
        return []
        
    arr = np.array(time_series)
    mean = np.mean(arr)
    std = np.std(arr)
    
    if std == 0:
        return []
        
    z_scores = np.abs((arr - mean) / std)
    anomalous_indices = np.where(z_scores > threshold)[0]
    
    return list(anomalous_indices)
