
# ==========================================
# QUESTION 3: MEMORY MANAGEMENT
# Algorithms: First-Fit and Best-Fit
# ==========================================


# 1. Create the initial memory
def create_memory(total_memory):
    return [{"size": total_memory, "process": None}]


# 2. Allocate memory to a process
def allocate(memory, process, request, algorithm, stats):

    selected = -1

    # Search for a suitable free memory block
    for i in range(len(memory)):

        stats["checked"] += 1

        if memory[i]["process"] is None and memory[i]["size"] >= request:

            # First-Fit chooses the first suitable block
            if algorithm == "First-Fit":
                selected = i
                break

            # Best-Fit chooses the smallest suitable block
            elif selected == -1 or memory[i]["size"] < memory[selected]["size"]:
                selected = i

    # Check whether a suitable block was found
    if selected == -1:
        stats["failed"] += 1
        return

    # Calculate the memory remaining after allocation
    remaining = memory[selected]["size"] - request

    # Allocate the requested memory
    memory[selected]["size"] = request
    memory[selected]["process"] = process

    # Create a new free block if memory remains
    if remaining > 0:
        memory.insert(selected + 1, {
            "size": remaining,
            "process": None
        })

    stats["successful"] += 1


# 3. Release memory used by a process
def deallocate(memory, process):

    for block in memory:

        if block["process"] == process:

            # Mark the block as free
            block["process"] = None

            # Merge neighbouring free blocks
            merge_memory(memory)
            return


# 4. Merge neighbouring free memory blocks
def merge_memory(memory):

    i = 0

    while i < len(memory) - 1:

        if memory[i]["process"] is None and memory[i + 1]["process"] is None:

            memory[i]["size"] += memory[i + 1]["size"]
            memory.pop(i + 1)

        else:
            i += 1


# 5. Calculate memory utilization
def calculate_utilization(memory, total_memory):

    allocated = 0

    for block in memory:

        if block["process"] is not None:
            allocated += block["size"]

    utilization = (allocated / total_memory) * 100

    return utilization


# 6. Run one test using a selected algorithm
def run_test(algorithm, total_memory, operations):

    memory = create_memory(total_memory)

    stats = {
        "successful": 0,
        "failed": 0,
        "checked": 0
    }

    # Perform each allocation or deallocation
    for operation in operations:

        action = operation[0]
        process = operation[1]

        if action == "allocate":

            size = operation[2]
            allocate(memory, process, size, algorithm, stats)

        elif action == "free":

            deallocate(memory, process)

    # Calculate the final memory utilization
    utilization = calculate_utilization(memory, total_memory)

    # Return the results
    return {
        "utilization": utilization,
        "successful": stats["successful"],
        "failed": stats["failed"],
        "checked": stats["checked"]
    }


# 7. Compare First-Fit and Best-Fit
def compare_algorithms(test_name, total_memory, operations):

    print("\n", test_name)
    print("Total Memory:", total_memory, "KB")
    print("-" * 65)

    # Run both algorithms using the same operations
    first_fit = run_test("First-Fit", total_memory, operations)
    best_fit = run_test("Best-Fit", total_memory, operations)

    # Display the comparison
    print(f"{'Measurement':<25}{'First-Fit':<18}{'Best-Fit'}")
    print("-" * 65)

    print(
        f"{'Memory Utilization':<25}"
        f"{first_fit['utilization']:.2f}%{'':<12}"
        f"{best_fit['utilization']:.2f}%"
    )

    print(
        f"{'Successful Allocations':<25}"
        f"{first_fit['successful']:<18}"
        f"{best_fit['successful']}"
    )

    print(
        f"{'Failed Allocations':<25}"
        f"{first_fit['failed']:<18}"
        f"{best_fit['failed']}"
    )

    print(
        f"{'Blocks Examined':<25}"
        f"{first_fit['checked']:<18}"
        f"{best_fit['checked']}"
    )

    print("-" * 65)


# 8. Main program
if __name__ == "__main__":

    # TEST 1: 1000 KB memory
    test_one = [
        ("allocate", "P1", 200),
        ("allocate", "P2", 300),
        ("allocate", "P3", 100),
        ("free", "P2"),
        ("allocate", "P4", 250),
        ("allocate", "P5", 180)
    ]

    # TEST 2: 1500 KB memory with different process sizes
    test_two = [
        ("allocate", "P1", 400),
        ("allocate", "P2", 200),
        ("allocate", "P3", 500),
        ("free", "P1"),
        ("allocate", "P4", 300),
        ("allocate", "P5", 350),
        ("free", "P2"),
        ("allocate", "P6", 250)
    ]

    print("MEMORY MANAGEMENT SIMULATOR")
    print("===========================")

    compare_algorithms("TEST 1", 1000, test_one)

    compare_algorithms("TEST 2", 1500, test_two)

    print("\nSimulation completed.")
