#cp /home/darkmage/testform.html .
./build_docker.sh "$1"
docker push "jennamage/project-rest:$1"
#./restart.sh
