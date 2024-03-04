#curl -X POST http://127.0.0.1:8000 -H 'Content-Type: application/json' -d '{"login":"my_login","password":"my_password"}'

curl -X GET http://127.0.0.1:8000 -H 'Content-Type: application/json'

#curl -X POST http://127.0.0.1:8000 -H 'Content-Type: application/json' -d '{"login":"my_login","password":"my_password"}'


# docker commands
#
# 

docker rmi iroottech/iroottech-rinha-2024q1 --force
docker build --no-cache -t iroottech/iroottech-rinha-2024q1 .
docker push iroottech/iroottech-rinha-2024q1
