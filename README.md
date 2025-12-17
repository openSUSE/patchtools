# SUSE Patch Tools

These python script allow easy manipulation of Linux patches, which makes
back-porting them much easier.

The configuration file will be installed in /etc/patch.cfg if /etc is writable.
Otherwise it is installed in ~/.local/etc/patch.cfg.

If you have installed this tool via an RPM or other package, you'll need
to copy the sample config file from /etc to ~/.local/etc/patch.cfg and edit
it to fit your site.

* Tools written by Jeff Mahoney <jeffm@suse.com>
* Setuptools integration by Lee Duncan <lduncan@suse.com>
* Conversion to Python3 by Tony Jones <tonyj@suse.de>

# Installation

To install this code on your system manually, you can use
something like the following:

    python3 -mpip install --prefix=/usr/local .

You will need permission to write in the /usr/local hierachy to do
this, and you will have to ensure any "patchtools" package on your
system is removed first.

Alternatively, you can install using a virtual environment. To do this,
create a virtual environment using something like:

    python3 -mvenv myvenv

This creates a virtual environment in the "myvenv" subdirectory. To
activate this, run (from the shell):

    source myvenv/bin/activate

Then, to install in this new virtual environment, run:

    python3 -mpip install --editable .

Now, if you run "which exportpatch", for example, you should
see the just-installed version. If you already have this tool installed
on your system, then the newly-installed version should show up first
in the list. When you are done, run "deactivate" to exit the virtual
environment.

# Testing

There is a "test" subdirectory, where you can find more information
on selftests.

In addition, whenever changes are made to the code, you can use the
"ruff" tool to check that your changes match the existing configuration.
For example, you can run:

    ruff check --target-version py311 --config pyproject.toml --preview

