#
#  RPM Spec file for all Packages.
#  Mostly it contains defines and stuff that is the same for all of them
#  Dimitri Tarassenko <m1tk4@hotmail.com>
#
#  $Date$	$Revision$ $Name$
#

%define	typo_version	3.6.1

#RH:    %define	rpm_flavor	RH
#SuSE:  %define rpm_flavor	SuSE

%define	rpm_release	0.4%rpm_flavor

#RH:	%define	apache_group	apache
#SuSE:	%define	apache_group	www

%define	typo_libdir	/usr/lib/typo3
%define typo_sitedir	/var/typo3


# Stuff that's the same for all of them
Copyright: GPL/Freeware (see contents)
Vendor: http://typo3.mitka.us
Packager: Dimitri Tarassenko <mitka.mitka.us>
Group: Applications/Internet
Distribution: TYPO3 %typo_version
BuildRoot: /var/tmp/%{name}

