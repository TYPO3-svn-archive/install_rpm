# This file is appended to the header of .spec before the RPM is built.
# All platform/flavor dependent stuff (like requires with specific version
# numbers should go here. 
Release: RH_~~RPMRELEASE~~
Requires: httpd >= 2.0.46-32
Requires: mysql-server >= 3.23.58
Requires: php >= 4.3.2-11
Requires: php-mysql >= 4.3.2-11
Requires: freetype >= 2.1.4
Requires: sendmail >= 8.12.11
Requires: libjpeg >= 6b
Requires: libtiff >= 3.5.7
Requires: XFree86-libs >= 4.3.0
Requires: bzip2-libs >= 1.0.2
Requires: libpng10 >= 1.0.13

Provides: libbz2.so.0