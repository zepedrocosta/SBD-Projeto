# Dockerfile para MariaDB 11.4
# Só assim é que coonsegui meter as configurações

FROM mariadb:11.4

COPY ./Configs/Hard_Test/my.cnf /etc/mysql/my.cnf

RUN chmod 644 /etc/mysql/my.cnf