# Dockerfile para MySQL 8.4
# Só assim é que coonsegui meter as configurações

FROM mysql:8.4

RUN mkdir -p /var/log/mysql && \
    chown -R mysql:mysql /var/log/mysql

COPY ./Configs/Hard_Test/mysql.cnf /etc/mysql/conf.d/mysql.cnf

RUN chmod 644 /etc/mysql/conf.d/mysql.cnf