#
#  RPM Spec file for Quickstart test site of TYPO3
#  Dimitri Tarassenko <m1tk4@hotmail.com>
#
#  $Date$	$Revision$ $Name$
#

Name: typo3-site-quickstart
Version: ~~TYPOVERSION~~
ExclusiveArch: noarch
Copyright: GPL
Vendor: Red Nex, Ltd.
Packager: Dimitri Tarassenko <m1tk4@hotmail.com>
Summary: TYPO3 Test Site "Quickstart"
Group: Applications/Internet
Requires: typo3 >= ~~TYPOVERSION~~
BuildRoot: /var/tmp/%{name}

Source0: quickstart-~~TYPOVERSION~~.tar.gz
Source1: quickstart.tar.gz
Patch0: quickstart.patch

%description
TYPO3 is an enterprise-class Web Content Management System 
written in PHP/MySQL. 

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
%__cp --recursive ../quickstart/* --target-directory=%buildroot
# Fix the typo3 core symlink
%__rm -f $QUICKDIR/typo3_src
%__ln_s /usr/lib/typo3 $QUICKDIR/typo3_src 

# Fix permissions
%__chown -R root:apache $QUICKDIR
%__chmod -R g+w,o-rwx $QUICKDIR

%clean

%files
%defattr(-, root,apache)
/var/typo3
%defattr(-, root,root)
/etc/httpd/conf.d/typo3-quickstart.conf

%post
# create the MySQL user and database
service mysqld status > /dev/null
if [ "$?" != "0" ]; then
    # let's try starting mysql
    service mysqld start
fi
/usr/bin/mysql -e "create database t3quickstart;"
/usr/bin/mysql -e "grant all privileges on t3quickstart.* to 't3quickstart'@'localhost' identified by 't3quickstart' WITH Grant option;"
/usr/bin/mysql t3quickstart < /var/typo3/quickstart/typo3conf/database.sql
# restart Apache
service httpd status > /dev/null
if [ "$?" == "0" ]; then
    service httpd reload > /dev/null
fi

%postun
%__rm -rf /var/typo3/quickstart*
/usr/bin/mysql -e "drop database t3quickstart; delete from mysql.user where User='t3quickstart'; flush privileges; "
%__rm -rf /var/lib/mysql/t3quickstart
service mysqld restart > /dev/null
service httpd status > /dev/null
if [ "$?" == "0" ]; then
    service httpd reload > /dev/null
fi

