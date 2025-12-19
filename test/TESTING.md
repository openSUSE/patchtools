# Testing for patchtools, using pyunit

## to test

### exportpatch

#### error conditions

* bogus commit supplied (does not match anything)
* no commit supplied
* try to supply "HEAD" or "^" (should fail)
* incorrect patch config file (points to nothing?)
* no patch config file?
* try to write with no write permission in dir
* invalid directory supplied to write patch
* exclude everything, so patch is empty
* specify out-of-range starting number for a numbered patch
* trying to write a patch file when one already exists without --force (should get funky name)

#### normal ops

* export a simple commit, just one file, just one hunk:

** export a known patch to a dir/file, with and without a suffix

** export a known patch to a dir/file, with and without a suffix
   numeric, with normal and set starting number, with and
   without max width

** export a simple patch to current dir

** export a simple patch to dir/file, but one already exists

** export a simple patch to dir/file, overwriting one that exists

** export a simple patch to dir/file, testing reference

** export a known patch to stdout


* export a tag (not a commit)


* export a commit that has multiple files

** ensure extract works

** ensure exclude works

* test various commits to ensure "Patch-mainline" is correct
* test "num-width"?
