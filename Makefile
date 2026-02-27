.PHONY: check-conventions check-conventions-naming check-conventions-compatibility install-prettier markdown-fmt generate-docs generate-python install-ruff lint-python generate

check-conventions: check-conventions-naming check-conventions-compatibility

check-conventions-naming:
	~/repo/weaver/target/debug/weaver registry check \
		-p https://github.com/open-telemetry/opentelemetry-weaver-packages.git[policies/check/naming_conventions] \
		-r ./conventions \
		--v2

install-prettier:
	npm install --save-dev prettier

markdown-fmt: install-prettier
	npx prettier --write "./docs/**/*.md"
	npx prettier --write "README.md"

generate-docs:
	~/repo/weaver/target/debug/weaver registry generate \
		--registry ./conventions \
		markdown \
		--v2 \
		./docs
	$(MAKE) markdown-fmt

generate-python: install-ruff
	~/repo/weaver/target/debug/weaver registry generate \
		--registry ./conventions \
		python \
		--v2 \
		./conventions_py
	ruff format ./conventions_py
	ruff check ./conventions_py

generate: generate-docs generate-python

install-ruff:
	pip install ruff

lint-python: install-ruff
	ruff format .
	ruff check .

check-conventions-compatibility:
	~/repo/weaver/target/debug/weaver registry check \
		-p https://github.com/open-telemetry/opentelemetry-weaver-packages.git[policies/check/backwards-compatibility] \
		-r ./conventions \
		--baseline-registry https://github.com/lmolkova/semconv-scale23x-demo.git[conventions] \
		--v2
