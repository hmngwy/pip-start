.PHONY: requirements rq_check rq_clean

rq_objects = $(wildcard requirements/*.in)
rq_outputs := $(rq_objects:.in=.txt)

# Make all requirements
requirements: $(rq_outputs)

# Make for requirements .txt files
requirements/%.txt: requirements/%.in
	pip-compile -v --output-file $@ $<

# Cascading dependencies
requirements/test.txt: requirements/base.txt
requirements/develop.txt: requirements/test.txt

rq_check:
	@which pip-compile > /dev/null

rq_clean: rq_check
	- rm requirements/*.txt
