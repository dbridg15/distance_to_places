# distance_to_places

A simple flask web-app to find and display the closest train-stations to a given postcode.

To run you will need a valid API-key for `OS Names API` and `OS Maps API` (https://osdatahub.os.uk/)

## run
 - set your api-key to an environment variable (OS_API_KEY)
 - build the docker container:
 ```
 docker build -t distance_to_places --build-arg OS_API_KEY=${OS_API_KEY} .
 ```
 - go to http://127.0.0.1:5000
