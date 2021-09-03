#!/usr/bin/env python

"""
Get the head of the CABLE trunk, the user branch and CABLE-AUX

That's all folks.
"""

# __author__ = "Martin De Kauwe"
# __version__ = "1.0 (09.03.2019)"
# __email__ = "mdekauwe@gmail.com"

import os
import sys
import subprocess
import datetime

class GetCable(object):

    def __init__(self, src_dir=None, root="https://trac.nci.org.au/svn/cable",
                 user=None, copy_trunk=True):

        self.src_dir = src_dir
        self.root = root
        self.user = user
        self.msg="\"checked out repo\""
        self.aux_dir = "CABLE-AUX"
        self.copy_trunk = copy_trunk

    def main(self, repo_name=None, trunk=False):

        self.initialise_stuff()

        self.get_repo(repo_name, trunk=trunk)

    def initialise_stuff(self):

        if not os.path.exists(self.src_dir):
            os.makedirs(self.src_dir)

    def get_repo(self, repo_name, trunk=False):

        cwd = os.getcwd()
        os.chdir(self.src_dir)

        # Checkout the head of the trunk ...
        if trunk:

            # Check if we have a local copy of the trunk, if we do we won't
            # write over this, otherwise we will check one out
            cmd = "svn info %s/branches/Users/%s/%s" % \
                    (self.root, self.user, repo_name)

            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT)
            output, error = p.communicate()
            if error == 1:
                raise("Error checking if repo exists")

            if "non-existent" in str(output) or "problem" in str(output) and \
                self.copy_trunk:
                cmd = "svn copy %s/trunk %s/branches/Users/%s/%s -m %s" % \
                        (self.root, self.root, self.user, repo_name, self.msg)
                error = subprocess.call(cmd, shell=True)
                if error == 1:
                    raise("Error copying repo to local space")

            cmd = "svn checkout %s/branches/Users/%s/%s" % \
                    (self.root, self.user, repo_name)
            error = subprocess.call(cmd, shell=True)
            if error == 1:
                raise("Error downloading repo")

        # Checkout named branch ...
        else:

            # Check if we have a local copy of the branch?
            cmd = "svn info %s" % (repo_name)
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT)
            output, error = p.communicate()
            if error == 1:
                raise("Error checking if repo exists")

            if "non-existent" in str(output):
                cmd = "svn copy %s -m %s" % (repo_name, self.msg)
                error = subprocess.call(cmd, shell=True)
                if error == 1:
                    raise("Error copying repo to local space")

            cmd = "svn checkout %s" % (repo_name)
            error = subprocess.call(cmd, shell=True)
            if error == 1:
                raise("Error downloading repo")

        os.chdir(cwd)

    def get_aux(self):

        # Checkout CABLE-AUX
        if not os.path.exists(self.aux_dir):
            cmd = "svn checkout %s/branches/Share/%s %s" % \
                    (self.root, self.aux_dir, self.aux_dir)
            error = subprocess.call(cmd, shell=True)
            if error == 1:
                raise("Error checking out CABLE-AUX")


if __name__ == "__main__":

    #------------- Change stuff ------------- #
    cwd = os.getcwd()
    #src_dir = "src"
    src_dir = cwd
    user = "sr2710"
    #repo = "https://trac.nci.org.au/svn/cable/branches/Users/mgk576/trunk_covid"
    repo = "https://trac.nci.org.au/svn/cable/trunk"
    #repo = "trunk"
    # ------------------------------------------- #

    G = GetCable(src_dir=src_dir, user=user, copy_trunk=False)
    #G.main(repo_name=repo, trunk=True)
    G.main(repo_name=repo, trunk=False)
