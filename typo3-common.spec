m4_dnl	
m4_dnl	RPM Spec file for all Packages.
m4_dnl	Mostly it contains defines and stuff that is the same for all of them
m4_dnl	Dimitri Tarassenko <m1tk4@hotmail.com>
m4_dnl	
m4_dnl	
%define	typo_version	m4_typo_version
%define	rpm_flavor	m4_rpm_flavor
%define	rpm_release	m4_rpm_release()m4_rpm_flavor
m4_ifelse(m4_rpm_flavor, `RH', `%define	apache_group apache')
m4_ifelse(m4_rpm_flavor, `SuSE', `%define	apache_group www')
%define	typo_libdir	/usr/lib/typo3
%define typo_sitedir	/var/typo3

Copyright: GPL/Freeware (see contents)
Vendor: http://typo3.mitka.us
Packager: Dimitri Tarassenko <mitka@mitka.us>
Group: Applications/Internet
Distribution: TYPO3 %typo_version
BuildRoot: /var/tmp/%{name}

