FROM centos:6.6
RUN yum -y install httpd wget
RUN wget https://demo.borland.com/testsite/stadyn_largepagewithimages.html -O /var/www/html/index.html
EXPOSE 80
ENTRYPOINT ["/usr/sbin/httpd", "-D", "FOREGROUND"]
