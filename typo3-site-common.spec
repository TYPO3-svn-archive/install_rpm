m4_dnl
m4_dnl 	Common Spec parts for all Site Packages
m4_dnl  ************************************************************************
m4_dnl
m4_dnl
m4_dnl	========================================================================
m4_dnl	Let's create macros for switching MySQL to bypass-password mode and back
m4_dnl
m4_define( m4_mysqld, 
    m4_ifelse( m4_rpm_flavor, `RH', `service mysqld', 
    m4_ifelse( m4_rpm_flavor, `SuSE', `/etc/init.d/mysql')))m4_dnl
m4_dnl .........................................
m4_dnl 
m4_define( m4_make_sure, `m4_dnl
# make sure "$1" is really executed!
	for x in 1 2 3 4 5; do
	    $1
	    if [ $? -eq 0 ]; then
	        break;
	    else
		echo "Failed [$?], retrying $x : $1"
	        sleep 5
	    fi
	done
')m4_dnl
m4_dnl .........................................
m4_dnl 
m4_define( m4_mysql_whore, `m4_dnl
# fix the config
MYCONF="/etc/my.cnf"
cp -pf $MYCONF $MYCONF.TYPO-SAVE
cat >> $MYCONF <<EOF
; Switch to passwordless mode temporarily
[mysqld]
skip-grant-tables
EOF
# restart mysql in passwordless mode now
m4_mysqld status > /dev/null
if [ $? -eq 0 ]; then
    m4_make_sure( m4_mysqld `stop' )
    m4_make_sure( m4_mysqld `start' )
else
    m4_make_sure( m4_mysqld `start' )
fi
sleep 10
')m4_dnl
m4_dnl .........................................
m4_dnl
m4_define( m4_mysql_virgin, `m4_dnl
# restore the config
MYCONF="/etc/my.cnf"
mv -f $MYCONF.TYPO-SAVE $MYCONF
# restart mysql in normal mode
m4_make_sure( m4_mysqld `stop' )
m4_make_sure( m4_mysqld `start' )
')m4_dnl
m4_dnl .........................................
m4_dnl
m4_define( m4_httpd, 
    m4_ifelse( m4_rpm_flavor, `RH', `service httpd', 
    m4_ifelse( m4_rpm_flavor, `SuSE', `/etc/init.d/apache2')))m4_dnl
m4_define( m4_apache_restart, `m4_dnl
# restart Apache
m4_httpd status > /dev/null
if [ "$?" == "0" ]; then
    m4_httpd reload > /dev/null
fi
')m4_dnl
m4_dnl
m4_dnl ***************************************************************************
m4_dnl
Name: typo3-site-%site_name
Summary: TYPO3 Test Site "%site_name"
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
Source0: %site_name-%typo_version.tar.gz
Source1: %site_name.%rpm_flavor.tgz
Patch0: %site_name.patch

%description
TYPO3 is an enterprise-class Web Content Management System 
written in PHP/MySQL. To find out more, see:

http://www.typo3.org

'%site_name' is a test website for TYPO3.

%prep
%__rm -rf %buildroot
%setup -q -b 1 -n %site_name-%typo_version
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
m4_ifelse(m4_rpm_flavor, `RH', `%config /etc/httpd/conf.d/typo3-%site_name.conf')
m4_ifelse(m4_rpm_flavor, `SuSE', `%config /etc/apache2/vhosts.d/typo3-%site_name.conf')

%post
m4_mysql_whore
# create the MySQL user and database
/usr/bin/mysql -e "create database t3%{site_name};"
/usr/bin/mysql mysql -e "INSERT INTO user (Host,User,Password) \
    VALUES('localhost','t3%{site_name}',PASSWORD('t3%{site_name}'));"
/usr/bin/mysql mysql -e "INSERT INTO db \
    (Host,Db,User,Select_priv,Insert_priv,Update_priv,Delete_priv,Create_priv,Drop_priv) \
    VALUES('localhost','t3%{site_name}','t3%{site_name}','Y','Y','Y','Y','Y','Y');"
/usr/bin/mysql t3%{site_name} < %typo_sitedir/%site_name/typo3conf/database.sql
m4_mysql_virgin
m4_ifelse( m4_rpm_flavor, `SuSE', `m4_dnl
# Make sure apache2 has mod_rewrite on SuSE
AP2CFG="/etc/sysconfig/apache2"
if [ ! "`grep "^APACHE_MODULES.*rewrite" $AP2CFG`" ]; then
	awk '{ if ( match ($0, /^APACHE_MODULES=(.*)\"$/, r)) print "APACHE_MODULES=" r[1] " rewrite\""; else print }'  $AP2CFG > $AP2CFG.new
	mv -f $AP2CFG.new $AP2CFG
fi
')m4_dnl
m4_apache_restart

%preun
%__rm -rf %typo_sitedir/%site_name/typo3temp/*
%__rm -rf %typo_sitedir/%site_name/typo3conf/temp*

%postun
m4_mysql_whore
/usr/bin/mysql -e "delete from mysql.user where User='t3%site_name';"
/usr/bin/mysql -e "delete from mysql.db where User='t3%site_name';"
/usr/bin/mysql -e "drop database t3%site_name;"
/usr/bin/mysql -e "flush privileges;"
m4_make_sure ( m4_mysqld stop )
%__rm -rf /var/lib/mysql/t3%site_name
m4_mysql_virgin
m4_apache_restart

%changelog
* Sun Nov 14 2004 Dimitri Tarassenko <mitka@mitka.us> 3.6.2-0.6
- updated to 3.7.0
* Fri Jul 16 2004 Dimitri Tarassenko <mitka@mitka.us> 3.6.2-0.6
- mysql password protected root acct circumvented
- makefiles written instead of build scripts
- updated to 3.6.2
* Wed Jun 02 2004 Dimitri Tarassenko <mitka@mitka.us> 3.6.1-0.5a
- common macros used
