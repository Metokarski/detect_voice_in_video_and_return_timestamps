import csv
import os

def save_timestamps_to_csv(timestamps, output_path):
    """
    Saves a list of timestamps to a CSV file.

    Args:
        timestamps (list): A list of (start, end) tuples.
        output_path (str): The path to save the output CSV file.
    """
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['start_time', 'end_time'])
            writer.writerows(timestamps)
        print(f"Timestamps saved to {output_path}")
    except Exception as e:
        print(f"Error saving timestamps to CSV: {e}")
        raise

def merge_segments(segments, max_gap=0.5):
    """
    Merges adjacent or overlapping segments.

    Args:
        segments (list): A list of (start, end) tuples.
        max_gap (float): The maximum gap between segments to merge.

    Returns:
        list: A list of merged (start, end) tuples.
    """
    if not segments:
        return []

    segments.sort(key=lambda x: x[0])
    merged = []
    current_start, current_end = segments[0]

    for next_start, next_end in segments[1:]:
        if next_start <= current_end + max_gap:
            current_end = max(current_end, next_end)
        else:
            merged.append((current_start, current_end))
            current_start, current_end = next_start, next_end
    
    merged.append((current_start, current_end))
    return merged
