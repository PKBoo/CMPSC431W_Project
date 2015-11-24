# templatesand.moe

Project for CMPSC431W

Team Name: Two's Complement

Team Members: Dylan Nguyen, Paul Kim, Chinmay Garg, Pocholo Gayan

## Setup

Install VirtualBox and Vagrant

1. `git clone https://github.com/PochGee/CMPSC431W_Project.git`
   
2. `cd CMPSC431W_Project`
   
3. `vagrant up` (takes some time)
   
4. `vagrant ssh` (should ssh you into your VM)
   
5. Edit your hosts file on your local machine to point `192.168.56.101` to `templatesandmoe.local`
   
   ``` 
   - Windows: `C:/Windows/System32/drivers/hosts`
   - OSX: `/etc/hosts`
   ```

## Running the App

1. Go to the root project folder on host machine
2. `vagrant up` (if the vm isn't on yet)
3. `vagrant ssh`
4. `cd /var/www/src`
5. `python3 run.py`  (run with `sudo` if there are any permission denied errors)
6. Go to templatesandmoe.local:5000 in your browser

Changes can be made through the host machine and will automatically be synced to the VM. Any files changes should be detected, and the application will be restarted automatically.

## Database Setup

1. SSH into the VM
2. `mysql -u root -p`
3. Enter `123456` as the password
4. `CREATE DATABASE templatesandmoe DEFAULT CHARACTER SET utf8;`
5. `exit`
6. `cd /var/www/src/sql`
7. `mysql -u root -p templatesandmoe < database1_2015-10-10.sql`
8. `mysql -u root -p templatesandmoe < testdata.sql`

### Useful commands

##### Import SQL file

` mysql -u root -p templatesandmoe < [sqlfile]` 