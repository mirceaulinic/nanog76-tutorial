export PROXYID ?= dummy

up:
	docker-compose up -d

down:
	docker-compose down
