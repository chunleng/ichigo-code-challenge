install: \
	install-front \
	install-api

install-front:
	cd apps/front; direnv allow; direnv exec . yarn install
install-api:
	{ \
		cd apps/api; \
		direnv allow; \
		direnv exec . poetry config --local virtualenvs.in-project true; \
		direnv exec . poetry env use python; \
		direnv exec . poetry install; \
	}

dev-front:
	cd apps/front; direnv exec . yarn dev
dev-api:
	cd apps/api; direnv exec . uvicorn main:app --reload
dev-resources:
	docker run -p 15432:5432 -e POSTGRES_PASSWORD=password postgres
