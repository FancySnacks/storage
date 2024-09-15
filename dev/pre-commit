#!/bin/bash

echo "===== Pre-commit: Running pre-commit script ====="

echo "===== Pre-commit: running Pytest ====="
pytest

if [ $? -ne 0 ]
then
  echo "===== Pre-commit: Pytest failed, abandoning commit ====="
  exit 1
else
  echo "===== Pre-commit: Pytest success ====="
fi

echo "===== Pre-commit: Success! Committing... ====="