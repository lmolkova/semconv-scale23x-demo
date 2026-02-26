.PHONY: check-conventions

check-conventions:
	~/repo/weaver/target/debug/weaver registry check \
		-p https://github.com/open-telemetry/opentelemetry-weaver-packages.git[policies/check/naming_conventions] \
		-r ./conventions/src \
		--v2
