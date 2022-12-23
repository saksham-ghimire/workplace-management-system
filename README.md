# PAN Workplace Management System

PAN workplace management system is an opensource workplace management platform that is built upon Python and GO. Incorporating features like 
* process monitoring
* firewall rule management
* network analytics 
* service management
* system health analytics

The project is still under developmental phase and if you are interested in participating here are steps to replicate development environment.

## Steps to replicate
* Clone the repository
```
git clone https://github.com/saksham-ghimire/workplace-management-system.git
```
* Setup Elasticsearch Instance (recommended to set it up with certificate)
* Inside server folder create python env and install necessities
```bash
python3 -m venv env
pip install -r requirements.txt
```
* Register client on elasticsearch instance on index namely 'workstations'. You can find description on index and fields below.

* Open cmd with escalated privileges inside client folder and run 
``` bash
go run main.go #without escalated privilege many features including firewall rule management is restricted.
```

* Run 
``` bash
uvicorn main:app --reload
``` 

## Context Explanation

Here are some helpful explanation and screenshot for people willing to contribute/participate. 

* API Document [The project is built upon fastapi so openAPI documentation is pre-provided. Access it with /docs endpoint]
* Dashboard [chartJS is used for visualization]
* State Management [Fetches information over GRPC and visualizes it on dashboard]
* Firewall rule management [Uses netsh under the hood to add remove and update firewall rule]
* Elasticsearch [Stores every collected log on elasticsearch, later used for visusalization]





## TechStack

* Python [Fast API]
* Go
* GRPC
* Elasticsearch
* Docker
* Chart.js


## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

