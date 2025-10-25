"""
Interactive F1 Leaderboard Management System
Demonstrates modular design with menu-driven interface
"""

from leaderboard_core import Leaderboard
import os

# Global leaderboard instance
lb = Leaderboard()

def clear_screen():
    """Clear console for better UX"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print application header"""
    print("=" * 60)
    print("        F1 LEADERBOARD MANAGEMENT SYSTEM")
    print("=" * 60)
    print()

def module_1_add_driver():
    """Module 1: Insert driver information"""
    print("\n--- MODULE 1: ADD DRIVER ---")
    name = input("Enter driver code (3 letters, e.g., LEC): ").upper().strip()
    
    if len(name) != 3:
        print("Error: Driver code must be exactly 3 letters!")
        return
    
    if name in lb.driver_map:
        print(f"Warning: Driver {name} already exists!")
        choice = input("Update their gap time? (y/n): ").lower()
        if choice != 'y':
            return
    
    try:
        gap = float(input("Enter gap time (seconds, 0 for leader): "))
        if gap < 0:
            print("Error: Gap time cannot be negative!")
            return
        lb.update(name, gap)
        print(f"Success: Driver {name} added with gap: {gap:.3f}s")
    except ValueError:
        print("Error: Invalid gap time! Please enter a number.")

def module_2_update_lap_time():
    """Module 2: Update driver's lap/gap time"""
    print("\n--- MODULE 2: UPDATE LAP TIME ---")
    
    if not lb.driver_map:
        print("Warning: No drivers in the system. Add drivers first!")
        return
    
    print("\nCurrent drivers:")
    for name in sorted(lb.driver_map.keys()):
        print(f"  - {name}")
    
    name = input("\nEnter driver code to update: ").upper().strip()
    
    if name not in lb.driver_map:
        print(f"Error: Driver {name} not found!")
        return
    
    print(f"Current gap: {lb.driver_map[name]:.3f}s")
    
    try:
        new_gap = float(input("Enter new gap time (seconds): "))
        if new_gap < 0:
            print("Error: Gap time cannot be negative!")
            return
        
        old_rank = lb.get_rank(name)
        lb.update(name, new_gap)
        new_rank = lb.get_rank(name)
        
        print(f"Success: {name}'s gap updated to {new_gap:.3f}s")
        
        if old_rank is not None and new_rank is not None:
            if old_rank != new_rank:
                if new_rank < old_rank:
                    print(f"Position change: {name} moved UP from P{old_rank} to P{new_rank}")
                else:
                    print(f"Position change: {name} dropped from P{old_rank} to P{new_rank}")
            else:
                print(f"Position unchanged: P{new_rank}")
            
    except ValueError:
        print("Error: Invalid gap time! Please enter a number.")

def module_3_display_leaderboard():
    """Module 3: Display top 20 leaderboard"""
    print("\n--- MODULE 3: LEADERBOARD (TOP 20) ---")
    
    if not lb.driver_map:
        print("Warning: No drivers in the system yet!")
        return
    
    print()
    top_20 = lb.top_k(20)
    
    print(f"{'Pos':<5} {'Driver':<10} {'Gap':<12}")
    print("-" * 35)
    
    for rank, name, gap in top_20:
        gap_str = "Leader" if rank == 1 else f"+{gap:.3f}s"
        print(f"{rank:<5} {name:<10} {gap_str:<12}")
    
    total_drivers = len(lb.driver_map)
    if total_drivers > 20:
        print(f"\n... and {total_drivers - 20} more drivers")
    
    print(f"\nTotal drivers: {total_drivers}")

def module_4_remove_driver():
    """Module 4: Remove driver from leaderboard"""
    print("\n--- MODULE 4: REMOVE DRIVER ---")
    
    if not lb.driver_map:
        print("Warning: No drivers in the system!")
        return
    
    print("\nCurrent drivers:")
    for name in sorted(lb.driver_map.keys()):
        rank = lb.get_rank(name)
        gap = lb.driver_map[name]
        gap_str = "Leader" if rank == 1 else f"+{gap:.3f}s"
        print(f"  P{rank} - {name} ({gap_str})")
    
    name = input("\nEnter driver code to remove: ").upper().strip()
    
    if name not in lb.driver_map:
        print(f"Error: Driver {name} not found!")
        return
    
    confirm = input(f"Warning: Are you sure you want to remove {name}? (y/n): ").lower()
    if confirm != 'y':
        print("Removal cancelled.")
        return
    
    # Remove driver
    gap = lb.driver_map[name]
    idx = None
    for i, (g, n) in enumerate(lb.drivers):
        if n == name and g == gap:
            idx = i
            break
    
    if idx is not None:
        lb.drivers.pop(idx)
        del lb.driver_map[name]
        print(f"Success: Driver {name} removed successfully!")
    else:
        print("Error: Error removing driver")

def load_sample_data():
    """Load sample F1 data for testing"""
    sample_drivers = [
        ('LEC', 0.0), ('SAI', 11.850), ('VER', 12.252),
        ('PER', 14.777), ('BOT', 16.347), ('HAM', 18.481),
        ('GAS', 18.332), ('ALO', 20.359), ('NOR', 20.155),
        ('TSU', 20.570)
    ]
    
    for name, gap in sample_drivers:
        lb.update(name, gap)
    
    print("Success: Sample data loaded - 10 drivers")

def show_menu():
    """Display main menu"""
    print("\n" + "-" * 60)
    print("MENU OPTIONS:")
    print("-" * 60)
    print("  1. Add Driver")
    print("  2. Update Lap Time")
    print("  3. Display Leaderboard (Top 20)")
    print("  4. Remove Driver")
    print("  5. Load Sample Data")
    print("  6. Clear All Data")
    print("  0. Exit")
    print("-" * 60)

def main():
    """Main driver program"""
    clear_screen()
    print_header()
    print("Welcome to the F1 Leaderboard Management System!")
    print("This system demonstrates efficient data structure usage")
    print("for real-time leaderboard management.\n")
    
    while True:
        show_menu()
        choice = input("\nEnter your choice (0-6): ").strip()
        
        if choice == '1':
            module_1_add_driver()
        elif choice == '2':
            module_2_update_lap_time()
        elif choice == '3':
            module_3_display_leaderboard()
        elif choice == '4':
            module_4_remove_driver()
        elif choice == '5':
            load_sample_data()
        elif choice == '6':
            confirm = input("Warning: Clear all data? (y/n): ").lower()
            if confirm == 'y':
                lb.drivers.clear()
                lb.driver_map.clear()
                print("Success: All data cleared!")
        elif choice == '0':
            print("\n" + "=" * 60)
            print("Thank you for using F1 Leaderboard Management System!")
            print("=" * 60)
            break
        else:
            print("Error: Invalid choice! Please enter 0-6.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
