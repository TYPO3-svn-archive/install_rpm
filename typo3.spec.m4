m4_dnl
m4_dnl	TYPO3 Core package RPM spec
m4_dnl
m4_sinclude(typo3-common.spec)

Name: typo3
Version: %typo_version
Release: %rpm_release
ExclusiveArch: noarch
Summary: TYPO3 CMS Core

Source0: typo3_src-%typo_version.tar.gz
Source1: typo3.%rpm_flavor.tgz
Patch0: typo3.patch

m4_dnl  Platform-specific requires
m4_ifelse(m4_rpm_flavor, `RH', `
Requires: httpd >= 2.0.40
Requires: mysql-server >= 3.23.54
Requires: mysql >= 3.23.54
Requires: php >= 4.2.2
Requires: php-mysql >= 4.2.2
Requires: freetype >= 2.1.3
')
m4_ifelse(m4_rpm_flavor, `SuSE', `
Requires: mysql >= 4.0.18
Requires: mysql-client >= 4.0.18
Requires: apache2 >= 2.0.49
Requires: php4 >= 4.3.4
Requires: apache2-mod_php4
Requires: php4-mysql
Requires: php4-pear
Requires: php4-zlib
Requires: php4-curl
Requires: php4-mbstring
Requires: php4-gd
Requires: freetype2
')
AutoReqProv: no
Provides: typo3-flavor-%rpm_flavor

%description
TYPO3 is an enterprise-class Web Content Management System 
written in PHP/MySQL. To find out more, see:

http://www.typo3.org

%prep
%__rm -rf %_builddir/quickstart*
%__rm -rf %_builddir/typo*
%__rm -rf %buildroot
%setup -q -b 1 -n typo3_src-%typo_version
%patch

%build

%install
# Copy all TYPO3 Sources, set permissions and create typo3 symlink
TYPOLIB="%{buildroot}%{typo_libdir}"
%__mkdir_p $TYPOLIB
%__cp --recursive * --target-directory=$TYPOLIB
# Now let's add/replace our custom files
%__cp --recursive ../typo3.%rpm_flavor/* --target-directory=%buildroot
# Fix permissions
%__chmod -R g+w,o-rwx $TYPOLIB
%__chmod -R g-w $TYPOLIB/common

%clean
%__rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root,%apache_group)
%typo_libdir
%typo_sitedir

%post
%typo_libdir/tools/setdatetimeformat --force

%postun

%changelog
* Fri Jul 16 2004 Dimitri Tarassenko <mitka@mitka.us> 3.6.2-0.6
- make+m4 processing implemented instead of shell scripts
- update to 3.6.2
- added our IM 4.2.9 to paths list used by install tool
* Fri Jun 02 2004 Dimitri Tarassenko <mitka@mitka.us> 3.6.1-0.5a
- common macro header introduced