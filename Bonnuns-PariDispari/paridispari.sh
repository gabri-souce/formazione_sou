#ESERCIZIO BONUS
#Scrivere uno script che accetti un argomento numerico e stampi la sequenze di numeri da 1 a quel numero con l'indicazione se è pari o dispari.
#Controllare il corretto numero di argomenti passati allo script e che l'argomento sia di tipo numerico, in caso contrario generare una condizione di errore."
#!/bin/bash
if ! [ "$1" -eq "$1" ]  2>/dev/null; then   #compara il numero inserito con se stesso e silenzia l errore per permettere la visione del messaggio                  
    echo "Errore: '$1' non è un numero valido."
    exit 1 #con 1 si indica un errore
fi                                                   
    
#if ! [[ "$1" =~ ^[0-9]+$ ]] ; metodo n2 compreso ma lo ritengo ancora per ora complicato per me.
#Inoltre lo ritengo poco affidabile in quanto non controlla valori come lo 0 e caratteri speciali

for (( i=1; i<=$1; i++ )); do # l iteratore parte da 1,confronta l argomento passato ,aumenta di 1 l iteratore
  if (( i % 2 == 0 )); then #controlla se in numero è divisibile per due e quindi controlla se è pari
    echo "$i è pari"
  else
    echo "$i è dispari"
  fi
done


