# Test task

In the task it was needed to create simple API that can work with rates for cargos and calculate price for it.

## Features
    * Create, Read, Update, Delete rates for different dates and cargo types
    * Calculate actual price
    * Deploy via docker-compose

## How to use?

1. Clone this repository
2. Go to root directory of the project
3. Edit DB settings in docker-compose.yml file
4. Run `docker-compose build` to build project
5. Run `docker-compose up` to run project (use -d oprtion for detached run)
6. Go to `127.0.0.1:8000/docs` to see avaiable methods and use them
