https://docs.docker.com/engine/network/drivers/macvlan/
https://docs.docker.com/engine/network/
$ docker network create -d macvlan   --subnet=10.8.172.0/24   --gateway=10.8.172.1   -o parent=lxdbr0 lxdbr_dock0
docker run  --network lxdbr_dock0 -p 8501:8501 streamlit_app