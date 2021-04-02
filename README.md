# stellar

## Developing

A Makefile, Dockerfile and docker-compose file are provided in the project repository to enable building image which may be useful when developing. To build a development image and run the compose version:
```
make up
```

Once the docker-compose version is ready, the service will be available at <http://127.0.0.1:80>. Additionally, the API documentation is available at <http://127.0.0.1:80/docs>.


## Reflecting

The project was built using FastAPI framework and were deployable using Docker as a service. Redis was used as a key-value store and caching server. I used FastAPI because it helped me develop an MVP fast given these time constraints, Redis because it was fast and powerful where it had built-in functionalities to cache and expire values out of the box, Docker because it could encapsulated a lot of the complexities of the build and deploy.

When deploying in production, I would want to have a manage Redis cluster so I don't have to manage my own and also will deploy the service using Kubernetes instead of Docker Compose for multi-node deployments.

There are many things to be improved but here are some of them that I think will give us a better ROI: having a better configuration management system, adding more details error handling, supporting logs and so on.
