# ns3-simulator

This repository contains the files and basic instructions to create a docker container to run simulations using the NB-IoT implementation provided by [https://github.com/BelogaevIDLab/ns3-nbiot](https://github.com/BelogaevIDLab/ns3-nbiot).

## Quick Start Guide

Follow these steps to clone the repository and launch the NS-3 simulator environment using Docker.

### 1. Clone the Repository

Clone the repository to your local machine and navigate into the project directory:

```bash
git clone [https://github.com/h3dema/ns3-simulator.git](https://github.com/h3dema/ns3-simulator.git)
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


---

```
