build:
	gitbash package.sh

publish: build
	gitbash publish.sh

.PHONY: build publish
