SHELL = /bin/bash

typo_version := $(shell cat VERSION)
rpm_release = 0.7

allsites = quickstart testsite dummy
alltargets = typo3 imagemagick $(allsites)

typo_tarball = src/typo3_src-$(typo_version).tar.gz
typo_rpms = \
    rpm/typo3-$(typo_version)-$(rpm_release)RH.noarch.rpm \
    rpm/typo3-$(typo_version)-$(rpm_release)SuSE.noarch.rpm
    
imagick_release = 	1.3
imagick_tarball = 	src/ImageMagick-4.2.9.tar.gz
imagick_rpm = 		rpm/typo3-ImageMagick4-4.2.9-$(imagick_release).i386.rpm
imagick_patch = 	ImageMagick-4.2.9-delegates.patch

quickstart_tarball = 	src/quickstart-$(typo_version).tar.gz
testsite_tarball = 	src/testsite-$(typo_version).tar.gz
dummy_tarball = 	src/dummy-$(typo_version).tar.gz

quickstart_rpms = \
    rpm/typo3-site-quickstart-$(typo_version)-$(rpm_release)RH.noarch.rpm \
    rpm/typo3-site-quickstart-$(typo_version)-$(rpm_release)SuSE.noarch.rpm

dummy_rpms = \
    rpm/typo3-site-dummy-$(typo_version)-$(rpm_release)RH.noarch.rpm \
    rpm/typo3-site-dummy-$(typo_version)-$(rpm_release)SuSE.noarch.rpm

testsite_rpms = \
    rpm/typo3-site-testsite-$(typo_version)-$(rpm_release)RH.noarch.rpm \
    rpm/typo3-site-testsite-$(typo_version)-$(rpm_release)SuSE.noarch.rpm

#    rpm/typo3-site-dummy-$(typo_version)-$(rpm_release)RH.noarch.rpm
    
# list of all tarballs and other files required for building that are not in cvs
all_required = \
    $(typo_tarball) \
    $(imagick_tarball) \
    $(quickstart_tarball) \
    $(testsite_tarball)
    
# list of all rpms
all_rpms = \
    $(typo_rpms) \
    $(imagick_rpm) \
    $(quickstart_rpms) \
    $(dummy_rpms) \
    $(testsite_rpms)
    
# RPM directories
# TODO: have to determine if SuSE
rpm_dir = /usr/src/redhat/RPMS
src_dir = /usr/src/redhat/SOURCES

# Signature Key
gpg_key_name = TYPO3 RPM Key


# --- main targets ------------------------------------------

#debug: clean typo3

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

dummy: $(dummy_rpms)

testsite: $(testsite_rpms)

sign:	all
#	mv -f ~/.rpmmacros ~/.rpmmacros.sav
#	echo "%_gpg_name $(gpg_key_name)" >> ~/.rpmmacros
#	echo "%_signature gpg" >> ~/.rpmmacros
#	echo " " >> ~/.rpmmacros
#	echo "Signing packages:"
	chmod og-rwx ./keys
	rpm \
	    --define "_gpg_name $(gpg_key_name)" \
	    --define "_signature gpg" \
	    --define "_gpg_path ./keys" \
	    --resign $(all_rpms) \
	    2>&1
#	mv -f ~/.rpmmacros.sav ~/.rpmmacros

clean:
	rm -rf \
	    $(quickstart_rpms)\
	    $(dummy_rpms)\
	    $(testsite_rpms)\
	    $(dir $(rpm_dir))/BUILD/quickstart* \
	    $(dir $(rpm_dir))/BUILD/dummy* \
	    $(dir $(rpm_dir))/BUILD/testsite* \
	    
	rm -rf $(typo_rpms)
# debug!!!
	rm -rf $(src_dir)/*.spec
	
#	    $(imagick_rpm) \
#	    $(src_dir)/$(notdir $(imagick_tarball)) \
#	    $(src_dir)/ImageMagick4.tgz

clean_dummy:
	rm -rf \
	    $(dummy_rpms)\
	    $(dir $(rpm_dir))/BUILD/dummy* \
	    $(src_dir)/dummy* \
	    $(src_dir)/typo3-site-dummy* \

clean_quickstart:
	rm -rf \
	    $(quickstart_rpms)\
	    $(dir $(rpm_dir))/BUILD/quickstart* \
	    $(src_dir)/quickstart* \
	    $(src_dir)/typo3-site-quickstart* \

clean_testsite:
	rm -rf \
	    $(testsite_rpms)\
	    $(dir $(rpm_dir))/BUILD/testsite* \
	    $(src_dir)/testsite* \
	    $(src_dir)/typo3-site-testsite* \

# --- typo3 source rpm building
$(rpm_dir)/noarch/typo3-$(typo_version)-$(rpm_release)%.noarch.rpm: \
    $(src_dir)/typo3.%.spec \
    $(src_dir)/typo3.patch \
    $(src_dir)/typo3.%.tgz \
    $(src_dir)/$(notdir $(typo_tarball))
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
#.PRECIOUS: $(src_dir)/%.spec
$(src_dir)/%.spec: \
    typo3-common.spec \
    typo3-site-common.spec
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
