# setup CABLE repo

Repository to checkout & build a svn development branch

To get started:

    # this is wherever you personal plan to develop the code
    $ cd CABLE/src

    # where test is what you wish to call the repo
    $ git clone https://github.com/mdekauwe/CABLE_setup.git test

To work, the expectation is that the user will update the relevant entries (e.g. repo name, etc) within:

    $ ./get_cable_repo.py

    #------------- User set stuff ------------- #
    user = "XXX579"

    ...
    # ------------------------------------------- #


NB. to self, deleta a branch:

```bash
$ svn rm https://trac.nci.org.au/svn/cable/branches/Users/mgk576/CABLE-trunk -m "Deleting branch"
```

## Contacts

* [Martin De Kauwe](http://mdekauwe.github.io/)
