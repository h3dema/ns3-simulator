Your custom code can be put here to be accessed inside the container.
It will appear in the `/opt/ns3-nbiot/scratch/my-scripts` directory inside the container.
You can add any scripts or code files you want to use with ns-3 in this directory, and they will be available when you run the container.

> Note: When the container is build, the contents of this directory will be copied and compiled into the ns-3 build. If there is any compiling error, the container will not be created.