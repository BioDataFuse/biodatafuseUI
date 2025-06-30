# biodatafuseUI (beta)

work in progress...

# Docker
## Building the docker images
- **Build the backend image**
    While in the /backend directory:
    '''
    docker build --network=host -t backend .
    '''

- **Build the backend image**
    While in the /vue-app directory:
    '''
    docker build --network=host -t vue-app .
    '''
## Run docker compose
While in the main directory:
docker compose -f compose.yaml up

