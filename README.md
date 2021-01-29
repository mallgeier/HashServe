# HashServe
Basic PyTest Coverage of hash Serve api

Broken-hashserve testing
============================================================

Environment
----------------------------------------------------------------------------------------------
Ubuntu running as App in windows as well as directly in Windows, python 3 with pytest, requests module

Setup
----------------------------------------------------------------------------------------------

- Install python 3

  sudo apt-get update
  sudo apt-get install python3.8
- Install pip

  Sudo apt install python3-pip
- Install api-testing (NOTE: not used at present - intended for ease of future refactoring for boilerplate code and configuration)
  
  Git clone https://github.com/luvsharma19/api-testing.git
- Install requests(for api interation), Flask (more mocking endpoints to test and validate tests), pytest (test framework)
  pip3 install -U requests Flask pytest pytest-html
  Sudo apt install python-pytest

Execution
----------------------------------------------------------------------------------------------
- navigate to base directory and execute pytest with logging and html output file specified:
  pytest -sv --capture=sys --html=results\output.html
- sample output: https://github.com/mallgeier/HashServe/blob/main/pytest/results/output.html

Defects Uncovered
----------------------------------------------------------------------------------------------
- Retrieval of hash is not returning correct value (see: tests/test_Hash3.py::TestHash::test_hash_pw_valid)
- stats is incorrectly reporting 0 average time per request (see: tests/test_Hash3.py::TestHash::test_hash_stats_valid)

To-Dos
----------------------------------------------------------------------------------------------
- refactor for configuration, helpers, exception handling, etc (either directly or with a package like api-testing)
- decouple tests further
- expand boundary, edge, negative testing, etc
- enhance reporting for specific CI pipeline
  
