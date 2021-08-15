cd ~/project
echo `pwd`
mkdir -p ~/logs
docker-compose up -d
python3 scripts/docker_tail.py