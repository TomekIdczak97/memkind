#!/bin/bash
# SPDX-License-Identifier: BSD-2-Clause
# Copyright (C) 2019- 2020 Intel Corporation.

# docker_install_ndctl.sh - is called inside a Docker container;
# installs ndctl library
#

set -e

git clone --depth=1 --branch="$NDCTL_LIBRARY_VERSION" https://github.com/pmem/ndctl.git $HOME/ndctl/
cd $HOME/ndctl/

if [[ $(cat /etc/os-release) = *"fedora"* ]]; then

  rpmdev-setuptree

  SPEC=./rhel/ndctl.spec
  VERSION=$(./git-version)
  RPMDIR=$HOME/rpmbuild/

  git archive --format=tar --prefix="ndctl-${VERSION}/" HEAD | gzip > "$RPMDIR/SOURCES/ndctl-${VERSION}.tar.gz"

  ./autogen.sh
  ./configure --prefix=/usr --sysconfdir=/etc --libdir=/usr/lib --disable-docks
  make -j "$(nproc)"

  ./rpmbuild.sh

  RPM_ARCH=$(uname -m)
  rpm -i $RPMDIR/RPMS/$RPM_ARCH/*.rpm

else

  ./autogen.sh
  ./configure --prefix=/usr --sysconfdir=/etc --libdir=/usr/lib
  make -j "$(nproc)"

  sudo make -j "$(nproc)" install

fi
# update shared library cache
sudo ldconfig
# return to previous directory
cd -
rm -rf $HOME/ndctl
