all: test

filename=markment-`python -c 'import markment.version;print markment.version.version'`.tar.gz

export PYTHONPATH:=  ${PWD}

test: clean unit functional docs integration

unit:
	@echo "Running unit tests"
	@nosetests --with-coverage --cover-erase --cover-package=markment -v -s tests/unit

functional: prepare
	@echo "Running functional tests"
	@nosetests -v -s tests/functional

integration:
	@nosetests -v -s tests/integration
	@python markment/main.py -t slate -o ./generated/

docs:
	@steadymark README.md

clean:
	@printf "Cleaning up files that are already in .gitignore... "
	@for pattern in `cat .gitignore`; do rm -rf $$pattern; find . -name "$$pattern" -exec rm -rf {} \;; done
	@echo "OK!"

release: test publish
	@printf "Exporting to $(filename)... "
	@tar czf $(filename) markment setup.py README.md COPYING
	@echo "DONE!"

publish:
	@python setup.py sdist register upload

prepare:
	@mkdir -p output

run:
	@reset && python markment/server.py
