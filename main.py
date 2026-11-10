import math

collection_history = []

bins_database = []

def add_bin():
    print("\n--- Add a New Bin ---")
    try:
        bin_id = input("Enter Bin ID (e.g., B01): ")
        for b in bins_database:
            if b["id"] == bin_id:
                print("Error: A bin with this ID already exists.")
                return
        
        loc_x = float(input("Enter Location X coordinate: "))
        loc_y = float(input("Enter Location Y coordinate: "))
        fill_level = float(input("Enter Fill Level (0-100): "))
        
        # Ensure fill level is within valid bounds
        if fill_level < 0 or fill_level > 100:
            print("Error: Fill level must be between 0 and 100.")
            return

        # Create the dictionary and add it to our list
        new_bin = {
            "id": bin_id,
            "x": loc_x,
            "y": loc_y,
            "fill_level": fill_level
        }
        
        bins_database.append(new_bin)
        print(f"Success! Bin {bin_id} added.")
        
    except ValueError:
        print("Invalid input! Coordinates and fill level must be numbers.")

def update_bin():
    print("\n--- Update Bin Fill Level ---")
    
    # Check if database is empty
    if not bins_database:
        print("No bins recorded yet. Please add a bin first.")
        return

    target_id = input("Enter Bin ID to update: ")
    
    # Search for the bin
    for b in bins_database:
        if b["id"] == target_id:
            try:
                new_fill = float(input(f"Enter new fill level for {target_id} (0-100): "))
                
                # Validate bounds
                if new_fill < 0 or new_fill > 100:
                    print("Error: Fill level must be between 0 and 100.")
                    return
                
                # Update the value
                b["fill_level"] = new_fill
                print(f"Success! Bin {target_id} updated to {new_fill}%.")
                return
                
            except ValueError:
                print("Invalid input! Fill level must be a number.")
                return
    
    # If the loop finishes without returning, the ID wasn't found
    print(f"Error: Bin ID '{target_id}' not found.")

def view_route():
    print("\n--- Route Planning & Alerts ---")
    
    # 1. Feature 3 & 5: Filter bins > 75% and trigger alerts
    bins_to_collect = []
    for b in bins_database:
        if b["fill_level"] >= 100:
            print(f"⚠️ WARNING: Bin {b['id']} is OVERFLOWING!")
            
        if b["fill_level"] > 75:
            bins_to_collect.append(b.copy()) # Copy to safely remove items later
            
    if not bins_to_collect:
        print("No bins currently require collection.")
        return
        
    print(f"\nBins requiring collection: {[b['id'] for b in bins_to_collect]}")
    
    # 2. Feature 4: Nearest-Neighbor Routing
    current_x, current_y = 0.0, 0.0 # Starting at the Depot
    route = []
    
    while bins_to_collect:
        nearest_bin = None
        min_dist = float('inf')
        
        for b in bins_to_collect:
            # Euclidean distance formula
            dist = math.sqrt((b["x"] - current_x)**2 + (b["y"] - current_y)**2)
            if dist < min_dist:
                min_dist = dist
                nearest_bin = b
        
        # Move truck to nearest bin
        route.append(nearest_bin["id"])
        current_x, current_y = nearest_bin["x"], nearest_bin["y"]
        bins_to_collect.remove(nearest_bin)
        
    print("\n📍 Optimized Collection Route:")
    print("Depot -> " + " -> ".join(route))
    
    # 3. Feature 5: Update Collection History
    log_entry = f"Collection run initiated for {len(route)} bins: {', '.join(route)}"
    collection_history.append(log_entry)
    print(f"\n[System Log] {log_entry}")

def main():
    while True:
        print("\n=== BinSense Route Planner ===")
        print("1. Add a New Bin")
        print("2. Update Fill Level ")
        print("3. View Route (Coming Soon)")
        print("4. View Collection History")
        print("5. Exit")
        
        choice = input("Select an option (1-5): ")
        
        if choice == '1':
            add_bin()
        elif choice == '2':
            update_bin()
        elif choice == '3':
            view_route()
        elif choice == '4':
            print("\n--- Collection History ---")
            if not collection_history:
                print("No collections run yet.")
            else:
                for log in collection_history:
                    print(f"- {log}")
        elif choice == '5':
            print("\nExiting BinSense. Goodbye!")
            break
        else:
            print("\nInvalid choice. Please select 1-5.")

# This ensures the script runs when executed directly
if __name__ == "__main__":
    main()
