# Sole-Zon-Solis website, CyberForce 2022

This site was built for the 2022 CyberForce competition. It's not secure, please 
don't run this in a real environment.

This site is built using the Flask python framework. Our site does not integrate
with AD or SMTP. It was made to integrate with FTP using rclone's mount
functionality.

Start-up was setup using the vita.service systemd service. The site was proxied
and static resources served by through nginx's try\_files.

The app must be placed in /srv/flask, with a flask user, and the rclone ftp
remote mounted in to a directory in its folder named `uploads`.

I apologize in advance for the questionable code quality and practices.
