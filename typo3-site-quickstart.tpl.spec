#
#  RPM Spec file for Quickstart test site of TYPO3
#  Dimitri Tarassenko <m1tk4@hotmail.com>
#
#  $Date$	$Revision$ $Name$
#

Name: typo3-site-quickstart
Summary: TYPO3 Test Site "Quickstart"

Source0: quickstart-~~TYPOVERSION~~.tar.gz
Source1: quickstart.tar.gz
Patch0: quickstart.patch

%description
TYPO3 is an enterprise-class Web Content Management System 
written in PHP/MySQL. To find out more, see:

http://www.typo3.org

%prep
%__rm -rf %_builddir/quickstart*
%__rm -rf %buildroot
%setup -b 1 -n quickstart-~~TYPOVERSION~~
%patch

%build

%install

# Copy all sources, set permissions and create typo3 symlink
QUICKDIR="%buildroot/var/typo3/quickstart"
%__mkdir_p $QUICKDIR
%__cp --recursive * --target-directory=$QUICKDIR
# Now let's add/replace our custom files
#RH:	%__cp --recursive ../quickstart.RH/* --target-directory=%buildroot
#SuSE:	%__cp --recursive ../quickstart.SuSE/* --target-directory=%buildroot
# Fix the typo3 core symlink
%__rm -f $QUICKDIR/typo3_src
%__ln_s /usr/lib/typo3 $QUICKDIR/typo3_src 

# Fix permissions
%__chown -R root:apache $QUICKDIR
%__chmod -R g+w,o-rwx $QUICKDIR

%clean
%__rm -rf $RPM_BUILD_ROOT

%files
#RH:	%defattr(-, root,apache)
#SuSE:	%defattr(-, root,www)
/var/typo3/quickstart
%defattr(-, root,root)
#RH:	%config /etc/httpd/conf.d/typo3-quickstart.conf
#SuSE:	%config /etc/apache2/vhosts.d/typo3-quickstart.conf

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
/usr/bin/mysql -e "create database t3quickstart;"
/usr/bin/mysql -e "grant all privileges on t3quickstart.* to 't3quickstart'@'localhost' identified by 't3quickstart' WITH Grant option;"
/usr/bin/mysql t3quickstart < /var/typo3/quickstart/typo3conf/database.sql
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
%__rm -rf /var/typo3/quickstart/typo3temp/*
%__rm -rf /var/typo3/quickstart/typo3conf/temp*

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
/usr/bin/mysql -e "drop database t3quickstart; delete from mysql.user where User='t3quickstart'; flush privileges; "
%__rm -rf /var/lib/mysql/t3quickstart
$MYSQLD restart > /dev/null
$HTTPD status > /dev/null
if [ "$?" == "0" ]; then
    $HTTPD reload > /dev/null
fi

