SHELL = /bin/bash

typo_version := $(shell cat VERSION)
rpm_release = 0.6

alltargets = typo3 quickstart testsite dummy imagemagick
allsites = quickstart testsite dummy

typo_tarball = src/typo3_src-$(typo_version).tar.gz
typo_rpms = \
    rpm/typo3-$(typo_version)-$(rpm_release)RH.noarch.rpm \
    rpm/typo3-$(typo_version)-$(rpm_release)SuSE.noarch.rpm
    
imagick_release = 	1.2
imagick_tarball = 	src/ImageMagick-4.2.9.tar.gz
imagick_rpm = 		rpm/typo3-ImageMagick4-4.2.9-$(imagick_release).i386.rpm
imagick_patch = 	ImageMagick-4.2.9-delegates.patch

quickstart_tarball = 	src/quickstart-$(typo_version).tar.gz
testsite_tarball = 	src/testsite-$(typo_version).tar.gz
dummy_tarball = 	src/dummy-$(typo_version).tar.gz

quickstart_rpms = \
    rpm/typo3-site-quickstart-$(typo_version)-$(rpm_release)RH.noarch.rpm \
    rpm/typo3-site-quickstart-$(typo_version)-$(rpm_release)SuSE.noarch.rpm
    
# list of all tarballs and other files required for building that are not in cvs
all_required = \
    $(typo_tarball) \
    $(imagick_tarball) \
    $(quickstart_tarball) 
    
# RPM directories
# TODO: have to determine if SuSE
rpm_dir = /usr/src/redhat/RPMS
src_dir = /usr/src/redhat/SOURCES

# --- main targets ------------------------------------------

debug: clean quickstart

usage:
	@echo "TYPO3 RPM Builder - available targets:"
	@echo ""
	@echo "  typo3"
	@echo "  quickstart"
	@echo "  testsite"
	@echo "  dummy"
	@echo "  imagemagick"
	@echo "  all"
	@echo ""

all:	$(alltargets)

typo3:	$(typo_tarball) $(typo_rpms)

imagemagick: $(imagick_tarball) $(imagick_rpm)

quickstart: $(quickstart_rpms)

clean:
	rm -rf \
	    $(quickstart_rpms)\
	    $(dir $(rpm_dir))/BUILD/quickstart*
#	    $(imagick_rpm) \
#	    $(src_dir)/$(notdir $(imagick_tarball)) \
#	    $(src_dir)/ImageMagick4.tgz
#	rm -rf $(typo_rpms)
# debug!!!
	rm -rf $(src_dir)/*.spec


# --- typo3 source rpm building
$(rpm_dir)/noarch/typo3-$(typo_version)-$(rpm_release)%.noarch.rpm: \
    $(src_dir)/typo3.%.spec \
    $(src_dir)/$(notdir $(typo_tarball)) \
    $(src_dir)/typo3.%.tgz \
    $(src_dir)/typo3.patch
	rpmbuild -ba --target=noarch-redhat-linux $<

# --- IM 4.2.9
$(rpm_dir)/i386/$(notdir $(imagick_rpm)) : \
    $(src_dir)/typo3-ImageMagick4.spec \
    $(src_dir)/$(notdir $(imagick_tarball)) \
    $(src_dir)/ImageMagick4.tgz \
    src/$(imagick_patch)
	cp -uf src/$(imagick_patch) $(src_dir)/$(imagick_patch) 
	rpmbuild -ba --target=i386-redhat-linux $<
#	touch $@

# --- Site packages
$(rpm_dir)/noarch/typo3-site-%-$(typo_version)-$(rpm_release)RH.noarch.rpm \
$(rpm_dir)/noarch/typo3-site-%-$(typo_version)-$(rpm_release)SuSE.noarch.rpm : \
    $(src_dir)/%-$(typo_version).tar.gz \
    $(src_dir)/%.patch \
    $(src_dir)/typo3-site-%.RH.spec \
    $(src_dir)/typo3-site-%.SuSE.spec \
    $(src_dir)/%.RH.tgz \
    $(src_dir)/%.SuSE.tgz
	rpmbuild -ba --target=noarch-redhat-linux $(src_dir)/typo3-site-$*.RH.spec
	rpmbuild -ba --target=noarch-redhat-linux $(src_dir)/typo3-site-$*.SuSE.spec

# --- intermediate targets ---------------------------------------

# build the RPM spec using m4
.PRECIOUS: $(src_dir)/%.spec
$(src_dir)/%.spec:
	m4 --prefix-builtins \
	  --define=m4_rpm_flavor=$(subst .,,$(suffix $*)) \
	  --define=m4_typo_version=$(typo_version) \
	  --define=m4_rpm_release=$(rpm_release) \
	  --define=m4_imagick_release=$(imagick_release) \
	  $(basename $*).spec.m4 \
	  > $@

# fetching the rpms here
rpm/%.noarch.rpm: $(rpm_dir)/noarch/%.noarch.rpm
	cp -uf $< $@
rpm/%.i386.rpm: $(rpm_dir)/i386/%.i386.rpm
	cp -uf $< $@

# packing the overwrite/substitute files
#.PRECIOUS: $(src_dir)/%.tgz
$(src_dir)/%.tgz : files/%
	cd files; tar cvzf $@ --exclude=CVS $*/* >/dev/null

# copying the source tarballs
$(src_dir)/%.tar.gz: src/%.tar.gz
#	ln -s $< $@
	ln $< $@

# copying the patches
$(src_dir)/%.patch: patches/%.patch
	ln $< $@

# making sure stuff is in place
$(all_required):
	@echo " "
	@echo "ERROR: $(notdir $@) is missing."
	@echo "       This file is not in CVS. Please download it from"
	@echo "       http://www.typo3.org (or other place), saving it as "
	@echo "       $@ and try again."
	@echo " ";
	@exit 1;
