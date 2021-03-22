# Survey

Система опроса клиентов 05RU

## Запуск

`docker` и `docker-compose` должны быть установлены.

- Сборка образов из `Dockerfile`:

  ```shell
  docker-compose build
  ```

- Запуск в локальном режиме:

    ```shell
    docker-compose up
    ```
- Запуск в режиме продакшена:

    ```shell
    docker-compose -f docker-compose-yml -f docker-compose.production.yml up
    ```
