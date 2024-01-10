- `Simulation`: contains code for generating all the results for this manuscript.

## Instruction on running the code
### Running Moran process on a graph
1. Compiling the C++ code.
```bash
g++ -std=c++11 Single.cpp -o Single 
``` 

2. Running Moran process on input graph and output results in to the results folder.
```bash
./Single graphs/$IN results/$OUT $TRIALS $SELECTION
```

### Generating a k-regular graph with given number of triangles:
```bash
python Triangle_sampling.py $DEGREE $SIZE $FRACTION_OF_TRIANGLES $OUTPUT
```

### Generating a two degree graph with given mixing pattern (Assortativity coefficient):
`Mixing_sampling.py` generates a graph with 50 nodes with degree D1 and 50 nodes with degree D2 while trying to satisfy the given mixing pattern. 
```bash
python Mixing_sampling.py $DEGREE1 $DEGREE2 $MIXING $OUTPUT
```

### Tuning input graph to a given number of triangles while keeping degree distribution and mixing pattern constant: 
```bash
python Triangle_tuning.py $INPUT $FRACTION_OF_TRIANGLES $OUTPUT
```

### Running evolutionary optimization using a network structure:
```bash
python GA_Main.py $ITERATIONS_PER_RUN $NUM_OF_RUNS $INPUT_GRAPH $OUTPUT
```
