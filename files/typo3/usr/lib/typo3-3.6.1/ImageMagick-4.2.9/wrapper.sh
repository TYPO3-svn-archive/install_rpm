#!/bin/sh
# This is a wrapper for all ImageMagick programs.
# It solves the problem that delegates.mgk cannot be found.

# Define im_path, telling us where this script actually is
im_path=`dirname $0`

# Set path to delegates.mgk
export DELEGATE_PATH=${im_path}

# Absolute program path
${im_path}/bin/`basename $0` "$@"

exit 0
