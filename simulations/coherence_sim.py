import numpy as np

PHI_PI = 5.083203692
D_ent_values = np.array([0.001, 0.01, 0.05, 0.1])
results = [(d, 1 + PHI_PI * d) for d in D_ent_values]

with open('simulations/results.csv', 'w') as f:
    f.write('D_ent,F_QC\n')
    for d, fqc in results:
        f.write(f'{d},{fqc}\n')
