FROM ubuntu:22.04

ENV USER=root
ENV TZ=UTC

COPY wait-for-it.sh /usr/local/bin/

RUN echo "APT::Get::Assume-Yes \"true\";" > /etc/apt/apt.conf.d/90assumeyes
RUN echo >>/etc/apt/apt.conf.d/99verify-peer.conf "Acquire { https::Verify-Peer false }"
RUN apt update 
RUN apt upgrade 
RUN apt -y install locales wget curl nano unzip ca-certificates rename iproute2 libc6-prof 
RUN locale-gen en_US.UTF-8 
RUN apt autoremove 
RUN apt clean 
RUN rm -rf /var/lib/apt/lists/* 
RUN rm -f /etc/apt/apt.conf.d/99verify-peer.conf    

ENV LANG=en_US.utf8 LANGUAGE=en_US:en LC_ALL=en_US.utf8
WORKDIR /
