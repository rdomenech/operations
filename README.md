# Operations

Basically there is a client script which reads the file operations.txt, sends the information from the file to a server through a socket, receive the response and writes it in a file called results.txt.

The server receives the information through a socket, does the arithmetic calcultions without using an EVAL and returns the response to the client.


## Supported Platforms

* [Python](http://www.python.org/) >= 3.6

## Getting Started

Install virtualenwrapper:
http://virtualenvwrapper.readthedocs.io/en/latest/install.html

Create a new virtualenwrapper environment and install: 
```bash
mkvirtualenv <name> python=<python_path>
pip install -r requirements.txt
```

Run the project:
```bash
python
```

```python
from socket_server import Server
server = Server()
server.start()
```

```bash
python socket_client.py
```

## Versioning

### 0.1.0

#### Features

- Initial release.

## Authors
* **Roger Domènech Aguilera**