# Local network simulator - AjiraNet
## Description
Local network simulator -Ajiranet simulates the basic network operations in a local network.
There are two types of Nodes in this network "COMPUTER" and "REPEATER"
We can connect Computer to Another Computer or Repeater, forming a undirected graph.  
Examples:
Cs are computers and Rs are repeaters
```
    C1 
    /\
 C2    C3 — R1 — C4 — C5
                |
                C6 
                |
                C7
```

```
    C1 
   /   \
  C2   R1 — C3 
   |   |
  R2 — C4 — C5

```

The networks can be in any topology.
Data traversing through the nodes has a strength. The strength decreases by one unit
when reaching a computer, and multiplies by 2 when reaching a repeater  

The network simulator can:
1. Add a node to the network
2. Add a connection between the nodes
3. Fetch the devices information from the network
4. Fetch the path of the route which the data travels, given a source and destination node
5. Modify the strength of the node to a given value

## Setup
### Requirements
1. I have built the project using python 3.7  
2. ```pip ``` is required to install packages
2. ```Virtualenv``` is required to setup virtual environment  
3. Python library requirements are specified in ```requirements.txt``` file  

### Get the server up and running
Three steps:
1. Create a virtual environment (You may skip this if you have no conflicting dependencies)
2. Install the dependencies  
3. Start the server

Step 1:  
Install virtual environment if not installed. Use ```pip3``` or ```pip``` according to your system setup  
In mac/linux:
```
python3 -m pip install --user virtualenv
```
In windows:
``` 
py -m pip install --user virtualenv
```

More information can be found here : https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/

In the project directory create a virtual environment (I am assuming a linux based environment)
```
virtualenv venv
```
Activate the virtual environment as   
In mac/linux:
``` 
source ./venv/bin/activate
```

In windows:
```
.\venv\Scripts\activate
```

Step 2:  
Install the dependencies
```
pip install -r requirements.txt
```

Step3:  
Start the server
```
python server.py
```
The server runs on port **8080**

## Running tests
There are two test files in /tests/ directory
1. ```test.py``` - All the tests that I wrote as part of development
2. ```test_cases.py``` - All the tests that were given as part of the problem statement

### Running from terminal
``` 
python -m unittest tests/test.py  
```

``` 
python -m unittest tests/test_cases.py  
```

### Running from Pycharm
Run the test files ```main``` function. Note that the order of the tests are dependant on each other

## Calling the endpoint
I am including both screenshots of using Postman as well as curl command in terminal.

### Postman
<img src="https://github.com/sidharthyatish/local-network-simulator/blob/main/screenshots/postman.png" alt="Making a POST call from python with input in body as raw text">

### Curl
<img src="https://github.com/sidharthyatish/local-network-simulator/blob/main/screenshots/curl.png" alt="Making a POST call curl">
