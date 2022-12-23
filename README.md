# PAN Workplace Management System

PAN workplace management system is an opensource workplace management platform that is built upon Python and GO. Incorporating features like 
* process monitoring
* firewall rule management
* network analytics 
* service management
* system health analytics

**NOTE : The project is still under developmental phase and if you are interested in participating here are steps to replicate development environment and screenshots.**


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


## Tech Stack

**Client :** Go, GRPC

**Server :** Python, FastAPI, GRPC, RestAPI, Chart JS    

**Database :** Elasticsearch

## Screenshots

**Dashboard**

![dashboard](https://github.com/saksham-ghimire/workplace-management-system/blob/master/screenshots/dashboard.png)
![dashboard](https://raw.githubusercontent.com/saksham-ghimire/workplace-management-system/master/screenshots/dashboard_2.png)

**User Profile**

![user profile](https://raw.githubusercontent.com/saksham-ghimire/workplace-management-system/master/screenshots/profile.png)
![dynamic chart rendering](https://raw.githubusercontent.com/saksham-ghimire/workplace-management-system/master/screenshots/dynamic_rendering.gif)


**User activity detail**

![user activity](https://raw.githubusercontent.com/saksham-ghimire/workplace-management-system/master/screenshots/breached_log.png)
![table filtering](https://raw.githubusercontent.com/saksham-ghimire/workplace-management-system/master/screenshots/advanced_filtering.gif)

**Firewall Action**

![firewall action 1](https://raw.githubusercontent.com/saksham-ghimire/workplace-management-system/master/screenshots/firewall.png)
![successful response](https://raw.githubusercontent.com/saksham-ghimire/workplace-management-system/master/screenshots/firewall_add.png)


## License

[MIT](https://choosealicense.com/licenses/mit/)

