import numpy as np
import time

# Default values
DEFAULT_DISTANCES = [100, 150, 200]
DEFAULT_SPEEDS = [50, 60, 70]
DEFAULT_VOLUMES = [1000, 1200, 1500]
DEFAULT_GREEN_TIMES = [30, 40, 50]
DEFAULT_EMERGENCIES = []
DEFAULT_ACCIDENTS = []

# Traffic simulation class
class TrafficSimulation:
    def __init__(self, distances, speeds, volumes, green_times, emergencies, accidents):
        self.distances = distances
        self.speeds = speeds
        self.volumes = volumes
        self.green_times = green_times
        self.emergencies = set(emergencies)
        self.accidents = set(accidents)
        self.flow = []
        self.bad_scenarios = []

    def optimize_signals(self):
        # Example of dynamic adjustment: Increase green time for high volume signals
        optimized_green_times = [
            max(gt, volume * 2 / 3600 * 60)  # Adjust based on volume
            for gt, volume in zip(self.green_times, self.volumes)
        ]
        return optimized_green_times

    def simulate(self):
        optimized_green_times = self.optimize_signals()
        num_signals = len(self.distances)

        self.flow = []
        self.bad_scenarios = []

        for i in range(num_signals):
            if i in self.accidents:
                self.flow.append(0)  # Traffic is blocked due to an accident
                self.bad_scenarios.append((i, 'Accident'))
            elif i in self.emergencies:
                self.flow.append(5)  # Reduced flow due to an emergency
                self.bad_scenarios.append((i, 'Emergency'))
            else:
                try:
                    # Calculate travel time
                    travel_time = self.distances[i] / self.speeds[i]
                    # Compare travel time with green light duration
                    if travel_time <= optimized_green_times[i]:
                        self.flow.append(10)  # Smooth flow
                    else:
                        # Penalty based on how much the travel time exceeds green time
                        excess_time = travel_time - optimized_green_times[i]
                        penalty = min(9, excess_time / optimized_green_times[i] * 9)  # Cap penalty to 9
                        flow_rating = max(1, 10 - penalty)
                        self.flow.append(flow_rating)
                        if flow_rating < 5:
                            self.bad_scenarios.append((i, f'Low flow (Rating: {flow_rating:.2f})'))
                except ZeroDivisionError:
                    print(f"Warning: Speed cannot be zero at signal index {i}.")
                    self.flow.append(0)
                    self.bad_scenarios.append((i, 'Zero Speed'))

        # Calculate the mean flow rating
        self.rating = np.mean(self.flow) if self.flow else 0
        return self.rating

def calculate_green_times(distances, speeds, volumes):
    green_times = []
    for distance, speed, volume in zip(distances, speeds, volumes):
        if speed <= 0:
            print(f"Warning: Speed should be greater than zero for distance {distance}.")
            green_times.append(0)
        else:
            travel_time = distance / speed
            volume_green_time = volume * 2 / 3600 * 60  # Convert to seconds
            green_time = max(travel_time, volume_green_time)
            green_times.append(green_time)
    return green_times

# Function to simulate predefined user input
def get_predefined_input():
    num_signals = len(DEFAULT_DISTANCES)
    distances = DEFAULT_DISTANCES
    speeds = DEFAULT_SPEEDS
    volumes = DEFAULT_VOLUMES
    emergencies = DEFAULT_EMERGENCIES
    accidents = DEFAULT_ACCIDENTS
    return num_signals, distances, speeds, volumes, emergencies, accidents

def real_time_update_with_input(simulation, interval=10):
    while True:
        distances = DEFAULT_DISTANCES
        speeds = DEFAULT_SPEEDS
        volumes = DEFAULT_VOLUMES
        simulation.distances = distances
        simulation.speeds = speeds
        simulation.volumes = volumes
        simulation.green_times = calculate_green_times(distances, speeds, volumes)  # Recalculate green times

        simulation.simulate()
        print(f"Simulation Rating (1-10): {simulation.rating:.2f}")
        if simulation.bad_scenarios:
            print("Bad Scenarios:")
            for index, reason in simulation.bad_scenarios:
                print(f"Signal {index}: {reason}")

        time.sleep(interval)  # Wait for a specified interval before the next update

# Main execution
def main():
    num_signals, distances, speeds, volumes, emergencies, accidents = get_predefined_input()
    green_times = calculate_green_times(distances, speeds, volumes)

    print(f"Calculated Green Times for each signal: {green_times}")

    simulation = TrafficSimulation(distances, speeds, volumes, green_times, emergencies, accidents)

    # Start real-time simulation with dynamic input
    real_time_update_with_input(simulation)

if __name__ == "__main__":
    main()
