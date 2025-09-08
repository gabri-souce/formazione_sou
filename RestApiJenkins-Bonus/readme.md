# Jenkins Master/Agent Automation with Vagrant & Ansible

Questo progetto automatizza la creazione di un ambiente Jenkins Master/Agent su Rocky Linux 9 usando Vagrant, VirtualBox e Ansible. Tutto viene gestito tramite playbook Ansible e provisioning Vagrant.

## Struttura del progetto

- **vagrantfile**  
  Configura la VM Jenkins con Rocky Linux 9, provisioning tramite Ansible.
- **ansible/**
  - **inventory.ini**  
    Inventario Ansible per la VM Jenkins.
  - **playbook-setup.yml**  
    Installa Docker, Jenkins Master (in container), e dipendenze di base.
  - **playbook-api.yml**  
    Crea un agente Jenkins via API REST (curl), genera token e avvia il container agent.
  - **playbook-api-uri.yml**  
    Crea un agente Jenkins via API REST (modulo Ansible URI + Groovy), genera token e avvia il container agent.

## Prerequisiti

- [Vagrant](https://www.vagrantup.com/)
- [VirtualBox](https://www.virtualbox.org/)
- [Ansible](https://www.ansible.com/)
- [Python 3](https://www.python.org/)

## Avvio rapido

1. **Avvia la VM Jenkins:**
   ```sh
   vagrant up jenkins
   ```
   Questo esegue il provisioning con `ansible/playbook-setup.yml`.

2. **Recupera la password iniziale Jenkins:**
   Alla fine del provisioning, troverai le istruzioni e la password nel log.

3. **Accedi a Jenkins:**
   - URL: [http://192.168.56.10:8080](http://192.168.56.10:8080)
   - Password: quella stampata dal provisioning

4. **Completa la configurazione Jenkins (installazione plugin, utente admin).**

5. **Provisiona l'agente Jenkins:**
   - Metodo API (curl):
     ```sh
     vagrant provision jenkins --provision-with api-setup
     ```
   - Metodo API (Ansible URI + Groovy):
     ```sh
     vagrant provision jenkins --provision-with api-uri
     ```

## Funzionalità principali

- **Jenkins Master** in container Docker, con volume persistente.
- **Jenkins Agent** creato e avviato automaticamente via API REST.
- **Networking**: Master e agent comunicano su una Docker network dedicata.
- **Automazione completa**: provisioning, installazione, configurazione e avvio agent tutto via Ansible.

## File principali

- [`vagrantfile`](vagrantfile): configurazione VM e provisioning.
- [`ansible/inventory.ini`](ansible/inventory.ini): inventario Ansible.
- [`ansible/playbook-setup.yml`](ansible/playbook-setup.yml): setup base Jenkins.
- [`ansible/playbook-api.yml`](ansible/playbook-api.yml): provisioning agent via API curl.
- [`ansible/playbook-api-uri.yml`](ansible/playbook-api-uri.yml): provisioning agent via API Ansible URI.

## Note

- L'utente di default per Jenkins è `gab` con password `123456` (modifica nei playbook per sicurezza).
- Tutti i container e volumi sono gestiti tramite Docker.
- Puoi estendere i playbook Ansible per aggiungere plugin, job, o configurazioni personalizzate.

---

**Autore:**  
Gabriele Inguscio