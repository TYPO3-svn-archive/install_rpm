#
#  Common typo3-site- main part.
#  It goes AFTER the package header in the assembled .spec
#  Dimitri Tarassenko <m1tk4@hotmail.com>
#
#  $Date$	$Revision$ $Name$
#

#  NOTE: %site_name has to be defined at this point!!!


Version: %typo_version
Release: %rpm_release

ExclusiveArch: noarch

Requires: typo3 >= %typo_version
Requires: typo3-ImageMagick4
Requires: typo3-flavor-%rpm_flavor
Requires: coreutils, grep, gawk

AutoReqProv: no
Provides: typo3-site

BuildRoot: /var/tmp/%{name}

Name: typo3-site-%site_name
Summary: TYPO3 Test Site "%site_name"

Source0: %site_name-%typo_version.tar.gz
Source1: %site_name.tar.gz
Patch0: %site_name.patch

%description
TYPO3 is an enterprise-class Web Content Management System 
written in PHP/MySQL. To find out more, see:

http://www.typo3.org

'%site_name' is a test website for TYPO3.

%prep
#%__rm -rf %_builddir/%_site_name*
%__rm -rf %buildroot
#echo "--%site_name--"
#echo "--%typo_version--"
%setup -b 1 -n %site_name-%typo_version
%patch

%build

%install

# Copy all sources, set permissions and create typo3 symlink
QUICKDIR="%{buildroot}%{typo_sitedir}/%site_name"
%__mkdir_p $QUICKDIR
%__cp --recursive * --target-directory=$QUICKDIR
# Now let's add/replace our custom files
%__cp --recursive ../%site_name.%rpm_flavor/* --target-directory=%buildroot
# Fix the typo3 core symlink
%__rm -f $QUICKDIR/typo3_src
%__ln_s /usr/lib/typo3 $QUICKDIR/typo3_src 

# Fix permissions
%__chmod -R g+w,o-rwx $QUICKDIR

%clean
%__rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, %apache_group)
%typo_sitedir/%site_name

%defattr(-, root, root)
#RH:	%config /etc/httpd/conf.d/typo3-%site_name.conf
#SuSE:	%config /etc/apache2/vhosts.d/typo3-%site_name.conf

%post
#RH:	MYSQLD="service mysqld"
#SuSE:	MYSQLD="/etc/init.d/mysql"
#RH:	HTTPD="service httpd"
#SuSE:	HTTPD="/etc/init.d/apache2"
# create the MySQL user and database
$MYSQLD status > /dev/null
if [ "$?" != "0" ]; then
    # let's try starting mysql
    $MYSQLD start
    /bin/sleep 5
fi
/usr/bin/mysql -e "create database t3%{site_name};"
/usr/bin/mysql -e "grant all privileges on t3%{site_name}.* to 't3%{site_name}'@'localhost' identified by 't3%{site_name}' WITH Grant option;"
/usr/bin/mysql t3%{site_name} < %typo_sitedir/%site_name/typo3conf/database.sql
# Make sure apache2 has mod_rewrite on SuSE
#SuSE:	AP2CFG="/etc/sysconfig/apache2"
#SuSE:	if [ ! "`grep "^APACHE_MODULES.*rewrite" $AP2CFG`" ]; then
#SuSE:		awk '{ if ( match ($0, /^APACHE_MODULES=(.*)\"$/, r)) print "APACHE_MODULES=" r[1] " rewrite\""; else print }'  $AP2CFG > $AP2CFG.new
#SuSE:		mv -f $AP2CFG.new $AP2CFG
#SuSE:	fi

# restart Apache
$HTTPD status > /dev/null
if [ "$?" == "0" ]; then
    $HTTPD reload > /dev/null
fi

%preun
%__rm -rf %typo_sitedir/%site_name/typo3temp/*
%__rm -rf %typo_sitedir/%site_name/typo3conf/temp*

%postun
#RH:	MYSQLD="service mysqld"
#SuSE:	MYSQLD="/etc/init.d/mysql"
#RH:	HTTPD="service httpd"
#SuSE:	HTTPD="/etc/init.d/apache2"
$MYSQLD status > /dev/null
if [ "$?" != "0" ]; then
    # let's try starting mysql
    $MYSQLD start
    /bin/sleep 5
fi
/usr/bin/mysql -e "drop database t3%site_name; delete from mysql.user where User='t3%site_name'; flush privileges; "
$MYSQLD stop > /dev/null
%__rm -rf /var/lib/mysql/t3%site_name
$MYSQLD start > /dev/null
$HTTPD status > /dev/null
if [ "$?" == "0" ]; then
    $HTTPD reload > /dev/null
fi

%changelog

* Wed Jun 02 2004 Dimitri Tarassenko <mitka@mitka.us> 3.6.1-0.5a
- common macros used
