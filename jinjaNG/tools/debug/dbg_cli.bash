KIND="json"
KIND="py"
#KIND="yaml"

NB="01"

UNSAFE="-u"
#UNSAFE="--unsafe"
#UNSAFE=""

error_exit() {
    echo ""
    echo "ERROR - The following folder is the one giving an error."
    echo ""
    echo "  > $1"
    exit 1
}

THIS_DIR="$(cd "$(dirname "$0")" && pwd)"
JINJANG_DIR="$(cd "$THIS_DIR/../.." && pwd)"

TESTED_FOLDER="$THIS_DIR/files/$KIND-$NB"
DATA="$TESTED_FOLDER/data.$KIND"
TEMPLATE="$TESTED_FOLDER/template.txt"
OUTPUTFOUND="$TESTED_FOLDER/output_found.txt"

cd "$JINJANG_DIR"

echo ""
echo "\"$DATA\""
echo "\"$TEMPLATE\""
echo ""

python -m src $UNSAFE "$DATA" "$TEMPLATE" "$OUTPUTFOUND"  || error_exit "$TESTED_FOLDER"
