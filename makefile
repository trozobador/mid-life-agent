# Makefile — Agente da Meia Idade

VENV = .venv
PYTHON = $(VENV)/bin/python
PIP = uv pip

.PHONY: setup
setup:
	uv venv $(VENV) --python 3.12
	$(PIP) install -r requirements.txt

.PHONY: run
run:
	$(PYTHON) main.py

.PHONY: role
# Uso: make role ROLE=data_scientist [PROVIDER=anthropic]
role:
	$(PYTHON) main.py --role $(ROLE) $(if $(PROVIDER),--provider $(PROVIDER),)

.PHONY: all-roles
# Uso: make all-roles [PROVIDER=anthropic]
all-roles:
	$(PYTHON) main.py --all $(if $(PROVIDER),--provider $(PROVIDER),)

.PHONY: list-roles
list-roles:
	$(PYTHON) main.py --list-roles

.PHONY: ingest
# Lê input/ e gera data/resume.json
# Uso: make ingest [PROVIDER=anthropic]
ingest:
	$(PYTHON) src/scripts/ingest_resume.py $(if $(PROVIDER),--provider $(PROVIDER),)

.PHONY: render
render:
	$(PYTHON) resume/generator.py

.PHONY: compare
compare:
	$(PYTHON) src/scripts/run_compare_pdf.py

.PHONY: linkedin-auth
linkedin-auth:
	$(PYTHON) src/scripts/linkedin_auth.py

.PHONY: clean
clean:
	rm -rf outputs/pdf/*.out outputs/pdf/*.log outputs/pdf/*.aux
	find . -name "__pycache__" -type d -exec rm -rf {} +
