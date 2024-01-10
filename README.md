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

### Generating a two degree graph with given mixing pattern:
