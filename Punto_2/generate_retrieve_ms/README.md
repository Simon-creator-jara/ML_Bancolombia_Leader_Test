# AIO Data Processing

Repositorio con el miscroservicio de limpieza de datos (limpieza de marca de agua, conversion a png y join de archivos de ocr).

## Unit test

```bash
python -m pytest --full-trace -vv -x --cov=src --cov-config=.coveragerc tests/unit-test
```

## Smoke Test

```bash
gradle clean test -Dendpoint=https://informacion-int-dev.apps.ambientesbc.com/aio/orchestrator/v1/health  --tests ManagementTest -i
```

## Local Development

### send message to sqs

```sh
aws sqs --endpoint-url=http://localhost:4566 send-message --queue-url http://sqs.us-east-1.localhost.localstack.cloud:4566/000000000000/local-aio-r2-dev-sqs-reception-queue.fifo --message-body file://local/sqs-message-example.json --message-group-id "message-group-id"
```
