
# CS4310 Project - Graph Isomorphism


## Author
Brandon Rodriguez


## Description
Semester project. An attempt to investigate and implement a published algorithm about Graph Isomorphism.

This is a NP-Complete problem and as such, is expected to have exponential growth as more data is iterated through.


## Reference Paper
The offical, published paper which was referenced for this project can be located at
https://bmcbioinformatics.biomedcentral.com/articles/10.1186/1471-2105-14-S7-S13


## Powerpoint Location
Can be found at https://docs.google.com/presentation/d/1xKKcfbQlTewS2lX00D1-4tvnRIEUNj5gP5O8uUfnRUs/edit?usp=sharing


## Languages
Created in Python.

Networkx/Matplotlib extensions used for visual representation.
Such can be installed via:
* pip install networkx
* pip install matplotlib

Documentation can be found at:
* https://networkx.github.io/documentation/stable/
* https://matplotlib.org/users/index.html

To use matplotlib, you may need "sudo apt install python3-tk".


## Results
Results can be found in the documents/results folder. Each iteration of tests will have its own save file of data.

For simplicity, the following definitions will hold:
* All graphs and values will be randomly generated, using varying parameters as general soft-guides. (Due to
randomization, there is no gauranteed that iterations will hold to given parameters. However, statistically, they should
end up fairly close for the most part.)
* Every file will be 100 runs of the given parameters, noted in the file name.
* File name parameters will be as follows:
    * Node Count - This shall increase until compute time becomes too cumbersome. Due to randomization, graphs will
    contain roughly +/-10% of the indicated number.
    * Original Graph Density - Shall pertain to the following sub-definitions:
        * Sparse - Each node will be connected to roughly less than 33% of all nodes.
        * Middle - Each node will be connected to roughly between 33% and 66% of all nodes.
        * Dense - Each node will be connected to roughly more than 66% of all nodes.
    * Node Removal Amount - The "subgraph" to use in comparison shall have the following node amounts randomly removed:
        * None - Will be identical to original graph.
        * Few - Roughly less than 33% of all nodes will be removed.
        * Some - Roughly between 33% and 66% of all nodes will be removed.
        * Many - Roughly more than 66% of all nodes will be removed.
    * Edge Strictness - Due to data implementation, there are only two "edge strictness" modes:
        * 'loose' - Checks for only 33% of all edges to match.
        * 'strict' - Checks for only 66% of all edges to match.
* Inside each file, the results will be stored inside Python dictionary object representation, with the following
values (Note that these are stored in "epoch" or "number of seconds since Midnight, Jan, 1, 1970, UTC/GMT timezone):
    * Start Time - Time just before either graph was randomly generated.
    * First Graph Creation Time - Time just after first graph was generated.
    * Second Graph Creation Time - Time just after second graph was generated.
    * Graph Edge Sort Time - Time just after sorting both graph edges, to optimize for "Greatest Constraints" part of
    algorithm.
    * Greatest Constraints Time - Time to run first major half of algorithm, dubbed "Greatest Constraints".
    * Matching Time - Time to run second major half of algorithm, dubbed "Matching".
    * Number of Matches - Number of total node matches by algorithm.

