# Stylist

## Setup

## 1. How to set up local environment

### 1) Clone the repo into local environment

Use git clone with the repo's link

### 2) Create an virtual environment of Python to work on this project

```shell
python3 -m venv env
```

### 3) Activate the venv and install the required libraries for this project

```shell
# Activate the virtual environment
source env/bin/activate

# Install required libraries
pip3 install -r requirements.txt
```

### 4) Weather set up

Currently, this [API](https://www.weatherapi.com/) is being used. Generate a .env file and add a weather key to use the feature.

```shell
WEATHER_KEY="YOUR API KEY"
```

The weather option is disabled by default, but can be turned on when creating the Database object.

### 5) Troubleshooting

If there are any problems dealing with installing certain packages - make sure your pip is updated to the most recent version.

```shell
pip3 install --upgrade setuptools
pip3 install --upgrade pip
```
