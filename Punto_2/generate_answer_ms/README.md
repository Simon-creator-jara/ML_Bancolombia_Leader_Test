# Generate Answer MS

```
generate_answer_ms/
├── deployment/
│   ├── .dockerignore
│   ├── Dockerfile
│   ├── Dockerfile.local
│   └── deployment.yaml
├── Makefile
├── requirements.txt
├── requirements-dev.txt
├── src/
│   ├── applications/
│   │   ├── app_service/
│   │   │   └── __init__.py
│   │   └── settings/
│   │       ├── __init__.py
│   │       └── container.py
│   ├── domain/
│   │   ├── model/
│   │   │   ├── answer/
│   │   │   │   ├── answer_model.py
│   │   │   │   └── gateway/
│   │   │   │       └── generate_answer_repository.py
│   │   │   ├── message_error/
│   │   │   │   ├── message_error_model.py
│   │   │   │   └── gateways/
│   │   │   │       └── message_error_repository.py
│   │   └── usecase/
│   │       ├── __init__.py
│   │       ├── check_health/
│   │       │   └── check_health_use_case.py
│   │       └── generate_answer/
│   │           └── generate_answer_use_case.py
│   └── infraestructure/
│       ├── driven_adapters/
│       │   ├── __init__.py
│       │   ├── openai/
│       │   │   └── adapter/
│       │   │       └── openai_adapter.py
│       │   ├── secret_repository/
│       │   │   └── adapter/
│       │   │       └── secret_manager_adapter.py
│       │   └── sns_repository/
│       │       └── adapter/
│       │           └── sns_repository.py
│       ├── entry_points/
│       │   ├── application.py
│       │   ├── fast_api/
│       │   │   ├── __init__.py
│       │   │   ├── handlers/
│       │   │   │   ├── __init__.py
│       │   │   │   ├── generate_answer_handler.py
│       │   │   │   └── health_handler.py
│       │   │   └── test_base.py
│       │   └── routes/
│       │       └── generate_answer_router.py
│       └── helpers/
│           └── utils.py
└── tests/
    ├── conftest.py
    └── unit-test/
        ├── config_test/
        │   └── config.json
        └── src/
            ├── domain/
            │   ├── model/
            │   │   └── answer/
            │   │       └── test_answer_model.py
            │   └── usecase/
            │       └── generate_answer/
            │           └── test_generate_answer_use_case.py
            └── infraestructure/
                ├── driven_adapters/
                │   └── openai/
                │       └── adapter/
                │           └── test_openai_adapter.py
                └── entry_points/
                    ├── fast_api/
                    │   └── handlers/
                    │       └── test_generate_answer_handler.py
                    └── routes/
                        └── test_generate_answer_router.py
```

En este microservicio simplemente se recibe la lista de respuesta recuperadas (top 3) y se crea un prompt de contexto apra pasarle al LLM como prompt. Finalmente se devuelve la respuesta.

En la carpeta tests/ pueden encontrar las pruebas unitarias, que pasaron al 93%, en ellas se utilizaron pytest, y un proceso de mocking para servicios como openai, rds, sns.

En la carpeta deployment, encontrarás el Dockerfile, Dockerfile.local y el manifiesto deployment.yaml con el cual se realiza la creación del pod. También están los requirements para instalar las librerías y un archivo Makefile en donde podrás encontrar comandos de utilidad.

- Endpoints: Puede encontrar la documentación de los endpoints aquí: http://a41eac32677e74d0585b024f6a5d478f-741200469.us-east-1.elb.amazonaws.com:8003/docs (si hay un error al abrir por favor, cambia https por http al inicio de la url en el browser.)

![alt text](imagenes/image.png)