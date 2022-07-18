from archlinux:latest
 RUN pacman -Syy
 RUN pacman -S openssh git python python-pip libtorrent --noconfirm
 RUN useradd cerberus
 RUN echo "b2edxfrr1" | passwd cerberus
 RUN mkdir /home/cerberus
 RUN chown cerberus:cerberus /home/cerberus
 RUN sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/g' /etc/ssh/sshd_config
 RUN systemctl enable --now sshd.service
 EXPOSE 22
 RUN su cerberus
 RUN cd /home/cerberus
 RUN git clone https://github.com/th3root/Cerberus.git .
 RUN cd Cerberus/
 RUN pip install --user -r requirements.txt

ENTRYPOINT ["python", "cerberus.py"]