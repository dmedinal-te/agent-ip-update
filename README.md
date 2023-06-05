# Workaround to update target IP addresses of agents that changed their IP because of DHCP.

Program will get all agents and will compare ipAddresses(array type) against targetForTests ip, if there's a mismatch it will update targetForTests by ipAddresses first value in array


## Getting Started
```
Before running install requirements package
pip install requests
pip install prettytable
```

## Running program
```
Update email
Program will get basic autch token from TOKEN env variable.(Suggested)
Alternatively, token can be hard coded into code(Not recommended).

```

## Output 
Program will ask if it should update all the matches, if "n" is selected it will ask entry by entry

```
**********Mismatched IPs**********
+--------+---------+--------------+-----------+
| Id     | Name    | IP           | Target_IP |
+--------+---------+--------------+-----------+
| 950891 | 9k-C111 | 10.11.111.11 | 1.2.3.4   |
+--------+---------+--------------+-----------+
Update all matches? (y/n): n
Update ip of 9k-C111 (y/n): y

**********Updated IPs**********
+--------+---------+--------------+--------------+
| Id     | Name    | IP           | Target_IP    |
+--------+---------+--------------+--------------+
| 950891 | 9k-C111 | 10.11.111.11 | 10.11.111.11 |
+--------+---------+--------------+--------------+
+---------+--------------+--------------+

```

## Enabling debugging to see HTTP requests performed 
```
Change logging level to DEBUG
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s - %(message)s')


DEBUG - URL: https://api.thousandeyes.com/v6/agents/987171.json
	GET - 200
	Headers: {'Content-Type': 'application/json', 'Accept': 'application/json'}

DEBUG - URL: https://api.thousandeyes.com/v6/agents/950891/update.json
	POST - 200
	Headers: {'Content-Type': 'application/json', 'Accept': 'application/json'}
	Body: {'targetForTests': '10.11.111.11'}

```

