# PBO

## - ![#f03c15](https://via.placeholder.com/15/f03c15/000000?text="FLORIS JE BENT EEN LUIE KANKER HOND") ##

This repository is an academic exercise for the course Business Process Optimization (
X_400213) for the Vrije Universiteit Amsterdam. The goal of this project is building a decision support system (DSS) 


### A/B Testing
Hier uitleg wat A/B testing is en welke algoritmes we gebruiken



### Structure of DSS 
The decision support system consists of three main components: 
1. Data generation
2. A website selection algorithms
3. A graphical user interface



### Data generation and representation

##### Data generation
The budget _N_ stated by the user represents the amount of unique visitors to the domain featuring one of the _K_ websites to be tested. Each visitor is assumed to visit - and therefore participate in the experiment - only once. All visitors are assumed to have the same probability of "clicking" on a specific version of the website P(Click|Website N). Because some selection algorithms dynamically allocate traffic to some websites, a realisation of the click probability will be generated for each user for _all_ website configurations. This makes for convenient implementation. 

The data is generated in tree steps. 
1. For each element (3 x text, 3 x header, 3 x picture) a _effect size_ is generated using a uniform distribution U(A,B)
2. Then, for each possible combination (27 combinations) an interaction probability will be calculated using sigmoid(text + header + picture)
3. Lastly, a "synergestic" effect _P\_syn\_w_ will be added by skewing the generated interaction probability using a normal distribution N(P_i, 0.1)

##### Data representation
The data will be stored in a json and will have "metadata" key, keys for each website w with _N_ realisations of the Bernoulli distribution with p = P_syn_w 

### How to set up:
1. Clone
2. Hier verdere tutorial
