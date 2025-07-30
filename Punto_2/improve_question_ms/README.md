# Improve Question MS

```
improve_question_ms/
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
│   │   └── settings/
│   │       └── container.py
│   ├── domain/
│   │   ├── model/
│   │   │   ├── __init__.py
│   │   │   ├── message_error/
│   │   │   └── question/
│   │   └── usecase/
│   │       ├── __init__.py
│   │       ├── check_health/
│   │       └── improve_question/
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
│       │   ├── fast_api/
│       │   │   ├── __init__.py
│       │   │   ├── handlers/
│       │   │   │   ├── __init__.py
│       │   │   │   └── improve_question_handler.py
│       │   │   └── health_handler.py
│       │   └── routes/
│       │       └── improve_question_router.py
│       └── helpers/
│           └── utils.py
└── tests/
    ├── conftest.py
    └── unit-test/
        └── src/
            ├── domain/
            │   ├── model/
            │   │   └── question/
            │   └── usecase/
            │       └── improve_question/
            └── infraestructure/
                ├── driven_adapters/
                │   └── openai/
                │       └── adapter/
                └── entry_points/
                    ├── fast_api/
                    │   └── handlers/
                    └── routes/
```
Este microservicio se encarga de recibir la pregunta del usuario y antes de mejorar se realiza un proceso de etiquetado, en donde se toma la decisión si es una pregunta real o es otro tipo de interacción. Si es otro tipo de interacción este micro responde directamente al front para evitar gastar tokens en el resto del proceso. Si es una pregunat real se continua con el llamado a los otros micros.

En la carpeta tests/ pueden encontrar las pruebas unitarias, que pasaron al 91%, en ellas se utilizaron pytest, y un proceso de mocking para servicios como openai, rds, sns.

En la carpeta deployment, encontrarás el Dockerfile, Dockerfile.local y el manifiesto deployment.yaml con el cual se realiza la creación del pod. También están los requirements para instalar las librerías y un archivo Makefile en donde podrás encontrar comandos de utilidad.

- Endpoints: Puede encontrar la documentación de los endpoints aquí: http://a801dd17f9e774a8b9d5b847151edea8-810000311.us-east-1.elb.amazonaws.com:8001/docs#/ (si hay un error al abrir por favor, cambia https por http al inicio de la url en el browser.)
