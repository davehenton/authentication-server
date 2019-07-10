#!/bin/bash
set -e
echo "1" > /tmp/kk
echo "#!/bin/bash" > /tmp/myscript
echo "export PATH='/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin'" >> /tmp/myscript
echo "touch /tmp/triggered" >> /tmp/myscript
#echo "/usr/bin/sleep 10s" >> /tmp/myscript
#echo "ln -s /usr/lib/systemd/system/nginx.service /etc/systemd/system/multi-user.target.wants/nginx.service" >> /tmp/myscript
echo "touch /tmp/triggered22222222" >> /tmp/myscript
echo "echo adingpythinscripthere" >> /tmp/myscript
#echo "/usr/bin/systemctl restart nginx" >> /tmp/myscript
chmod +x /tmp/myscript
#exec /tmp/myscript 2>&1 >> /tmp/mylog &
exec /tmp/myscript >> /tmp/mylog 2>&1 &
exec /usr/sbin/init


