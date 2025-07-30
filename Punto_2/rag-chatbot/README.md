# rag chatbot (Interfaz Gráfica)

```
rag-chatbot/
├── adapter/
│   └── load-secrets.js
├── deployment/
│   ├── .dockerignore
│   └── deployment.yaml
├── public/
│   ├── favicon.ico
│   ├── index.html
│   ├── logo192.png
│   ├── logo512.png
│   ├── manifest.json
│   └── robots.txt
├── src/
│   ├── App.css
│   ├── App.js
│   ├── ChatBox.css
│   ├── ChatBox.jsx
│   ├── index.css
│   ├── index.js
│   └── setupTests.js
├── config.json
├── package.json
├── README.md
└── server.js
```

Este microservicio tiene un front en React, puedes encontrar la estructura de un proyecto React en la carpeta src. El ChatBox.jsx es el principal script donde podrás encontrar la lógica de orquestación.

Tiene una carpeta de adapter/ donde encontraras un script para conectarse y extraer los secretos del secret manager en tiempo de ejecución (Es un wrapper).

En el archivo de server.js encontrarás el backend hecho con un servidor de ExpressJS.

Finalmente, en la carpeta de deployment, encontrarás la imagen Docker para dockerizar la aplicación y un entrypoint para poder crear .env en tiempo de ejecución. Además, dedployment.yaml es el manifiesto que tiene toda la configuración para crear el pod.