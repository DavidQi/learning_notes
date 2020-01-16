# Docker Notes

### True or False questions
* Docker is PaaS.
* Neither daemon nor cron job could run in Docker.
* VM is Iaas. AWS EC is belone Iaas.

[Reference](https://docs.docker.com/engine/admin/using_supervisord/#running-your-supervisor-container)

[Run a cron job with Docker](https://github.com/Ekito/docker-cron)

### Several issues that I faced while trying to get a cron job running in a docker container were:
1. time in the docker container is in UTC not local time;
2. the docker environment is not passed to cron;

[User guide](http://www.widuu.com/chinese_docker/userguide/dockervolumes.html)

[Docker Hub](https://hub.docker.com/explore/)

[Docker Store](https://store.docker.com/search?q=&source=verified&type=image)

## Steps and Command to install docker in ubuntu-xenial(16.x.x) env

1. get key
```shell
sudo apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
```
2. add source list and update
```shell
echo 'deb https://apt.dockerproject.org/repo/ ubuntu-xenial main' | sudo tee /etc/apt/sources.list.d/docker.list
sudo apt-get update
```
3. install
```shell
sudo apt-get install docker-engine
```
4. start docker
```shell
sudo systemctl enable docker
sudo systemctl start docker
```
5. create docker group and add user to the group
```shell
sudo groupadd docker
groupadd: group 'docker' already exists
#sudo useradd -G docker $USER
#sudo usermod -aG docker david.qi
sudo gpasswd -a ${USER} docker
```
6. get images and run it
```shell
sudo docker pull logstash
docker run -it --rm logstash -e 'input { stdin { } } output { stdout { } }'
sudo docker run -d -p 80:80 owncloud
>>> ea85efa0bd68357603a639ecb1f6046dec9b1f8211c3046cbd5bd48b6c05a206
```
7. enter into container
```shell
sudo docker exec -it ea85efa0bd68357603a639ecb1f6046dec9b1f8211c3046cbd5bd48b6c05a206 bash
```

### PostgreSQL DB

1. install
```shell
sudo docker pull postgres
```
2. run DB server
```shell
sudo docker run -rm --name test-db -e POSTGRES_PASSWORD=123456 -d postgres
```
3. link and use
```shell
sudo docker run -it --rm --link test-db:postgres postgres psql -h postgres -U postgres
```
4. get DNB server IP address
```shell
sudo docker inspect test-db | grep IPAddress
```
5. test with Python
```python
import psycopg2
db_info = {'host':'172.17.0.2', 'database':'postgres', 'user':'postgres', 'password':'123456'}
conn = psycopg2.connect(**db_info)
cur = conn.cursor()
cur.execute('select version();')
r = cur.fetchone()
r
>>> ('PostgreSQL 9.6.1 on x86_64-pc-linux-gnu, compiled by gcc (Debian 4.9.2-10) 4.9.2, 64-bit',)
```

### Anaconda 3
```shell
docker pull continuumio/anaconda3
docker run -i -t continuumio/anaconda3 /bin/bash
```

### Jupyter Notebook
```shell
sudo docker run -i -t -p 8888:8888 continuumio/anaconda3 /bin/bash -c "/opt/conda/bin/conda install jupyter -y --quiet && mkdir /opt/notebooks && /opt/conda/bin/jupyter notebook --notebook-dir=/opt/notebooks --ip='*' --port=8888 --no-browser"
sudo docker ps -l
sudo docker commit 9eaa0be10a4d conda/jupyter
```

### Mount local volume
```shell
sudo docker run -it -v /home/david.qi/projects/:/home/david.qi/projects/ -v /home/david.qi/projects/MyPython/:/app/ --rm continuumio/anaconda3
```



### remove confilicting account from Ubunut
```shell
sudo /usr/share/centrifydc/bin/adrmlocal -c
```
