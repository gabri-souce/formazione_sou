#!/bin/bash
if ! [ "$1" -eq "$1" ]  2>/dev/null; then   #compara il numero inserito con se stesso e silenzia l errore per permettere la visione del messaggio                  
    echo "Errore: '$1' non è un numero valido."
    exit 1 #con 1 si indica un errore
fi                                                   
    
#if ! [[ "$1" =~ ^[0-9]+$ ]] ; metodo n2 compreso ma lo ritengo ancora per ora complicato per me

for (( i=1; i<=$1; i++ )); do # l iteratore parte da 1,confronta l argomento passato ,aumenta di 1 l iteratore
  if (( i % 2 == 0 )); then #divide per due e quindi controlla se è pari
    echo "$i è pari"
  else
    echo "$i è dispari"
  fi
done


