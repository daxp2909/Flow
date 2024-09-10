import numpy as np

# Traffic simulation class
class TrafficSimulation:
    def __init__(self, distances, speeds, volumes, green_times, emergencies, accidents):
        self.distances = distances  # Distance between signals
        self.speeds = speeds  # Speed of vehicles
        self.volumes = volumes  # Traffic volume at each signal
        self.green_times = green_times  # Current green times at signals
        self.emergencies = emergencies  # List of emergency cases (indices)
        self.accidents = accidents  # List of accident cases (indices)
        self.rating = 0  # Simulation rating (1-10)

    def simulate(self):
        flow = []
        num_signals = len(self.distances)

        for i in range(num_signals):
            try:
                # Check if there is an accident or emergency at this signal
                if i in self.accidents:
                    flow.append(0)  # Traffic is blocked due to an accident
                    continue
                if i in self.emergencies:
                    flow.append(5)  # Reduced flow due to an emergency
                    continue

                # Calculate travel time between signals
                travel_time = self.distances[i] / self.speeds[i]
                # Compare travel time with green light duration
                if travel_time <= self.green_times[i]:
                    flow.append(10)  # Smooth flow
                else:
                    flow.append(max(1, 10 - (travel_time - self.green_times[i])))
            except ZeroDivisionError:
                print(f"Warning: Speed cannot be zero. Skipping signal index {i}.")
                flow.append(0)

        # Check if flow is empty before calculating mean
        if flow:
            self.rating = np.mean(flow)
        else:
            print("Warning: No valid flow data to calculate the rating.")
            self.rating = 0

        return self.rating

# Function to calculate green times
def calculate_green_times(distances, speeds, volumes):
    green_times = []
    for distance, speed, volume in zip(distances, speeds, volumes):
        if speed == 0:
            print(f"Warning: Speed cannot be zero for distance {distance}.")
            green_times.append(0)
        else:
            travel_time = distance / speed
            volume_green_time = volume * 2 / 3600 * 60  # Convert to seconds
            green_time = max(travel_time, volume_green_time)
            green_times.append(green_time)
    return green_times

# Function to get user input for distances, speeds, and traffic volumes
def get_user_input():
    while True:
        try:
            num_signals = int(input("Enter the number of signals: "))
            if num_signals <= 0:
                raise ValueError("Number of signals must be positive.")

            print(f"Enter distances between {num_signals} signals (comma-separated):")
            distances = list(map(int, input().strip().split(',')))

            print(f"Enter vehicle speeds for {num_signals} signals (comma-separated):")
            speeds = list(map(int, input().strip().split(',')))

            print(f"Enter traffic volumes at {num_signals} signals (comma-separated):")
            volumes = list(map(int, input().strip().split(',')))

            # Ensure that all lists are of the same length
            if len(distances) != num_signals or len(speeds) != num_signals or len(volumes) != num_signals:
                raise ValueError("The number of distances, speeds, and volumes must be equal to the number of signals.")

            return num_signals, distances, speeds, volumes
        except ValueError as e:
            print(f"Input error: {e}. Please try again.")
        except EOFError:
            print("Input error: Unexpected end of input. Please provide input in the expected format.")

# Function to get user input for emergencies and accidents
def get_emergency_accident_input(num_signals):
    emergencies = []
    accidents = []

    while True:
        try:
            print(f"Enter indices of signals with emergencies (comma-separated, e.g., 1,3) or press Enter to skip:")
            emergency_input = input().strip()
            if emergency_input:
                emergencies = list(map(int, emergency_input.split(',')))

            print(f"Enter indices of signals with accidents (comma-separated, e.g., 2,4) or press Enter to skip:")
            accident_input = input().strip()
            if accident_input:
                accidents = list(map(int, accident_input.split(',')))

            # Ensure indices are within range
            if any(e >= num_signals for e in emergencies) or any(a >= num_signals for a in accidents):
                raise ValueError("Emergency and accident indices must be within the range of signals.")

            return emergencies, accidents
        except ValueError as e:
            print(f"Input error: {e}. Please try again.")
        except EOFError:
            print("Input error: Unexpected end of input. Please provide input in the expected format.")

# Get user input
num_signals, distances, speeds, volumes = get_user_input()

# Get emergency and accident input
emergencies, accidents = get_emergency_accident_input(num_signals)

# Calculate green times based on the defined rules
green_times = calculate_green_times(distances, speeds, volumes)
print(f"Calculated Green Times for each signal: {green_times}")

# Run the simulation with the calculated green times and the emergency/accident cases
simulation = TrafficSimulation(distances, speeds, volumes, green_times, emergencies, accidents)
rating = simulation.simulate()

# Display the simulation result and rating
print(f"Simulation Rating (1-10): {rating}")
