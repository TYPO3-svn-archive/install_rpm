#
#  RPM Spec file for
#  Dimitri Tarassenko <m1tk4@hotmail.com>
#
#  $Date$	$Revision$ $Name$
#

Name: typo3-site-quickstart
Version: ~~TYPOVERSION~~
ExclusiveArch: i386
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
QUICKDIR="%buildroot/var/typo3/quickstart-~~TYPOVERSION~~"
%__mkdir_p $QUICKDIR
%__cp --recursive * --target-directory=$QUICKDIR
%__ln_s quickstart-~~TYPOVERSION~~ %buildroot/var/typo3/quickstart
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
/var/typo3/quickstart-~~TYPOVERSION~~
/var/typo3/quickstart
%defattr(-, root,root)
/etc/httpd/conf.d/typo3-quickstart.conf

%post
# create the MySQL user and database
service mysqld status > /dev/null
if [ "$?" != "0" ]; then
    # let's try starting mysql
    service mysqld start
fi
/usr/bin/mysql -e "grant all privileges on t3quickstart.* to 't3quickstart'@'localhost' identified by 't3quickstart' WITH Grant option;"



%postun
# IMPORTANT!!! CLEAN UP ALL TEMPS IN var/typo3/quickstart!!!
%__rm -rf /var/typo3/quickstart*




#%changelog ??

# Copy all the


# redhat = %_host_vendor 
# DEBUG: check that it's the same on SuSE!!
