#!/bin/bash

echo "storage: Running CLEAR arg command chain"

parent_dir=$(pwd)
relative_dir="/tests/test_cli/clear_args.txt"

exec_dir="${parent_dir}${relative_dir}"

source "$exec_dir"