Vagrant.configure(2) do |config|

  # remote-VM
  config.vm.define "remote" do |remote|
    remote.vm.box = "generic/ubuntu1804"
    remote.vm.hostname = "ansible-remote"
    remote.vm.network "private_network", ip: "192.168.122.102"
    remote.vm.synced_folder './remote/', '/vagrant', type: '9p', :mount_options => ['dmode=775', 'fmode=664']

    remote.vm.provider "virtualbox" do |vb|
      vb.memory = 1024
      vb.cpus = 2
      # vb.name = "ansible-remote"
    end
    
    remote.vm.provision "shell", inline: <<-SHELL
      # DNS config
      sed -i.bak -e "s/^DNS=.*$/DNS=8.8.8.8 192.168.122.1/g" /etc/systemd/resolved.conf
      systemctl restart systemd-resolved.service
    SHELL
  end

  # control-VM
  config.vm.define "control" do |control|
    control.vm.box = "generic/ubuntu1804"
    control.vm.hostname = "ansible-control"
    control.vm.network "private_network", ip: "192.168.122.101"
    control.vm.synced_folder './control/', '/vagrant', type: '9p', :mount_options => ['dmode=775', 'fmode=664']

    control.vm.provider "virtualbox" do |vb|
      vb.memory = 512
      vb.cpus = 2
    end

    control.vm.provision "shell", inline: <<-SHELL
      # DNS config
      sed -i.bak -e "s/^DNS=.*$/DNS=8.8.8.8 192.168.122.1/g" /etc/systemd/resolved.conf
      systemctl restart systemd-resolved.service

      # Apt Repository Japanese
      cd /tmp
      wget -nv https://www.ubuntulinux.jp/ubuntu-ja-archive-keyring.gpg
      apt-key add /tmp/ubuntu-ja-archive-keyring.gpg

      cd /tmp
      wget -nv https://www.ubuntulinux.jp/ubuntu-jp-ppa-keyring.gpg
      apt-key add /tmp/ubuntu-jp-ppa-keyring.gpg

      mkdir -p /etc/apt/sources.list.d
      cd /etc/apt/sources.list.d
      wget -nv https://www.ubuntulinux.jp/sources.list.d/bionic.list
      mv bionic.list ubuntu-ja.list
      
      export DEBIAN_FRONTEND=noninteractive
      apt -y update
      apt -y install ubuntu-defaults-ja
      
      # pexpect
      # apt -y install expect
      apt -y install python-pip
      pip install pexpect
      
      # ansible 
      apt -y install software-properties-common
      apt-add-repository --yes --update ppa:ansible/ansible
      apt -y install ansible
      apt -y autoremove

      # ssh
      cp -f /vagrant/pexpect_sendkey.py ~/pexepect_sendkey.py
      chmod 774 ~/pexpect_sendkey.py

      mkdir -p ~/.ssh
      ssh-keygen -N "" -t ed25519 -f ~/.ssh/id_ed25519

      rm -f ~/.ssh/known_hosts
      ~/pexpect_sendkey.py vagrant@192.168.122.102
    SHELL
  end

end
