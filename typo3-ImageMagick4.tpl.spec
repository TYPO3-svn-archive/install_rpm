#
#  RPM Spec file for Quickstart test site of TYPO3
#  Dimitri Tarassenko <m1tk4@hotmail.com>
#
#  $Date$	$Revision$ $Name$
#

Name: typo3-ImageMagick4
Version: 4.2.9
Release: ~~RPMRELEASE~~
Copyright: freeware
Vendor: http://typo3.mitka.us
Packager: Dimitri Tarassenko <mitka@mitka.us>
Summary: ImageMagick 4.2.9 for TYPO3
Group: Applications/Multimedia
Distribution: TYPO3

BuildRoot: /var/tmp/%{name}
Prefix: /usr/lib/typo3/ImageMagick4

BuildRequires: libpng-devel
BuildRequires: libjpeg-devel
BuildRequires: libtiff-devel
BuildRequires: zlib-devel

Source0: ftp://ftp.wizards.dupont.com/pub/ImageMagick/ImageMagick-%{version}.tar.gz
Source1: ImageMagick4.tar.gz

Patch0: ImageMagick-4.2.9-delegates.patch

%description
ImageMagick(TM) is an image display and manipulation tool for the X
Window System.  ImageMagick can read and write JPEG, TIFF, PNM, GIF
and Photo CD image formats.  It can resize, rotate, sharpen, color
reduce or add special effects to an image, and when finished you can
either save the completed work in the original format or a different
one.  ImageMagick also includes command line programs for creating
animated or transparent .gifs, creating composite images, creating
thumbnail images, and more.
                                                                                                          
This version of ImageMagick is a custom build made specifically
for TYPO3 Content Management System

%prep
%setup -b 1 -n ImageMagick-%{version}
%patch -b .delegates

%build
%configure \
   --disable-shared \
   --enable-static \
   --enable-lzw \
   --without-perl \
   --without-ttf \
   --without-x
%__make

%install
%__rm -rf $RPM_BUILD_ROOT
%__mkdir_p $RPM_BUILD_ROOT/usr/lib/typo3/ImageMagick4
%__mv -f combine identify convert README.txt  delegates/delegates.mgk $RPM_BUILD_ROOT/usr/lib/typo3/ImageMagick4
%__cp --recursive ../ImageMagick4/* --target-directory=$RPM_BUILD_ROOT

%clean
%__rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
/usr/lib/typo3/ImageMagick4

