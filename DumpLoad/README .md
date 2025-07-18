{\rtf1\ansi\ansicpg1252\cocoartf2709
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww22980\viewh14320\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 SVN 1.6 \uc0\u8594  1.10 MIGRAZIONE TEST ENV\
==================================\
\
Questo progetto utilizza Vagrant per creare due VM distinte:\
\
1. CentOS 6 con Subversion 1.6 (svn16)\
2. CentOS 8 Stream con Subversion 1.10 (svn110)\
\
Scopo:\
------\
Verificare compatibilit\'e0 e migrazione tra versioni di Subversion usando:\
- dump/load\
- copia via filesystem\
\
Requisiti:\
----------\
- Vagrant\
- VirtualBox\
- Cartella locale: /Users/gabrieleinguscio/Desktop/BonusIE/1_E_7_GNTMST\
\
Struttura VM:\
-------------\
- IP `svn16`: 192.168.168.10\
- IP `svn110`: 192.168.168.20\
- Cartella condivisa montata su: /condivisa\
\
Avvio Ambiente:\
---------------\
1. Posizionarsi nella directory dove risiede il Vagrantfile\
2. Avviare le VM con:\
   vagrant up\
\
Dump e Load: (SVN 1.6 \uc0\u8594  1.10)\
-----------------------------\
[SVN16]\
1. Creare un repository:\
   svnadmin create /home/vagrant/svn_repos/repo1\
\
2. Creare working copy e commit:\
   svn checkout file:///home/vagrant/svn_repos/repo1 wc\
   cd wc\
   echo "prova" > file.txt\
   svn add file.txt\
   svn commit -m "commit da SVN 1.6"\
\
3. Dump:\
   svnadmin dump /home/vagrant/svn_repos/repo1 > /condivisa/repo1.dump\
\
[SVN110]\
4. Creare repo vuoto:\
   svnadmin create /home/vagrant/svn_repos/repo1\
\
5. Importare dump:\
   svnadmin load /home/vagrant/svn_repos/repo1 < /condivisa/repo1.dump\
\
6. Checkout per verifica:\
   svn checkout file:///home/vagrant/svn_repos/repo1 /home/vagrant/wc\
\
SVN 1.6 \uc0\u8594  1.10 MIGRAZIONE TEST ENV\
==================================\
\
Questo progetto utilizza Vagrant per creare due VM distinte:\
\
1. CentOS 6 con Subversion 1.6 (svn16)\
2. CentOS 8 Stream con Subversion 1.10 (svn110)\
\
Scopo:\
------\
Verificare compatibilit\'e0 e migrazione tra versioni di Subversion usando:\
- dump/load\
- copia via filesystem\
\
Requisiti:\
----------\
- Vagrant\
- VirtualBox\
- Cartella locale: /Users/gabrieleinguscio/Desktop/BonusIE/1_E_7_GNTMST\
\
Struttura VM:\
-------------\
- IP `svn16`: 192.168.168.10\
- IP `svn110`: 192.168.168.20\
- Cartella condivisa montata su: /condivisa\
\
Avvio Ambiente:\
---------------\
1. Posizionarsi nella directory dove risiede il Vagrantfile\
2. Avviare le VM con:\
   vagrant up\
\
Dump e Load: (SVN 1.6 \uc0\u8594  1.10)\
-----------------------------\
[SVN16]\
1. Creare un repository:\
   svnadmin create /home/vagrant/svn_repos/repo1\
\
2. Creare working copy e commit:\
   svn checkout file:///home/vagrant/svn_repos/repo1 wc\
   cd wc\
   echo "prova" > file.txt\
   svn add file.txt\
   svn commit -m "commit da SVN 1.6"\
\
3. Dump:\
   svnadmin dump /home/vagrant/svn_repos/repo1 > /condivisa/repo1.dump\
\
[SVN110]\
4. Creare repo vuoto:\
   svnadmin create /home/vagrant/svn_repos/repo1\
\
5. Importare dump:\
   svnadmin load /home/vagrant/svn_repos/repo1 < /condivisa/repo1.dump\
\
6. Checkout per verifica:\
   svn checkout file:///home/vagrant/svn_repos/repo1 /home/vagrant/wc\
\
Copia via Filesystem:\
---------------------\
[SVN16]\
1. Copiare repo fisico:\
   cp -r /home/vagrant/svn_repos/repo1 /condivisa/repo1_fs\
\
[SVN110]\
2. Importare:\
   cp -r /condivisa/repo1_fs /home/vagrant/svn_repos/repo1\
   svn checkout file:///home/vagrant/svn_repos/repo1 /home/vagrant/wc2\
\
Attenzione:\
-----------\
- Evitare di "loadare" in un repo gi\'e0 popolato \uc0\u8594  errori!\
- Se repo gi\'e0 esistente: eliminarlo o usare `--force`\
- Verificare permessi nella cartella `/home/vagrant/svn_repos`\
\
Distruzione VM:\
---------------\
Per fermare le VM:\
   vagrant halt\
\
Per distruggere tutto:\
   vagrant destroy -f\
\
\
\
\
\
\
\
\
}