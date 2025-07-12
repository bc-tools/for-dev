#!/bin/bash

THIS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
THIS_FILE=$(basename "$0")
THIS_FILE=${THIS_FILE%%.*}

USAGE="Usage: bash $THIS_FILE.bash [OPTIONS]"
TRY="'bash $THIS_FILE.bash --help' for help."

HELP="$USAGE

  Launch all buider files.

Options:
  -q, --quick Any builder file named 'build_..._slow' wil be ignored.
              This option is useful during the development phase, but
              not when the project has to be published.
  --help      Show this message and exit.
"


print_cli_info() {
    echo "$2"
    exit $1
}


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

        "--help")
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

cd "$THIS_DIR"


error_exit() {
    printf "\033[91m\033[1m"

    echo "  ERROR , see the file:"
    echo "    + $1/$2"

    exit 1
}


print_about() {
    printf "\033[32m"
    echo "$1"
    printf "\033[0m"
}


while read -r builderfile  # <(find . -name 'build_*'  -type f | sort)
do
    filename=$(basename "$builderfile")

    echo ""

    if [[ $QUICKOPTION == 1 && $filename =~ ^build_.*_slow\..* ]]
    then
        print_about "Ignoring slow $builderfile"

    else
        print_about "Launching $builderfile"

        python "$builderfile" || error_exit "$THIS_DIR" "$builderfile"
    fi
done < <(find . -name 'build_*'  -type f | sort)

echo ""
