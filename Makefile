all_tests:
	pytest tests

unit_tests:
	pytest tests/unit

integration_tests:
	pytest tests/integration

e2e_tests:
	pytest tests/e2e

tests_coverage:
	coverage run -m pytest

tests_coverage_report:
	coverage report

tests_coverage_html:
	coverage html

server:
	python3 -m run