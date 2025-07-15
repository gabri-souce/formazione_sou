#!/bin/bash
# Controllo argomenti
if [ "$#" -ne 3 ]; then
    echo "Utilizzo: $0 <ip> <start> <end> "
    exit 1
fi

TARGET="$1"
START="$2"
END="$3"

# Validazione input
echo "Scansione porte TCP su $TARGET (porte $START-$END)"
echo "----------------------------------------"

for port in $(seq "$START" "$END"); do
    # Usiamo nc senza -z, con timeout di 1 secondo
    if nc -nv -w 1 "$TARGET" "$port" </dev/null 2>&1 | grep -q "succeeded" ; then 
        echo "Porta $port: APERTA"
    fi
done

echo "----------------------------------------"
echo "Scansione completata"