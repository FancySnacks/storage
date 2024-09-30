#!/bin/bash

echo "storage: Running CREATE arg command chain"

parent_dir=$(pwd)
relative_dir="/tests/test_cli/create_args.txt"

exec_dir="${parent_dir}${relative_dir}"

source "$exec_dir"