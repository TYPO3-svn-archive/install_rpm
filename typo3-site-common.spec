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
#RH:	Requires: typo3-flavor-RedHat
#SuSE:	Requires: typo3-flavor-SuSE
Requires: coreutils, grep, gawk

AutoReqProv: no
Provides: typo3-site

BuildRoot: /var/tmp/%{name}

