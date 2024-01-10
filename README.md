Code accompanying the project "Evolutionary graph theory beyond pairwise interactions: higher-order network motifs shape times to fixation in structured populations" https://www.biorxiv.org/content/10.1101/2021.06.26.450017v1.abstract

## Paper abstract 
To design population topologies that can accelerate rates of solution discovery in directed evolution problems or for evolutionary optimization applications, we must first systematically understand how population structure shapes evolutionary outcome. Using the mathematical formalism of evolutionary graph theory, recent studies have shown how to topologically build networks of population interaction that increase probabilities of fixation of beneficial mutations, at the expense, however, of longer fixation times, which can slow down rates of evolution, under elevated mutation rate. Here we find that moving beyond dyadic interactions in population graphs is fundamental to explain the trade-offs between probabilities and times to fixation of new mutants in the population. We show that higher-order motifs, and in particular three-node structures, allow the tuning of  times to fixation, without changes in probabilities of fixation. This gives a near-continuous control over achieving solutions that allow for a wide range of times to fixation.  We apply our algorithms and analytic results to two evolutionary optimization problems and show that the rate of solution discovery can be tuned near continuously by adjusting the higher-order topology of the population. We show that the effects of population structure on the rate of evolution critically depend on the optimization landscape and find that decelerators, with longer times to fixation of new mutants,  are able to reach the optimal solutions faster than accelerators in complex solution spaces.  Our results highlight that no one population topology fits all optimization applications, and we provide analytic and computational tools that allow for the design of networks suitable for each specific task.
 

## Instructions on running the code
- `Simulation`: contains code for generating all the results for this manuscript.
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
`Mixing_sampling.py` generates a graph with 50 nodes with degree D1 and 50 nodes with degree D2, while trying to satisfy the given mixing pattern. 
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
