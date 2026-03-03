1. docker-compose up -d --build
2. docker exec -it rabbitmq_client python receive_logs.py
3. docker exec -it rabbitmq_client python emit_logs.py
4. docker compose down --rmi all
5. docker-compose up -d --scale python-client=3
    - docker exec -ti CONTAINER_ID python emit_logs.py