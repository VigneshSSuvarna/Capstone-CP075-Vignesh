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
    
    bins_to_collect = []
    for b in bins_database:
        if b["fill_level"] >= 100:
            print(f"⚠️ WARNING: Bin {b['id']} is OVERFLOWING!")
        if b["fill_level"] > 75:
            bins_to_collect.append(b.copy())
            
    if not bins_to_collect:
        print("No collection needed today.") # Edge Case handled
        return
        
    # --- NEW: Calculate Unoptimized (Sequential) Distance ---
    seq_dist = 0.0
    curr_x, curr_y = 0.0, 0.0
    for b in bins_to_collect:
        seq_dist += math.sqrt((b["x"] - curr_x)**2 + (b["y"] - curr_y)**2)
        curr_x, curr_y = b["x"], b["y"]

    # Nearest-Neighbor Routing
    current_x, current_y = 0.0, 0.0
    optimized_dist = 0.0 # NEW: Track total optimized distance
    route = []
    
    while bins_to_collect:
        nearest_bin = None
        min_dist = float('inf')
        
        for b in bins_to_collect:
            dist = math.sqrt((b["x"] - current_x)**2 + (b["y"] - current_y)**2)
            if dist < min_dist:  # Edge Case: The < operator naturally breaks ties by picking the first one found
                min_dist = dist
                nearest_bin = b
        
        optimized_dist += min_dist # Add leg distance
        route.append(nearest_bin["id"])
        current_x, current_y = nearest_bin["x"], nearest_bin["y"]
        bins_to_collect.remove(nearest_bin)
        
    print("\n📍 Optimized Collection Route:")
    print("Depot -> " + " -> ".join(route))
    
    # --- NEW: Print Distance Saved ---
    distance_saved = seq_dist - optimized_dist
    print(f"\n📊 Route Analytics:")
    print(f"Standard Distance: {seq_dist:.2f} units")
    print(f"Optimized Distance: {optimized_dist:.2f} units")
    print(f"Distance Saved: {distance_saved:.2f} units")
    
    # --- NEW: File Saving ---
    log_entry = f"Collection for {len(route)} bins: {', '.join(route)} | Distance: {optimized_dist:.2f}"
    collection_history.append(log_entry)
    
    # Write to external file
    with open("route_history.txt", "a") as file:
        file.write(log_entry + "\n")
        
    print(f"\n[System Log] Saved to route_history.txt")
    
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

def load_demo_data():
    demo_bins = [
        {"id": "D01", "x": 10.0, "y": 10.0, "fill_level": 80.0},
        {"id": "D02", "x": 2.0, "y": 2.0, "fill_level": 100.0},
        {"id": "D03", "x": 50.0, "y": 50.0, "fill_level": 40.0},
        {"id": "D04", "x": 5.0, "y": 5.0, "fill_level": 90.0},
        {"id": "D05", "x": 15.0, "y": 15.0, "fill_level": 70.0} # Will update to 80 during demo
    ]
    bins_database.extend(demo_bins)
    print("\n[Demo Data Loaded] 5 bins added to the system.")

def main():
    while True:
        print("\n=== BinSense Route Planner ===")
        print("1. Add a New Bin")
        print("2. Update Fill Level ")
        print("3. View Route ")
        print("4. View Collection History")
        print("5. Exit")
        print("6. Load Demo Data ")
        
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
        elif choice == '6':
            load_demo_data()
        else:
            print("\nInvalid choice. Please select 1-6.")

# This ensures the script runs when executed directly
if __name__ == "__main__":
    main()
