# Testing for patchtools, using pyunit

## Version of Python

Currently, this report supports Python 3.6, 3.11, and 3.13,
but testing has been done on Python 3.6, since that's the
oldest version currently supported.

## What to test -- Which Scripts do we actually test?

These unit tests execute code in the source tree by running fixpatch:main
and exportpatch:main directly.

This allows the tests to be run on the source base, not the installed
(if any) package, and it allows code coverage to be measured when
testing.

## How to test

The pyunit unit testing framework is used, aka unittest.

The tests all live in the "test/" subdirectory, with a "data/"
subdirectory under it, where known good patchfiles exist,

For configuration, the tests create their own configuration file,
with the bogus user name and email address, so that the tests can
be user-independant. The tests also requires a valid Linux
git repository whos pathname is passed to the tests via the
"LINUX\_GIT" environment variable. This repository should be
up to date, and point to a valid Linux upstream repo, such as:

    git://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git


## Things to test

### exportpatch (testing at 100% now)

#### error conditions

* bogus commit supplied (does not match anything)
* no commit supplied
* try to supply "HEAD" or "^" (should fail)
* incorrect patch config file (points to nothing?)
* no patch config file?
* try to write with no write permission in dir
* invalid directory supplied to write patch
* specify out-of-range starting number for a numbered patch
* trying to write a patch file when one already exists without --force (should get funky name)

* test with various (or missing) config file for what RFEPOs to search


#### normal ops

Export a simple commit, just one file, just one hunk:

* export to a dir/file, using defaults
  repeat with a suffix
* export to a dir/file, using numeric values,
  repeat with non-default starting number
  repeat with non-default width
* export to a dir/file, using 'force' to overwrite
  repeat without force set
* export to stdout
* export to current dir
* export to dir/file, testing single reference
* export to dir/file, with double reference
* export to dir/file, testing single reference
* export to dir/file, using 'signed-off-by'
* export two commits, using defauls


Extract testing:

* export to file, extract whole (single) file
* repeat with two files
* repeat with specified file not in patch w/one file
* repeat with specified file not in patch w/two files
* repeat with one of two files in patch specified
* repeat with multiple files and multiple 'x' options

Exclude testing:

* exclude only file in one-file commit
* exclude all files in multi-file commit with a pattern
* exclude all files in multi-file commit with repeated options
* exclude nothing (bogus path) from one-file commit
* exclude nothing (bogus path) from multi-file commit
* exclude two files from multi-file commit


#### error ops

Test bogus params, such as:

* bogus commit
* no commit
* bad arguments (short and long)
* num-width with no value
* illegal values for num-width? (range is 1 to 4)
  this is currently difficult, since out-of-range
  vlaues are silently ignored. We should test by checking
  the actual width of the output number string in a patch?
* test first-number
  with no commit and no number
  with bogus number and and bogus commit
  with bogus number and valid commit
  with number out of range (too small & too large)
* REFERENCE with no value
* export to a dir with errors
  export to dir but dirname not supplied
  dir does not exist
  dir is read only


### fixpatch

#### normal ops

* fix a patch -- defaults
  ensure it adds acked-by
  ensure it adds diffstat
  ensure it renames?
  (duplicate?)

Test params:

* test no-rename
* test with rename
* test adding a suffix
* test dry-run (should do nothing)
* test rename collision, wiht force
* test rename collision, without force
* test name-only
* test name-only with suffix
* test no-ack (-N)
* test no-diffstat (-D)
* test header-only (no-ack and no-diffstat) (-H)
* test update-only (no-ack, no-diffstat, no-rename) (-U)
* test setting 1st reference (-F <ref>)
* test setting 2nd reference (-F <ref>)
* test with multiple references
* test header-only and a reference (-H -F <ref>)
* test signed-off-by (vs normal acked-by) (-S)
* test setting single dummy mainline tag (-M <mainline>)
* test setting two dummy mainline tags (-M <mainline> twice)
* test adding reference that already exist
* test with Signed-off-by already present

#### error conditions

* no patch filename specified
* pathname specified does not exist
* no rename but source patch is not writable
* patch directory not writable
* empty patch (so no Subject line)
* patch with just Subject, which has:
  no seperator
  no commit
  no from
  first signed-off-by
* patch with just Subject and ref
* patch with just Subject and signed-off-by already there

-- DONE TO HERE --

* patch with valid patch that has bogus Patch-mainline              -- XXX to do
* test with having 'Git-commit' already in patch                    -- XXX soon

* patch specified doesn't exist upstream? (i.e. a fake patch)
  (not sure what will happen here)

* patch after rename exists but is not writable
  (never mind -- it won't write over an existing patch filename)


### generic stuff

#### config.cfg

Right now the only generic stuff is reading the config file,
because that's done in the init file of the patchtools module.

It _should_ be read later, IMHO, which would make easier?

How do we test it now, with the config file being read way
before any test case is read?

An even better fix would be to make the config setup externally
available, so it could be tested separately.

### patch.cfg

* Supply patch with 'X-Git-Url:' header set to a non-URL string
* Supply patch with no Subject line
* Supply a completely empty body (using fixpatch?)


## How to Test

To run these tests, using the python unittest module. For
example, from the source directory, you can run:

    zsh> python3 -m unittest -v test

If you like a nicer interface, you can use "pytest", as
a unit, or from the command line, i.e. this:

    zsh> python3 -m pytest -v test

Note that, in general, wherever you see "unittest", or "pytest",
you can generally use either.

If you prefer the command line interface of pytest, you can run:

    zsh> pytest -v test

This will run all the tests in the "test" class, which
are in the "test" subdirectory. The "-v" adds more verbosity.

To run a single test, you could use, for example:

    zsh> pytest -v test.test_exportpatch.TestExportpatchNormalFunctionality.test_to_stdout_defaults

## Testing Code Coverage

If you would like to test the code coverage of these tests, you can install
the "pytest-cov" package, then run:

    zsh> coverage run --source=patchtools -m pytest -v test

Then, to get the coverage report:

    zsh> coverage report


# Test Structure

The tests are in files named "test_exportpatch.py" and "test_fixpatch.py",
and use the unittest.

There are multiple test classes in each test file. Each class groups together
multiple test cases that focus on a common area. Each self test is named along
the lines of "test_SOMETHING()".

The test framework finds the tests and runs them for you, as long as the naming
convention is followed.

# Known Bugs

For lack of a better place to track them, here's hopefully-current list
of known bugs, discovered during test creation or testing:

## Usage message of fixpatch

It says "-s"/"--suffix" is useful with "-w", but there is not "-w" in
fixpatch, so this seems like a cut-n-paste error.

This is a help message bug, not a functional bug.

### status: not fixed

## fixpatch on a non-existant file

It prints a stack dump. But exporpatch is much nicer if if you hit a
similar case, printing out a nice message. This is really more of an
enhancement than a bug fix.

### status: not fixed

## exporting a commit with a UTF-8 string seems to get strange chars

check out this commit: 8db816c6f176321e42254badd5c1a8df8bfcfdb4

This may or may not be a bug? It leaves the "from" name kind
of funky, e.g.:

    zsh> exportpatch  8db816c6f176321e42254badd5c1a8df8bfcfdb4 | head -1
    From: =?utf-8?q?Kai_M=C3=A4kisara_=3CKai=2EMakisara=40kolumbus=2Efi=3E?=

but ''git show'' on the same commit has different output:

    zsh git show 8db816c6f176321e42254badd5c1a8df8bfcfdb4 | head -2
    commit 8db816c6f176321e42254badd5c1a8df8bfcfdb4
    Author: Kai Mäkisara <Kai.Makisara@kolumbus.fi>

So should be rendering utf charaters better?

Not a new issue. Might actually be a "feature"?

### status: not fixed

## exportpatch parser uses parser.error()

This function, from optparse.OptionParser, prints an
error message then exits, but we have (had?):

    ...
    ...
    parser.error('some message')
    return 1

This also makes the unit test fail for parser errors.

### status: fix in place

## OptionParser likes to call sys.exit()

duplicate of above issue?

when the option parser gets an error, like an option
that should have a value associated with it but does not,
it calls "parser.error()", which ends up calling sys.exit().

This makes testing hard, so catch such errors.

### status: fix in place

## exportpatch num_width can be ignored

If the "-N width" value is less than 1 or more than 4,
it is silently ignored. There should at least be a
warning message, if not an error message?

### status: not fixed

## exportpatch treats first-number and and num-width differently

It tells the option parser that num-width is an int, but it
fails to do so for first-number, so we have to manually parse
first-number ourselves, making the error messages for both
have different paths and print different error messages.

### status: not fixed

## exportpatch stack dumps when writing to non-existant directory

This exception could be caught, and a nicer message printed.

### status: not fixed

## exportpatch nit: when writing to a dir that doesn't exist, print patch filename?

When we print to a dir that doesn't exist, we print the patch pathname,
as usual, then try to open it. If the open fails, we print an error
and exit. But why print the patch filename in such a case?

### status: not fixed

## the config file is read too early in the python code

The configuration file is found and read when the module is
loaded, from \_\_init\_\_.py, even though we may not be calling
the main exportpatch or fixpatch code yet.

It shouldn't be read until the commands are called, IMHO. The
current method makes testing a little heard, because we have
to create a config file before we even import the module.

### status: not fixed

## fixpatch help usage is wrong

It doesn't mention that you need to supply one or more patches
to be fixed because it uses the default help usage message.

### status: fix in place (simple)

## fixpatch no-diffstat doesn't remove existing diffstat

This option to fixpatch does not add a diffstat, but it
will not remove one, either. Probably not a bug.

### status: fixed: changed wording

## fixpatch does not limit patch filename length during rename

I haven't tested with non-suffix, where the patch filename is
just from the subject line, but when adding a suffix, it
does not limit the patch filename length to 64, as does
exportpatch.

### status: not fixed (may be a "feature"? does it matter?)

## fixpatch useless debug statement

It appears that "-d" (debug) isn't available for fixpatch,
and there's a debug statement that can never be called
in Patch(), which can never show up from fixpatch

### status: not fixed

## fixpatch setting dummy patch-mainline gives a duplicate

When you set this, you get two "Patch-mainline:" headers.
And this is on an initial patch being fixed that has no
such header, so fixpatch is adding two of them

### status: fixed

## fixpatch pukes stack dummp when supplied patch filename doesn't exist

### status: fix in place (simple)


## fixpatch didn't return error to CLI

The code never plumbed a return value.

### status: fix in place

## fixpatch called sys.exit() for CLI option errors

Like exportpatch, it used "parser.error()", which
ends up calling sys.exit().

### status: fix in place

## fixpatch no rename to a read-only dumps stack

Should be cleaner.

### status: simple fix in place

## fixpatch if patch filename is readonly it still prints it out

Don't need to see the patchname when it isn't being generated!

### status: simple fix in place






# infrastructure bugs (common to exportpatch and fixpatch)

## in patch.py: "switched" seems unused?

## in patch.py: add_signature() signed-off-by not used

## in patch.py: update_refs() method never used

## in patch.py, the Patch() repo argument is never ever used


# in generral

## replace deprecated (since 2.7!) optparse with argparse

