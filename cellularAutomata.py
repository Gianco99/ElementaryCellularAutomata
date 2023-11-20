import numpy as np
import matplotlib.pyplot as plt
import sys

if len(sys.argv) < 5:
    print("Usage: python cellularAutomata.py <rule> <size> <iterations> <boundary_condition>")
    sys.exit(1)

dimensions = int(sys.argv[2]) + 1
iterations = int(sys.argv[3])
boundary_condition = sys.argv[4].lower()

try:
    if int(sys.argv[1]) < 0 or int(sys.argv[1]) > 256:
        raise ValueError("Rule should be a number between 0 and 256.")
except ValueError:
    print("Error: Rule should be a valid integer between 0 and 256.")
    sys.exit(1)

if int(sys.argv[1]) != sys.argv[1]:
    print("Error: Rule must be an int!")
    sys.exit(1)

binary_rule = bin(int(sys.argv[1]))[2:].zfill(8)  

if dimensions < 3:
    print("Error: Size should be greater than or equal to 3.")
    sys.exit(1)

if iterations < 1:
    print("Error: Iterations should be greater than or equal to 1.")
    sys.exit(1)

if boundary_condition not in ['strict', 'periodic']:
    print("Error: Boundary condition should be 'strict' or 'periodic'.")
    sys.exit(1)

def create_rule_dictionary(binary_rule):
    rule_dict = {}
    for i in range(8):
        base_arr = np.array([int(x) for x in format(i, f'0{3}b')], dtype='int')
        rule_dict[tuple(base_arr)] = int(binary_rule[::-1][i])
    return rule_dict

rule_dict = create_rule_dictionary(binary_rule)

base_row = np.zeros(dimensions, dtype = int)
base_row[dimensions // 2] = 1

rows = [base_row]

def apply_rule(row, rule_dict, boundary_condition):
    new_row = np.zeros_like(row)
    for i in range(len(row)):
        left_neighbor = row[i - 1] if i > 0 else (row[-1] if boundary_condition == 'periodic' else 0)
        right_neighbor = row[i + 1] if i < len(row) - 1 else (row[0] if boundary_condition == 'periodic' else 0)
        neighborhood = (left_neighbor, row[i], right_neighbor)
        new_row[i] = rule_dict[neighborhood]
    return new_row

for iter in range(iterations - 1):
    base_row = apply_rule(base_row, rule_dict, boundary_condition)
    rows.append(base_row)

extent = [0, dimensions, iterations, 0]
plt.imshow(rows, cmap='binary', interpolation='nearest', extent=extent, aspect='equal')
plt.vlines(np.arange(0, dimensions+1), ymin=0, ymax=iterations, color='black', linewidth=1)
plt.hlines(np.arange(0, iterations+1), xmin=0, xmax=dimensions, color='black', linewidth=1)
plt.xlabel('Index')
plt.ylabel('Iteration')
plt.title('1D Cellular Automata - Rule ' + str(int(binary_rule, 2)))

plt.show()








