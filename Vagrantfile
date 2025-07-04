# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  config.vm.define "debian1" do |debian|
    debian.vm.box = "debian/bookworm64"
    debian.vm.box_version = "12.20250126.1"
    debian.vm.network "private_network", ip: "192.168.56.10"

    debian.vm.provision "shell", inline: <<-SHELL
      apt-get update
      dpkg --configure -a
      apt-get install -y apache2
      systemctl disable apache2
      systemctl stop apache2

      IFACE=$(ip -o -4 addr show | awk '$4 ~ /^192\\.168\\.56\\.10/ {print $2}')
      SRC_IP="192.168.56.20"
      LINK_SCELTO="https://youtu.be/9sJUDx7iEJw?si=ORqKT6-EZn8m0_9H"

      echo "!!!ASPETTO UN PING DA $SRC_IP SU $IFACE!!!"

      while true; do
        if tcpdump -c 1 -i "$IFACE" icmp and src host "$SRC_IP"; then
          echo "Ping ricevuto! Avvio Apache e creo la pagina web..."
          systemctl start apache2
          cat <<EOF > /var/www/html/index.html
<!DOCTYPE html>
<html>
  <head>
    <title>Pagina Link Personalizzato - AVVISO</title>
    <style>
      body {
        font-family: Arial, sans-serif;
        text-align: center;
        padding: 20px;
      }
      
      .avviso {
        background-color: #FFF8E1; /* Giallo chiaro solo nel box */
        border: 3px solid #FF5722; /* Bordo arancione */
        border-radius: 10px;
        padding: 20px;
        margin: 20px auto;
        max-width: 600px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
      }
      
      h1 {
        color: #D32F2F; /* Rosso scuro */
        font-size: 24px;
      }
      
      .icona {
        font-size: 40px;
        color: #FF5722; /* Arancione */
        margin-bottom: 10px;
      }
      
      .link {
        background-color: white;
        padding: 10px 15px;
        border-radius: 5px;
        display: inline-block;
        margin: 15px 0;
        font-weight: bold;
        border: 1px solid #ccc;
      }
      
      .avvertimento {
        font-weight: bold;
        color: #D32F2F;
        font-size: 16px;
        margin-top: 15px;
      }
    </style>
  </head>
  <body>
    <div class="avviso">
      <div class="icona"></div>
      <h1>AVVISO - CONTENUTO NON ADATTO AI MINORI</h1>
      
      <div class="link">
        <a href="$LINK_SCELTO" target="_blank">$LINK_SCELTO</a>
      </div>
      
      <p class="avvertimento">Cliccando sul link sopra, confermi di avere almeno 18 anni di eta'.</p>
    </div>
  </body>
</html>
EOF
          break
        fi
        sleep 1
      done
    SHELL
  end

  config.vm.define "rocky-music" do |rocky|
    rocky.vm.box = "bento/rockylinux-9"
    rocky.vm.box_version = "202502.21.0"
    rocky.vm.network "private_network", ip: "192.168.56.20"
  end
end
  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://vagrantcloud.com/search.
  
  # Disable automatic box update checking. If you disable this, then
  # boxes will only be checked for updates when the user runs
  # `vagrant box outdated`. This is not recommended.
  # config.vm.box_check_update = false

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine. In the example below,
  # accessing "localhost:8080" will access port 80 on the guest machine.
  # NOTE: This will enable public access to the opened port
  # config.vm.network "forwarded_port", guest: 80, host: 8080

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine and only allow access
  # via 127.0.0.1 to disable public access
  # config.vm.network "forwarded_port", guest: 80, host: 8080, host_ip: "127.0.0.1"

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  # config.vm.network "private_network", ip: "192.168.33.10"

  # Create a public network, which generally matched to bridged network.
  # Bridged networks make the machine appear as another physical device on
  # your network.
  # config.vm.network "public_network"

  # Share an additional folder to the guest VM. The first argument is
  # the path on the host to the actual folder. The second argument is
  # the path on the guest to mount the folder. And the optional third
  # argument is a set of non-required options.
  # config.vm.synced_folder "../data", "/vagrant_data"

  # Disable the default share of the current code directory. Doing this
  # provides improved isolation between the vagrant box and your host
  # by making sure your Vagrantfile isn't accessible to the vagrant box.
  # If you use this you may want to enable additional shared subfolders as
  # shown above.
  # config.vm.synced_folder ".", "/vagrant", disabled: true

  # Provider-specific configuration so you can fine-tune various
  # backing providers for Vagrant. These expose provider-specific options.
  # Example for VirtualBox:
  #
  # config.vm.provider "virtualbox" do |vb|
  #   # Display the VirtualBox GUI when booting the machine
  #   vb.gui = true
  #
  #   # Customize the amount of memory on the VM:
  #   vb.memory = "1024"
  # end
  #
  # View the documentation for the provider you are using for more
  # information on available options.

  # Enable provisioning with a shell script. Additional provisioners such as
  # Ansible, Chef, Docker, Puppet and Salt are also available. Please see the
  # documentation for more information about their specific syntax and use.
  # config.vm.provision "shell", inline: <<-SHELL
  #   apt-get update
  #   apt-get install -y apache2
  # SHELL

