#
#  RPM Spec file for all TYPO3 Packages
#  Dimitri Tarassenko <m1tk4@hotmail.com>
#
#  $Date$	$Revision$ $Name$
#

Name: typo3
Version: ~~TYPOVERSION~~
ExclusiveArch: i386
Copyright: GPL
Vendor: Red Nex, Ltd.
Packager: Dimitri Tarassenko <m1tk4@hotmail.com>
Summary: TYPO3 CMS Core
Group: Applications/Internet
BuildRoot: /var/tmp/%{name}

Source0: typo3_src-~~TYPOVERSION~~.tar.gz
Source1: typo3.tar.gz

Patch0: typo3.patch

%description
TYPO3 is an enterprise-class Web Content Management System 
written in PHP/MySQL. 

%prep
%__rm -rf %_builddir/typo*
%__rm -rf %buildroot

%setup -b 1 -n typo3_src-~~TYPOVERSION~~
%patch

#read

%build


%install

# Copy all TYPO3 Sources, set permissions and create typo3 symlink
TYPOLIB="%buildroot/usr/lib/typo3-~~TYPOVERSION~~"
%__mkdir_p $TYPOLIB
%__cp --recursive * --target-directory=$TYPOLIB
%__ln_s typo3-~~TYPOVERSION~~ %buildroot/usr/lib/typo3

# Now let's add/replace our custom files
%__cp --recursive ../typo3/* --target-directory=%buildroot

%__chown -R root:apache $TYPOLIB
%__chmod -R g+w,o-rwx $TYPOLIB

# Copy all the


# redhat = %_host_vendor 
# DEBUG: check that it's the same on SuSE!!

%clean


%files
%defattr(-, root,apache)
/usr/lib/typo3-~~TYPOVERSION~~
/usr/lib/typo3
%defattr(-, root,root)
/usr/lib/lib*

%post
/sbin/ldconfig

%postun
/sbin/ldconfig


# some more packages
#%package

#%changelog ??

