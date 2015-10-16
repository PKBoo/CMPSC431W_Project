Vagrant.configure("2") do |config|


    config.vm.box = "ubuntu/trusty64"
    config.vm.network :forwarded_port, guest: 5000, host: 5000, auto_correct: true
    config.vm.synced_folder "./project", "/var/www", create: true, group: "www-data", owner: "www-data"

    config.vm.provider "virtualbox" do |v|
        v.name = "templatesandmoedev"
        v.customize ["modifyvm", :id, "--memory", "512"]
    end

    config.vm.provision "shell", path: "provision/setup.sh"
end