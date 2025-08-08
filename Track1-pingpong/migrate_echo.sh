#!/bin/bash

CONTAINER="echo-server"
IMAGE="ealen/echo-server"

# Genera configurazione SSH
vagrant ssh-config > vagrant_ssh_config || {
    echo "Errore generazione ssh-config"
    exit 1
}

# Leggi i nomi degli host dal file SSH config
HOSTS=($(grep '^Host ' vagrant_ssh_config | awk '{print $2}'))
NODE1=${HOSTS[0]}
NODE2=${HOSTS[1]}

# Funzione di connessione con gestione errori
vm_ssh() {
    local node=$1
    local cmd=$2
    ssh -F vagrant_ssh_config -o ConnectTimeout=10 "$node" "$cmd" 2>/dev/null
    return $?
}

# Gestione container 
manage_container() {
    local node=$1
    local action=$2
    
    if [ "$action" == "stop" ]; then
        # Forza la rimozione se esiste
        vm_ssh "$node" "docker rm -f $CONTAINER" >/dev/null
        return 0
    elif [ "$action" == "start" ]; then
        # Prima verifica che non esista già
        if ! vm_ssh "$node" "docker inspect $CONTAINER" >/dev/null; then
            vm_ssh "$node" "docker run -d --name $CONTAINER -p 3000:80 $IMAGE"
            return $?
        else
            echo "Container già esistente su $node" >&2
            return 1
        fi
    fi
}

# Pulizia iniziale
manage_container "$NODE1" "stop"
manage_container "$NODE2" "stop"

current_node="$NODE1"
next_node="$NODE2"

echo "Avvio migrazione container tra $NODE1 e $NODE2 ogni 60 secondi"

while true; do
    # Ferma container corrente
    if manage_container "$current_node" "stop"; then
        echo "$(date): Container rimosso da $current_node"
    else
        echo "$(date): ERRORE rimozione da $current_node"
    fi
    
    # Avvia container nuovo
    if manage_container "$next_node" "start"; then
        echo "$(date): Container avviato su $next_node"
    else
        echo "$(date): ERRORE avvio su $next_node"
    fi
    
    # Scambia nodi
    if [ "$current_node" == "$NODE1" ]; then
        current_node="$NODE2"
        next_node="$NODE1"
    else
        current_node="$NODE1"
        next_node="$NODE2"
    fi
    
     # Attesa con progress bar
    echo -n "Prossima migrazione tra 60s: ["
    for i in {1..60}; do
        echo -n "#"
        sleep 1
    done
    echo -e "]\n"
    
done