#
#  RPM Spec file for TYPO3 Core Package
#  Dimitri Tarassenko <m1tk4@hotmail.com>
#
#  $Date$	$Revision$ $Name$
#

Name: typo3
Version: ~~TYPOVERSION~~
Release: ~~RPMRELEASE~~
ExclusiveArch: noarch
Copyright: GPL
Vendor: http://typo3.mitka.us
Packager: Dimitri Tarassenko <mitka.mitka.us>
Summary: TYPO3 CMS Core
Group: Applications/Internet
Distribution: TYPO3
BuildRoot: /var/tmp/%{name}

Source0: typo3_src-~~TYPOVERSION~~.tar.gz
Source1: typo3.tar.gz
Patch0: typo3.patch

Requires: typo3-site

AutoReqProv: no

%description
TYPO3 is an enterprise-class Web Content Management System 
written in PHP/MySQL. To find out more, see:

http://www.typo3.org

%prep
%__rm -rf %_builddir/quickstart*
%__rm -rf %_builddir/typo*
%__rm -rf %buildroot
%setup -b 1 -n typo3_src-~~TYPOVERSION~~
%patch

%build

%install
# Copy all TYPO3 Sources, set permissions and create typo3 symlink
TYPOLIB="%buildroot/usr/lib/typo3"
%__mkdir_p $TYPOLIB
%__cp --recursive * --target-directory=$TYPOLIB
# Now let's add/replace our custom files
%__cp --recursive ../typo3/* --target-directory=%buildroot
# Fix permissions
%__chown -R root:apache $TYPOLIB
%__chmod -R g+w,o-rwx $TYPOLIB

%clean
%__rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root,apache)
/usr/lib/typo3
/var/typo3

%post
/usr/lib/typo3/tools/setdatetimeformat --force

%postun


