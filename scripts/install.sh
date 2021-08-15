# install docker, iptables
sudo yum -y install docker python3 iptables-services
# copy in iptable rules
sudo cp ~/project/scripts/iptables /etc/sysconfig/iptables
# enable and start iptables
sudo systemctl enable iptables 
sudo systemctl start iptables
# start and configure docker and docker-compose 
sudo service docker start
sudo usermod -aG docker $USER
sudo chkconfig docker on
sudo curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
# install systemd service for project
sudo cp ~/project/scripts/project.service /etc/systemd/system/project.service
sudo chmod +x /etc/systemd/system/project.service
sudo systemctl enable project.service
sudo systemctl start project.service