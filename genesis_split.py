import math

PHI = (1 + math.sqrt(5)) / 2  # The Golden Ratio (approx. 1.618)

def genesis_split_resource(total_resource: float, num_splits: int):
    """
    Splits a total resource into segments based on the Golden Ratio (PHI).
    Each split uses PHI for one part and 1/PHI for the other, ensuring harmony.
    """
    if num_splits <= 0:
        return [total_resource]
    if total_resource <= 0:
        return []

    segments = []
    remaining_resource = total_resource

    print(f"--- Genesis Split of {total_resource} units into {num_splits} segments ---")
    print(f"PHI = {PHI:.3f}")

    for i in range(num_splits):
        # We'll create two parts: one PHI-proportion, one 1/PHI-proportion of the remaining
        # This can be interpreted in various ways for "splitting"
        # Let's define it as taking PHI's proportion as one segment, and (1-1/PHI) as the remainder
        
        # Part 1: PHI-proportional segment
        segment_size = remaining_resource / PHI
        segments.append(segment_size)
        remaining_resource -= segment_size
        
        print(f"Split {i+1}: Segment = {segment_size:.4f} units (PHI proportion), Remaining = {remaining_resource:.4f} units")

        # For the next iteration, the 'remaining_resource' becomes the new 'total'
        # to ensure the successive segments are also PHI-proportional to their 'parents'
        
        # Optional: You could also define it as taking the shorter segment (1/PHI proportion)
        # short_segment = remaining_resource / PHI**2
        # segments.append(short_segment)
        # remaining_resource -= short_segment
        # print(f"Split {i+1}: Short Segment = {short_segment:.4f}, Remaining = {remaining_resource:.4f}")

    # If there's any remaining resource after the last split, add it
    if remaining_resource > 0.0001: # Check for floating point precision
        segments.append(remaining_resource)
        print(f"Final segment (remainder) = {remaining_resource:.4f} units")

    print(f"Total segments generated: {len(segments)}")
    print(f"All segments: {[f'{s:.4f}' for s in segments]}")
    print(f"Sum of segments: {sum(segments):.4f}")
    
    return segments

# --- Example Usage ---
if __name__ == "__main__":
    print("\nExample 1: Splitting 100 units into 3 segments")
    genesis_split_resource(100, 3)

    print("\nExample 2: Splitting a single unit (e.g., a quantum of information) into 5 segments")
    genesis_split_resource(1.0, 5)

    print("\nExample 3: Splitting 144 (a Fibonacci number) units into 4 segments")
    genesis_split_resource(144, 4)
