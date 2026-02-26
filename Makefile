.PHONY: check-conventions check-compatibility install-prettier markdown-fmt generate-docs

check-conventions:
	~/repo/weaver/target/debug/weaver registry check \
		-p https://github.com/open-telemetry/opentelemetry-weaver-packages.git[policies/check/naming_conventions] \
		-r ./conventions/src \
		--v2

install-prettier:
	npm install --save-dev prettier

markdown-fmt: install-prettier
	npx prettier --write "./docs/**/*.md"

generate-docs:
	~/repo/weaver/target/debug/weaver registry generate \
		-r ./conventions/src \
		markdown \
		--v2 \
		./docs
	$(MAKE) markdown-fmt

check-compatibility:
	~/repo/weaver/target/debug/weaver registry check \
		-p https://github.com/open-telemetry/opentelemetry-weaver-packages.git[policies/check/backwards-compatibility] \
		-r ./conventions/src \
		--baseline-registry https://github.com/lmolkova/semconv-scale23x-demo.git[conventions/src] \
		--v2
