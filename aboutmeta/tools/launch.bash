#!/bin/bash

# --------------- #
# -- CONSTANTS -- #
# --------------- #

THIS_DIR="$(cd "$(dirname "$0")" && pwd)"
THIS_FILE=$(basename "$0")
THIS_FILE=${THIS_FILE%%.*}


# -------------- #
# -- AUTO-DOC -- #
# -------------- #

USAGE="Usage: bash $THIS_FILE.bash [OPTIONS]"
TRY="'bash $THIS_FILE.bash --help' for help."

HELP="$USAGE

  Launch all Python buider files.

Options:
  -q, --quick Any builder named '...-slow.py' will be ignored.
              This option is useful during the development phase,
              but not when the project has to be published.
  -h, --help  Show this message and exit.
"


# ----------- #
# -- TOOLS -- #
# ----------- #

print_cli_info() {
    echo "$2"
    exit $1
}


error_exit() {
    printf "\033[91m\033[1m"

    echo "  ERROR , see the file:"
    echo "    + $1/$2"

    exit 1
}


print_about() {
    printf "\033[$1"
    echo "$2"
    printf "\033[0m"
}


# ------------------- #
# -- ACTION WANTED -- #
# ------------------- #

if (( $# > 1 ))
then
    message="$USAGE
$TRY

Error: Too much options."

    print_cli_info 1 "$message"
fi


QUICKOPTION=0

if (( $# == 1 ))
then
    case $1 in
        "-q"|"--quick")
            QUICKOPTION=1
        ;;

        "-h"|"--help")
            print_cli_info 0 "$HELP"
        ;;

        *)
            message="$USAGE
$TRY

Error: No such option: $1"

            print_cli_info 1 "$message"
        ;;
    esac
fi


# ----------------- #
# -- LET'S WORK! -- #
# ----------------- #

cd "$THIS_DIR"

rm -f tools.log

# find . -type f -name "*.py" | sort | while read -r builderfile
find . -type f -name "*.py" ! -path "*/utilities/*" | sort | while read -r builderfile
do
    echo ""

    filename=$(basename "$builderfile")

    if [[ $QUICKOPTION == 1 && $filename =~ ^.*-slow\.py ]]
    then
        print_about "33m" "Ignoring $builderfile"

    else
        print_about "32m" "Launching $builderfile"
        python "$builderfile" || error_exit "$THIS_DIR" "$builderfile"
    fi
done

echo ""
