# Preprocessing ms

```
preprocessing_ms/
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
│   │   │   ├── __init__.py
│   │   │   ├── chunks/
│   │   │   ├── dataset/
│   │   │   ├── database/
│   │   │   ├── embeddings/
│   │   │   ├── message_error/
│   │   │   └── repository/
│   │   └── usecase/
│   │       ├── __init__.py
│   │       ├── check_health/
│   │       ├── clean_data/
│   │       │   └── clean_data_use_case.py
│   │       ├── embed_store/
│   │       │   └── embed_store_use_case.py
│   │       └── split_data/
│   │           └── split_data_use_case.py
│   └── infraestructure/
│       ├── entry_points/
│       │   ├── application.py
│       │   ├── fast_api/
│       │   │   ├── __init__.py
│       │   │   ├── handlers/
│       │   │   │   ├── __init__.py
│       │   │   │   └── clean_split_data_handler.py
│       │   │   └── health_handler.py
│       │   └── routes/
│       │       └── clean_split_router.py
│       └── helpers/
│           ├── task_manager.py
│           └── utils.py
└── tests/
    ├── conftest.py
    └── unit-test/
        └── src/
            ├── domain/
            │   └── usecase/
            │       ├── clean_data/
            │       │   └── test_clean_data_use_case.py
            │       ├── embed_store/
            │       │   └── test_embed_store_use_case.py
            │       └── split_data/
            │           └── test_split_data_use_case.py
            └── infraestructure/
                └── entry_points/
                    └── routes/
                        └── test_clean_split_router.py
```

En este microservicio encontrarás toda la lógica para subir los archivos a la base de datos RDS (Base de datos de conocimiento).
Antes de insertar la información, se realiza un proceso de limpieza de la información con por medio ed regex y la librería ftfy, esta ayuda a mejorar encodings extraños. Luego de eso se realiza un split de la infromación para subirla por batchs. Cada batch tiene 100 records y se utiliza un método de multithreading para procesar en diferentes hilos. Antes de esto, se RecursiveCharacterTextSplitter.from_tiktoken_encoder para garantizar que cada chunk de datos contiene el número exacto de tokens aceptado por el modelo de embeddings (text-embedding-3-large). Con este procceso de splitter, se logró reducir el tiempo en la inserción de 25 min la primera vez a 3 a 4 min. Además antes de insertar lso recors se realiza un proceso de normalización de los vectores.

En la carpeta tests/ pueden encontrar las pruebas unitarias, que pasaron al 90%, en ellas se utilizaron pytest, y un proceso de mocking para servicios como openai, rds, sns.

En la carpeta deployment, encontrarás el Dockerfile, Dockerfile.local y el manifiesto deployment.yaml con el cual se realiza la creación del pod. También están los requirements para instalar las librerías y un archivo Makefile en donde podrás encontrar comandos de utilidad.

- Endpoints: Puede encontrar la documentación de los endpoints aquí: http://aaeb4e540d1d64e33bb7363644ee8f7d-548615679.us-east-1.elb.amazonaws.com:8000/docs  (si hay un error al abrir por favor, cambia https por http al inicio de la url en el browser.)

![alt text](imagenes/image_7.png)