#
#  RPM Spec file for TYPO3 Core Package
#  Dimitri Tarassenko <m1tk4@hotmail.com>
#
#  $Date$	$Revision$ $Name$
#

Name: typo3
Version: %typo_version
Release: %rpm_release
ExclusiveArch: noarch
Summary: TYPO3 CMS Core

Source0: typo3_src-%typo_version.tar.gz
Source1: typo3.tar.gz
Patch0: typo3.patch

# -- Platform-specific requires

#RH:    Requires: httpd >= 2.0.40
#SuSE:  Requires: apache2 >= 2.0.49
                                                                                                      
#RH:    Requires: mysql-server >= 3.23.54
#RH:    Requires: mysql >= 3.23.54
#SuSE:  Requires: mysql >= 4.0.18
#SuSE:  Requires: mysql-client >= 4.0.18
                                                                                                      
#RH:    Requires: php >= 4.2.2
#RH:    Requires: php-mysql >= 4.2.2
#SuSE:  Requires: php4 >= 4.3.4
#SuSE:  Requires: apache2-mod_php4
#SuSE:  Requires: php4-mysql
#SuSE:  Requires: php4-pear
#SuSE:  Requires: php4-zlib
#SuSE:  Requires: php4-curl
#SuSE:  Requires: php4-mbstring
#SuSE:  Requires: php4-gd
                                                                                                      
#RH:    Requires: freetype >= 2.1.3
#SuSE:  Requires: freetype2
                                                                                                      
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
%setup -b 1 -n typo3_src-%typo_version
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

* Fri Jun 02 2004 Dimitri Tarassenko <mitka@mitka.us> 3.6.1-0.5a
- common macro header introduced