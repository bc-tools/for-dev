#!/bin/bash

THIS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"


# ------------ #
# -- PYTEST -- #
# ------------ #

cd "$THIS_DIR"

pytest -v ./
