FROM dockereg.wealth-park.com/centos7k8pythonpostgres:latest
#FROM centos/systemd

MAINTAINER "Peter Malaty" <p@pmalaty.com>
#RUN yum clean all
RUN mkdir -p /usr/local/bin
WORKDIR /opt
RUN rm -rf *
RUN mkdir authentication-server
WORKDIR /opt/authentication-server
RUN ls -l
COPY ./onboot.sh /usr/local/bin/onboot.sh
COPY ./cronscript.sh /usr/local/bin/cronscript.sh
COPY ./cicd.sh /usr/local/bin/cicd.sh

RUN /usr/bin/chmod +x /usr/local/bin/onboot.sh /usr/local/bin/cronscript.sh  /usr/local/bin/cicd.sh
COPY ./cronjobs /var/spool/cron/root
RUN /usr/bin/ls -l /usr/local/bin/onboot.sh
COPY . .
RUN ls -l
RUN /usr/bin/echo $?
#EXPOSE 80
ENTRYPOINT ["/usr/local/bin/onboot.sh"]

