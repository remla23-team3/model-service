# `model-service`

## Creating and running the Docker image

#### Build the docker image

```bash
docker build -t <image_name> .
```

#### Run the docker image

```bash
docker run --network <bridged_network_name> --name model-service -p 6789:6789 <image_name>
```
This command assumes you have a bridged network created by the `docker network` command. All containers should run on the same network.

Once you finish these two steps, you can make a POST request to `127.0.0.1:6789/predict`.
For more information about what the endpoint expects and what it will return, take a look at `127.0.0.1:6789/apidocs`.

## Creating and running the Kubernetes service

#### Creating the registry credentials

```bash
kubectl create secret docker-registry registry-credentials \
--docker-server=ghcr.io \
--docker-username=<github_username> \
--docker-password=<personal_access_token>
```

#### Start the Kubernetes service

```bash
kubectl apply -f model-service.yml
```

You can check if the image was correctly pulled from the GitHub crate registry by running the following command:

```bash
kubectl get pods
```

If the `STATUS` of the image with name `model-service-deployment-...` is `ErrImagePull`, you probably misconfigured the registry credentials.

#### Retrieve the URL for the `model-service`

```bash
minikube service model-service --url
```

If everything is working correctly, you should see a URL in the format `http://127.0.0.1:<port>`. If you visit that port, the app functions the same as described in the section about the Docker image. Ensure to keep the terminal window open, otherwise the service will be shut down.
