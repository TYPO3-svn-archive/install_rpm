#
#  Common typo3-site- requirements header
#  Dimitri Tarassenko <m1tk4@hotmail.com>
#
#  $Date$	$Revision$ $Name$
#

Version: ~~TYPOVERSION~~
#RH: 	Release: ~~RPMRELEASE~~RH
#SuSE:	Release: ~~RPMRELEASE~~SuSE
ExclusiveArch: noarch
Copyright: GPL
Vendor: http://typo3.mitka.us
Packager: Dimitri Tarassenko <mitka@mitka.us>
Group: Applications/Internet
Distribution: TYPO3 

Requires: typo3 >= ~~TYPOVERSION~~
Requires: typo3-ImageMagick4

#RH:	Requires: httpd >= 2.0.40
#SuSE:	Requires: apache2 >= 2.0.49

#RH:	Requires: mysql-server >= 3.23.54
#RH:	Requires: mysql >= 3.23.54
#SuSE:  Requires: mysql >= 4.0.18
#SuSE:  Requires: mysql-client: >= 4.0.18

#RH:	Requires: php >= 4.2.2
#RH:	Requires: php-mysql >= 4.2.2
#SuSE:	Requires: php4 >= 4.3.4
#SuSE:	Requires: apache2-mod_php4
#SuSE:	Requires: php4-mysql
#SuSE:	Requires: php4-pear
#SuSE:	Requires: php4-zlib
#SuSE:	Requires: php4-curl
#SuSE:	Requires: php4-mbstring
#SuSE:	Requires: php4-gd

#RH:	Requires: freetype >= 2.1.3
#SuSE:	Requires: freetype2

AutoReqProv: no

Provides: typo3-site

BuildRoot: /var/tmp/%{name}

