from archlinux:latest
 RUN pacman -Syy
 RUN pacman -Syu --noconfirm
 RUN pacman -S openssh wget python python-pip libtorrent --noconfirm
 COPY id_rsa.pub /root/.ssh/authorized_keys
 RUN sed -i 's/#PermitRootlogin prohibit-password/PermitRootlogin prohibit-password/g' /etc/ssh/sshd_config
 EXPOSE 22
 RUN mkdir /root/build
 WORKDIR /root/build
 RUN wget 'https://github.com/th3r00t/Cerberus/releases/download/release/cerberus.tar.gz'
 RUN tar -xvzf cerberus.tar.gz
 RUN pip install -r requirements.txt
 ENV TERM=xterm
 ENV TERMINFO=/usr/lib/terminfo
 ENTRYPOINT sh -c /usr/bin/bash