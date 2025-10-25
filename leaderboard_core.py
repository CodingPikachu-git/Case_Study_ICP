from bisect import insort, bisect_left
from typing import List, Tuple, Optional

class Leaderboard:
    """
    Efficient leaderboard using sorted list and hash map.
    Time Complexity:
    - update: O(log n)
    - get_rank: O(log n)
    - top_k: O(k)
    """
    def __init__(self):
        self.drivers = []  # List of (gap, name) tuples, kept sorted
        self.driver_map = {}   # name -> gap mapping for O(1) lookup
    
    def update(self, name: str, gap: float) -> None:
        """Update driver's gap time."""
        # Remove old entry if exists
        if name in self.driver_map:
            old_gap = self.driver_map[name]
            idx = bisect_left(self.drivers, (old_gap, name))
            self.drivers.pop(idx)
        
        # Insert new entry (maintains sorted order)
        insort(self.drivers, (gap, name))
        self.driver_map[name] = gap
    
    def get_rank(self, name: str) -> Optional[int]:
        """Get current rank of a driver (1-indexed)."""
        if name not in self.driver_map:
            return None
        gap = self.driver_map[name]
        idx = bisect_left(self.drivers, (gap, name))
        return idx + 1
    
    def top_k(self, k: int) -> List[Tuple[int, str, float]]:
        """Get top K drivers."""
        result = []
        for i, (gap, name) in enumerate(self.drivers[:k]):
            result.append((i+1, name, gap))
        return result
    
    def display(self) -> None:
        """Pretty print leaderboard."""
        print(f"{'Rank':<6} {'Name':<8} {'Gap':<10}")
        print("-" * 30)
        for i, (gap, name) in enumerate(self.drivers):
            gap_str = "Leader" if i == 0 else f"+{gap:.3f}"
            print(f"{i+1:<6} {name:<8} {gap_str:<10}")

# Demo usage - THIS RUNS AUTOMATICALLY
if __name__ == "__main__":
    print("=== LEADERBOARD DEMO ===\n")
    
    lb = Leaderboard()
    
    # Initial standings
    drivers = [
        ('LEC', 0.0),
        ('SAI', 11.850),
        ('VER', 12.252),
        ('PER', 14.777),
        ('BOT', 16.347)
    ]
    
    print("Initial Leaderboard:")
    for name, gap in drivers:
        lb.update(name, gap)
    lb.display()
    
    print("\n--- Simulating overtake: VER passes SAI ---")
    lb.update('VER', 11.500)
    lb.display()
    
    print(f"\nVER's rank: {lb.get_rank('VER')}")
    print(f"\nTop 3: {lb.top_k(3)}")
