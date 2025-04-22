import sys

def main(algo: str, world: str):
    """
    Main function to execute the vacuum robot planner.
    """
    print(initialize_world(world))


def initialize_world(world: str):
    """
    Initialize the world based on the provided world name.
    """
    with open(world, 'r') as file:
        vaccuum_world = file.readlines()
    vaccuum_world = [line.strip() for line in vaccuum_world] # [0] = height, [1] = width
    return vaccuum_world

def run_algorithm(algo: str, world: str):
    return 

if __name__ == "__main__":
    algorithm = sys.argv[1]
    world = sys.argv[2]
    main(algorithm, world)