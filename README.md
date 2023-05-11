# model-service

1. Build the docker image

```bash
docker build -t <image_name> .
```

2. Run the docker image

```bash
docker run --network <bridged_network_name> --name model-service -p 6789:6789 <image_name>
```
This command assumes you have a bridged network created by the `docker network` command. All containers should run on the same network.

Once you finish these two steps, you can make a POST request to `127.0.0.1:6789/predict`.
For more information about what the endpoint expects and what it will return, take a look at `127.0.0.1:6789/apidocs`.
