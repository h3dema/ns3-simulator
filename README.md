# ns3-simulator

This repository contains the files and basic instructions to create a docker container to run simulations using the NB-IoT implementation provided by [ns3-nbiot-ambient-iot](https://github.com/imec-idlab/ns3-nbiot-ambient-iot.git).

## Quick Start Guide

Follow these steps to clone the repository and launch the NS-3 simulator environment using Docker.

### 1. Clone the Repository

Clone the repository to your local machine and navigate into the project directory:

```bash
git clone https://github.com/h3dema/ns3-simulator.git
cd ns3-simulator
```

### 2. Build the Docker Image

Build the Docker container (this downloads dependencies and sets up the NS-3 environment):

```bash
docker compose build
```

### 3. Run the Container

Start an interactive session inside the NS-3 Docker container:

```bash
docker compose run ns3
```

> **Note:** If you prefer the container to be automatically cleaned up upon exit, run:
> ```bash
> docker compose run --rm ns3
> ```
>
>

### 4. Execute a Simulation

Once inside the container shell (`/opt/ns3-nbiot`), run a test simulation using `./waf`:

```bash
./waf --run "scratch/nb-scenario3.cc --simTime=60"
```


### 5. Exit the Container

To exit the container environment at any time, simply run:

```bash
exit
```


## Additional Command

This project can also use a simple `Makefile` to streamline common Docker tasks.
Instead of remembering long `docker` or `docker compose` commands, you can use short, predictable `make` targets.

Make acts as a lightweight command dispatcher: each target wraps a full Docker command behind a clean interface.
This keeps your workflow consistent and reduces mistakes when building, running, or cleaning up containers.

## Available Make Targets

Running:

```bash
make help
```

prints:

```text
Available targets:
  make build   - Build the Docker image
  make run     - Run the container (build if needed)
  make stop    - Stop the running container
  make clean   - Stop container and remove image
```

### `make build`

Builds the Docker image defined in the project’s `docker-compose.yaml` or Dockerfile.
Use this when:

- You changed source code that affects the image
- You updated dependencies
- You want to ensure the image is up‑to‑date before running

### `make run`

Runs the container. If the image does not exist yet, it will automatically trigger `make build` first.
Use this when:

- You want to start the simulator
- You want a fresh container instance
- You don’t want to manually check whether the image exists


### `make stop`

Stops the running container.
Use this command when:

- You want to halt the simulator
- You need to free ports or resources
- You want to restart cleanly


## `make clean`

Stops the container (if running) and removes the Docker image.
It is useful when:

- You want a full reset
- You want to rebuild everything from scratch
- You’re cleaning up old images or containers
