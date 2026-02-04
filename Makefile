VENV_DIR ?= .venv
VENV_RUN = . $(VENV_DIR)/bin/activate

usage:  ## Show available make targets
	@grep -Fh "##" $(MAKEFILE_LIST) | grep -Fv fgrep | sed -e 's/:.*##\s*/##/g' | awk -F'##' '{ printf "%-20s %s\n", $$1, $$2 }'

venv:  ## Create the virtual environment if it doesn't exist
	@if [ ! -d ".venv" ]; then \
		echo "Creating virtual environment..."; \
		uv venv; \
	else \
		echo "Virtual environment already exists."; \
	fi

install: venv  ## Install dependencies
	$(VENV_RUN); \
	uv sync;

clean:  ## Remove virtual environment and artifacts
	rm -rf .venv
	rm -rf build/
	rm -rf *.egg-info/

new:  ## Create new loaf file (usage: make new NUM=6)
	@if [ -z "$(NUM)" ]; then echo "Usage: make new NUM=6"; exit 1; fi
	@padded=$$(printf "%03d" $(NUM)); \
	cp template.yaml loaves/loaf-$$padded.yaml; \
	sed -i '' "s/loaf_number: 1/loaf_number: $(NUM)/" loaves/loaf-$$padded.yaml; \
	sed -i '' "s/date: 2026-02-04/date: $$(date +%Y-%m-%d)/" loaves/loaf-$$padded.yaml; \
	echo "Created loaves/loaf-$$padded.yaml"

calculate:  ## Calculate derived fields (usage: make calculate NUM=6)
	@if [ -z "$(NUM)" ]; then echo "Usage: make calculate NUM=6"; exit 1; fi
	@padded=$$(printf "%03d" $(NUM)); \
	$(VENV_RUN); python scripts/calculate.py loaves/loaf-$$padded.yaml

validate:  ## Validate YAML structure (usage: make validate NUM=6)
	@if [ -z "$(NUM)" ]; then echo "Usage: make validate NUM=6"; exit 1; fi
	@padded=$$(printf "%03d" $(NUM)); \
	$(VENV_RUN); python scripts/validate.py loaves/loaf-$$padded.yaml

.PHONY: usage venv install clean new calculate validate
