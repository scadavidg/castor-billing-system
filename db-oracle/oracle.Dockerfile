FROM gvenzl/oracle-xe:21-slim

ENV ORACLE_PASSWORD=Oracle123
ENV ORACLE_ALLOW_REMOTE=true
ENV ORACLE_DATABASE=CASTOR

COPY ./oracle-init.sql /container-entrypoint-initdb.d/

EXPOSE 1521

CMD ["/usr/bin/tini", "--", "/container-entrypoint.sh"]
