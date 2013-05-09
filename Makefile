all: test

filename=markment-`python -c 'import markment.version;print markment.version.version'`.tar.gz

export PYTHONPATH:=  ${PWD}

test: clean unit functional docs integration

unit: clean
	@echo "Running unit tests"
	@nosetests --with-coverage --cover-erase --cover-package=markment --stop -v -s tests/unit

functional: clean prepare
	@echo "Running functional tests"
	@nosetests --stop -v -s tests/functional

integration: clean
	@python markment/bin.py -t slate -o ./_public/
	@egrep --color -r 'style.css' _public

docs: clean
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

run: clean
	@reset && python markment/server.py
