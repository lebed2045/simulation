# Havven Simulation

## Running the simulation

This will be an agent-based model of the Havven system.

Before it can be run, you will need Python 3.6 or later and to install the pre-requisites with pip:

```pip3 install -r requirements.txt```

To run the simulation, invoke:

```python3 run.py```

If it is your first time running the simulation, a `settings.ini` file will be generated, that will give you control over how the simulation will run.
The first settings `cached = True` determines whether the data will be pre-generated before spawning a server, or whether the data will be generated in real time.
More info about the settings and caching can be found in the relevant sections.

To open the experiments notebook:

```jupyter notebook experiments.ipynb```

To run the tests:

```python3 -m pytest --pyargs -v```

Note: Running pytest through python3 is more consistent (global pytest install, other python versions).
The -v flag is for verbose, to list every individual test passing.

## Settings

Settings are contained in `settings.ini`, the file will be generated on the first run of the simulation using the `python3 run.py` command, individual setting descriptions can be found in `settingsloader.py`.

## Caching

Changing the caching setting changes how the data will be generated before being displayed on the local webpage. If caching is true, the data will be generated beforehand, and will be sent to the client at a rate only limited by connection speed (the `fps_default` setting controls this).
Otherwise, data will be presented in real time, being generated by the server as quickly as the client can request the next step.

Another difference between the two is the changing of model settings. If caching is true, settings are determined by dataset settings found in `cache_handler.py`. With caching being false, settings can be changed on the client side, and then generated by the server with the new settings.

## Overview

There are three major components to this simulation:

* The currency environment of Havven itself;
* A virtual exchange to go between nomins, havvens, and fiat;
* The agents themselves. possible future players:
    - [x] random players
    - [x] arbitrageurs
    - [x] havven bankers
    - [x] central bankers
    - [x] merchants / consumers
    - [x] market makers
    - [x] buy-and-hold speculators
    - [ ] day-trading speculators
    - [ ] cryptocurrency refugees
    - [ ] attackers

## Technicals
It runs on [Mesa](https://github.com/projectmesa/mesa), and includes the following files and folders:

* `run.py` - the main entry point for the program
* `server.py` - the simulation and visualisation server are instantiated here
* `model.py` - the actual ABM of Havven itself
* `core/orderbook.py` - an order book class for constructing markets between the three main currencies
* `core/stats.py` - statistical functions for examining interesting economic properties of the Havven model
* `core/settingsloader.py` - loads and generates settings files
* `core/cache_handler.py` - cached datasets are generated and loaded by this module
* `managers/` - helper classes for managing the Havven model's various parts
* `agents/` - economic actors who will interact with the model and the order book
* `test/` - the test suite
* `visualization/` - facilities for producing a live visualization web page
* `experiments.ipynb` - an environment for exploring system dynamics and scenarios in a more-efficient offline fashion.
