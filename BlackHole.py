#!/usr/bin/env python
# coding: utf-8

import numpy as np


def initialize_solutions(num_requirements, num_solutions):
    """
    Initialize random solutions (prioritizations).
    Each solution is a permutation of the requirement indices.
    """
    return [np.random.permutation(num_requirements) for _ in range(num_solutions)]

def update_position_towards_black_hole(solution, black_hole):
    """
    Update the position of a solution by moving it closer to the black hole.
    """
    update_ratio = np.random.random()
    # Calculate a weighted average between the solution and the black hole
    new_position = update_ratio * black_hole + (1 - update_ratio) * solution
    new_position = np.round(new_position).astype(int)
    new_position = np.clip(new_position, 0, len(solution) - 1)  # Ensure values are within valid range

    # Making sure the new position is a valid permutation
    unique, counts = np.unique(new_position, return_counts=True)
    duplicates = unique[counts > 1]

    for dup in duplicates:
        indices = np.where(new_position == dup)[0]
        for i in indices[1:]:  # Keep one, replace others
            replacement = np.random.choice(list(set(range(len(solution))) - set(new_position)))
            new_position[i] = replacement

    return new_position

def black_hole_optimization(objective_function, num_requirements, num_solutions, max_iterations):
    """
    The Black Hole Optimization Algorithm for requirements prioritization.
    """
    # Initialize solutions
    solutions = initialize_solutions(num_requirements, num_solutions)
    #print(solutions)

    for iteration in range(max_iterations):
        # Evaluate solutions
        fitness = np.array([objective_function(s) for s in solutions])

        # Find the best solution (black hole)
        black_hole_index = np.argmax(fitness)
        black_hole = solutions[black_hole_index]

        for i in range(num_solutions):
            if i != black_hole_index:
                solutions[i] = update_position_towards_black_hole(solutions[i], black_hole)
       
        # Evaluate solutions
        fitness = np.array([objective_function(s) for s in solutions])
        if black_hole_index != np.argmax(fitness):
            j = np.argmax(fitness)
            black_hole_index, j = j, black_hole_index
            black_hole = solutions[black_hole_index]
       

        event_horizon = fitness[black_hole_index]/sum(fitness)
        for i in range(num_solutions):
            if i != black_hole_index:

                # Distance between the black hole and the current solution
                distance = np.linalg.norm(black_hole - solutions[i])

                # Check if the solution is within the event horizon
                if distance < event_horizon:
                    # Replace the solution with a new random one
                    solutions[i] = np.random.permutation(num_requirements)

        #print(solutions)
        #print(objective_function(black_hole))
    # Return the best solution found
    return black_hole





