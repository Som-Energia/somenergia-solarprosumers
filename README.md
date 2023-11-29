# somenergia-solarprosumers
☀ Web application to manage collective campaigns to purchase and install solar panels at home


## Setup

### Requirements

* Python >= 3.8.2
* PostgreSQL >= 12
* redis >= 6
* mongo >= 3.0.2


### Application dependencies

Is highly recommendable to use a virtual environment to store application dependencies.

```shell
pip install -U pip
pip install -U setuptools
pip install -r requirements.txt
```

### Application configuration

Use the configuration template
```shell
cp config/settings/config.yaml.example config/settings/config.yaml
```

and set required configuration


## Usage

### Run migrations is needed
```shell
./manage.py showmigrations
./manage.py migrate
```

### Run the application
```shell
./manage.py runserver
```


## Development

### Development dependencies

```shell
pip install -r requirements-dev.txt
```

### Application infrastructure virtualization

As a development environment, it is recommended to use docker to virtualize the application infrastructure and
keep the infrastructure dependencies isolated of the host machine.


### Code standards

```shell
pre-commit install
```


### Tests

#### Execution

```shell
pytest somsolet/tests
```

### Changes
[CHANGELOG](CHANGELOG.md)
