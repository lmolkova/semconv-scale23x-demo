.PHONY: check-conventions check-compatibility install-prettier markdown-fmt generate-docs generate-python install-ruff lint-python

check-conventions:
	~/repo/weaver/target/debug/weaver registry check \
		-p https://github.com/open-telemetry/opentelemetry-weaver-packages.git[policies/check/naming_conventions] \
		-r ./conventions \
		--v2

install-prettier:
	npm install --save-dev prettier

markdown-fmt: install-prettier
	npx prettier --write "./docs/**/*.md"

generate-docs:
	~/repo/weaver/target/debug/weaver registry generate \
		-r ./conventions \
		markdown \
		--v2 \
		./docs
	$(MAKE) markdown-fmt

generate-python: install-ruff
	~/repo/weaver/target/debug/weaver registry generate \
		-r ./conventions \
		python \
		./conventions_py \
		--v2
	ruff format ./conventions_py
	ruff check ./conventions_py

install-ruff:
	pip install ruff

lint-python: install-ruff
	ruff format .
	ruff check .

check-compatibility:
	~/repo/weaver/target/debug/weaver registry check \
		-p https://github.com/open-telemetry/opentelemetry-weaver-packages.git[policies/check/backwards-compatibility] \
		-r ./conventions \
		--baseline-registry https://github.com/lmolkova/semconv-scale23x-demo.git[conventions] \
		--v2
