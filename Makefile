COMPOSE		:= docker compose --file compose.yml

up:
	$(COMPOSE) up --build  --detach --remove-orphans

down:
	$(COMPOSE) down --remove-orphans

alpine:
	docker run -it --rm alpine:3.18 sh

vault:
	docker run --cap-add=IPC_LOCK -e 'VAULT_LOCAL_CONFIG={"storage": {"file": {"path": "/vault/file"}}, "listener": [{"tcp": { "address": "0.0.0.0:8200", "tls_disable": true}}], "default_lease_ttl": "168h", "max_lease_ttl": "720h", "ui": true}' -p 8200:8200 hashicorp/vault server

clean:
	docker container prune -f
	docker image prune -f
	docker network prune -f
	docker volume prune -f
	docker builder prune --all -f

fclean: clean
	$(COMPOSE) down --volumes --remove-orphans
	docker image prune --all -f