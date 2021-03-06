# PBO

### How to run (Mac)
1. Python3 -m venv venv
2. source (or .) venv/bin/activate (Mac) OR source (or .) venv\scripts\activate (Windows)
3. pip install -r requirements.txt
4. Python3 main.py
5. Visit http://127.0.0.1:8050

### How to run (Windows
1. py -m venv venv
2. source (or .) venv\scripts\activate
3. pip install -r .\requirements.txt
4. py main.py
5. Visit http://127.0.0.1:8050

### About

This repository is an academic exercise for the course Business Process Optimization (
X_400213) for the Vrije Universiteit Amsterdam. The goal of this project is building a decision support system (DSS). 


### Scenario
In the given scenario, a website manager wants to know which version of their website will result in the most clicks. The website consists of three elements: A header, a text and a picture. The website manager has multiple variations of all three elements and wants to test various combinations. All combinations must contain one header, one text and one picture. 

We will create a decision support system that allows the website manager to run and analyse website selection experiments using multiple algorithms.



### Website selection algorithms. 
Hier uitleg wat A/B testing is en welke algoritmes we gebruiken

- AB Testing
- Multivariate testing
- Epsilon greedy
- Thompson sampling


### Structure of repository
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
