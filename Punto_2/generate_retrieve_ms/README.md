# Generate Retrieve MS

```
generate_retrieve_ms/
├── deployment/
│   ├── .dockerignore
│   ├── Dockerfile
│   ├── Dockerfile.local
│   └── deployment.yaml
├── Makefile
├── README.md
├── requirements.txt
├── requirements-dev.txt
├── src/
│   ├── applications/
│   │   └── app_service.py
│   ├── domain/
│   │   ├── model/
│   │   │   ├── __init__.py
│   │   │   ├── message_error/
│   │   │   │   └── gateways/
│   │   │   │       └── message_error_repository.py
│   │   │   ├── embeddings/
│   │   │   │   └── gateway/
│   │   │   │       └── embeddings_gateway.py
│   │   │   └── database/
│   │   │       └── gateway/
│   │   │           └── database_gateway.py
│   │   └── usecase/
│   │       ├── __init__.py
│   │       ├── check_health/
│   │       ├── embed_store/
│   │       │   └── embed_store_use_case.py
│   │       └── retrieve/
│   │           └── retrieve_use_case.py
│   └── infraestructure/
│       ├── entry_points/
│       │   ├── fast_api/
│       │   │   ├── __init__.py
│       │   │   ├── handlers/
│       │   │   │   ├── __init__.py
│       │   │   │   └── retrieve_handler.py
│       │   │   └── health_handler.py
│       │   └── routes/
│       │       └── retrieve_router.py
│       └── helpers/
│           └── utils.py
└── tests/
    ├── conftest.py
    └── unit-test/
        └── src/
            ├── domain/
            │   └── usecase/
            │       ├── embed_store/
            │       │   └── test_embed_store_use_case.py
            │       └── retrieve/
            │           └── test_retrieve_use_case.py
            └── infraestructure/
                └── entry_points/
                    └── routes/
                        └── test_retrieve_router.py
```

En este microservicio se realiza el retrieve a la base de datos de conocimiento, al recibir la pregunta mejorada del usuario se decide normalizar los vectores para realizar la comparación por medio de la distancia de coseno. Finalmente, se realiza un top 3 para el retrieval. En local se había utilizado un Rerank pero su efecto no era muy significativo debido a que es un top 3, entonces no hacía mucho la diferencia.

En la carpeta tests/ pueden encontrar las pruebas unitarias, que pasaron al 93%, en ellas se utilizaron pytest, y un proceso de mocking para servicios como openai, rds, sns.

En la carpeta deployment, encontrarás el Dockerfile, Dockerfile.local y el manifiesto deployment.yaml con el cual se realiza la creación del pod. También están los requirements para instalar las librerías y un archivo Makefile en donde podrás encontrar comandos de utilidad.

- Endpoints: Puede encontrar la documentación de los endpoints aquí: http://a9b64fe8aa91a4bd999ae28dae1451c3-1604131751.us-east-1.elb.amazonaws.com:8002/docs (si hay un error al abrir por favor, cambia https por http al inicio de la url en el browser.)

![alt text](imagenes/image-1.png)