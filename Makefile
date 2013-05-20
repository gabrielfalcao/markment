all: test

filename=markment-`python -c 'import markment.version;print markment.version.version'`.tar.gz

export PYTHONPATH:=  ${PWD}

test: clean unit functional docs integration

unit: clean
	@echo "Running unit tests"
	@nosetests --cover-branches --with-coverage  --cover-erase --cover-package=markment --stop -v -s tests/unit

functional: clean prepare
	@echo "Running functional tests"
	@nosetests --stop -v -s tests/functional

integration: clean
	@python markment/bin.py -t slate -o ./_public/ example

docs: clean
	@steadymark README.md

clean:
	@printf "Cleaning up files that are already in .gitignore... "
	@for pattern in `cat .gitignore`; do rm -rf $$pattern; find . -name "$$pattern" -exec rm -rf {} \;; done
	@echo "OK!"

release: test
	@./.release
	@python setup.py sdist register upload

prepare:
	@mkdir -p output

theme:
	@python markment/bin.py -t bootstrap --server example

run: clean
	@reset && python markment/server.py
