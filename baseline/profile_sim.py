import cProfile
import pstats
import simulation

def main():
    simulation.run_simulation()

if __name__ == "__main__":
    profiler = cProfile.Profile()
    profiler.runcall(main)

    # Save raw profile file
    profiler.dump_stats("baseline_profile.prof")

    # Print top 20 functions by cumulative time
    stats = pstats.Stats(profiler).sort_stats("cumulative")
    stats.print_stats(20)

