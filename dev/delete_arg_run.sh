#!/bin/bash

echo "storage: Running DELETE arg command chain"

parent_dir=$(pwd)
relative_dir="/tests/test_cli/delete_args.txt"

exec_dir="${parent_dir}${relative_dir}"

source "$exec_dir"