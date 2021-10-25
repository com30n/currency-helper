# currency-helper

### TLDR
 - Run server: `docker-compose run app`
 - Run tests: `docker-compose run tests`

### Docs
 - Openapi (swagger): http://0.0.0.0:8080/docs
 - Openapi.json http://0.0.0.0:8080/openapi.json
 - Redoc: http://0.0.0.0:8080/redoc
 
### Application configuration
 - Check out `config.yaml`

### Start server without docker
 - Create virtual env `virtualenv -p $(which python3) venv`
 - Enable the venv `source venv/bin/activate`
 - Install dependencies `pip install -r requirements.txt`
 - Run the server `python -m src.__main__`

### Run tests without docker
 - Create virtual env `virtualenv -p $(which python3) venv`
 - Enable the venv `source venv/bin/activate`
 - Install dependencies `pip install -r requirements.txt`
 - Run pytest `pytest`

### The app structure
 - The source directory `./src/`
 - The app entrypoint `./src/__main__.py`
 - The web server set up `./src/server.py`
 - Data models `./src/models.py`
 - API structure `./src/api/`
 - Tests `./src/tests/`
 - Caching strategies `./src/strategies/`
 - Additional scripts such as yaml config loading `./src/utils`

### Helm deployment
 - ```
   docker build -f Dockerfile \
     -t YOUR_DOCKER_REPOSITORY:YOUR_DOCKER_TAG
   ```
 - ```
    docker push YOUR_DOCKER_REPOSITORY:YOUR_DOCKER_TAG
   ```
 - ```
   helm install -f .helm/values .helm \
     --set app.image.repository=YOUR_DOCKER_REPOSITORY \
     --set app.image.tag=YOUR_DOCKER_TAG
   ```
