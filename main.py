import math

bins = []
history = []

def get_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def add_bin():
    print("\n--- Add New Bin ---")
    bin_id = input("Enter Bin ID: ").strip()
    if not bin_id:
        print("Bin ID cannot be empty.")
        return

    for b in bins:
        if b["id"].lower() == bin_id.lower():
            print("A bin with this ID already exists.")
            return

    try:
        x = float(input("Enter X coordinate: "))
        y = float(input("Enter Y coordinate: "))
        fill = float(input("Enter fill level (0-100): "))
    except ValueError:
        print("Invalid input. Coordinates and fill level must be numbers.")
        return

    if fill < 0 or fill > 100:
        print("Fill level must be between 0 and 100.")
        return

    bins.append({
        "id": bin_id,
        "x": x,
        "y": y,
        "fill": fill
    })
    print(f"Bin {bin_id} added successfully.")
    if fill >= 100:
        print(f"[ALERT] Bin {bin_id} is overflowing (100% full)!")

def update_fill_level():
    print("\n--- Update Bin Fill Level ---")
    if not bins:
        print("No bins in the system yet.")
        return

    bin_id = input("Enter Bin ID to update: ").strip()
    for b in bins:
        if b["id"].lower() == bin_id.lower():
            try:
                new_fill = float(input(f"Enter new fill level for {b['id']} (0-100): "))
            except ValueError:
                print("Invalid input. Please enter a number.")
                return

            if new_fill < 0 or new_fill > 100:
                print("Fill level must be between 0 and 100.")
                return

            b["fill"] = new_fill
            print(f"Updated {b['id']} fill level to {new_fill}%.")
            if new_fill >= 100:
                print(f"[ALERT] Bin {b['id']} is overflowing!")
            return

    print("Bin ID not found.")

def list_priority_bins():
    print("\n--- Priority Bins (> 75% Full) ---")
    if not bins:
        print("No bins recorded yet.")
        return []

    priority = []
    for b in bins:
        if b["fill"] > 75:
            status = " [OVERFLOWING!]" if b["fill"] >= 100 else ""
            print(f"ID: {b['id']} | Location: ({b['x']}, {b['y']}) | Fill: {b['fill']}%{status}")
            priority.append(b)

    if not priority:
        print("No bins are currently above 75% full.")

    return priority

def generate_route():
    print("\n--- Collection Route Planner ---")
    if not bins:
        print("No bins recorded yet.")
        return

    # Check for overflowing bins and filter bins > 75%
    unvisited = []
    for b in bins:
        if b["fill"] >= 100:
            print(f"[ALERT] Bin {b['id']} at ({b['x']}, {b['y']}) is overflowing!")
        if b["fill"] > 75:
            unvisited.append(b.copy())

    if not unvisited:
        print("All bins are at 75% or below. No collection needed right now.")
        return

    print(f"\nBins needing collection ({len(unvisited)}):")
    for b in unvisited:
        print(f" - {b['id']} ({b['fill']}% full) at ({b['x']}, {b['y']})")

    # Calculate fixed route distance (visiting every recorded bin in order)
    fixed_dist = 0.0
    cx, cy = 0.0, 0.0
    for b in bins:
        fixed_dist += get_distance(cx, cy, b["x"], b["y"])
        cx, cy = b["x"], b["y"]

    # Nearest-neighbour routing starting from depot (0, 0)
    curr_x, curr_y = 0.0, 0.0
    route_dist = 0.0
    route_order = []

    while len(unvisited) > 0:
        nearest = unvisited[0]
        min_d = get_distance(curr_x, curr_y, nearest["x"], nearest["y"])

        for b in unvisited[1:]:
            d = get_distance(curr_x, curr_y, b["x"], b["y"])
            if d < min_d:
                min_d = d
                nearest = b

        route_dist += min_d
        curr_x, curr_y = nearest["x"], nearest["y"]
        route_order.append(nearest["id"])
        unvisited.remove(nearest)

    saved_dist = fixed_dist - route_dist

    print("\nOptimized Route:")
    print("Depot (0,0) -> " + " -> ".join(route_order))
    print(f"Fixed Route Distance (All Bins): {fixed_dist:.2f} units")
    print(f"Optimized Route Distance:        {route_dist:.2f} units")
    print(f"Total Distance Saved:            {saved_dist:.2f} units")

    record = f"Collected {len(route_order)} bins ({', '.join(route_order)}) | Dist: {route_dist:.2f} | Saved: {saved_dist:.2f}"
    history.append(record)

    with open("route_history.txt", "a") as f:
        f.write(record + "\n")

def show_history():
    print("\n--- Collection History ---")
    if not history:
        print("No collection runs recorded in this session.")
        return

    for i in range(len(history)):
        print(f"{i + 1}. {history[i]}")

def load_sample_bins():
    sample = [
        {"id": "B01", "x": 10.0, "y": 10.0, "fill": 80.0},
        {"id": "B02", "x": 2.0, "y": 2.0, "fill": 100.0},
        {"id": "B03", "x": 50.0, "y": 50.0, "fill": 40.0},
        {"id": "B04", "x": 5.0, "y": 5.0, "fill": 90.0},
        {"id": "B05", "x": 15.0, "y": 15.0, "fill": 70.0}
    ]
    added = 0
    for s in sample:
        exists = False
        for b in bins:
            if b["id"].lower() == s["id"].lower():
                exists = True
                break
        if not exists:
            bins.append(s)
            added += 1
    print(f"\nLoaded {added} sample bins.")

def main():
    while True:
        print("\n=== BinSense: Waste Monitoring & Route Planner ===")
        print("1. Add Bin")
        print("2. Update Fill Level")
        print("3. List Bins Above 75% Full")
        print("4. Build Collection Route")
        print("5. View Collection History")
        print("6. Load Sample Data")
        print("7. Exit")

        choice = input("Enter choice (1-7): ").strip()

        if choice == "1":
            add_bin()
        elif choice == "2":
            update_fill_level()
        elif choice == "3":
            list_priority_bins()
        elif choice == "4":
            generate_route()
        elif choice == "5":
            show_history()
        elif choice == "6":
            load_sample_bins()
        elif choice == "7":
            print("Exiting program.")
            break
        else:
            print("Invalid option. Please enter a number between 1 and 7.")

if __name__ == "__main__":
    main()