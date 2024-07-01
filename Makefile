.PHONY: package

package:
	bash package.sh

deploy: package
	bash deploy.sh