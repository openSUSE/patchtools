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

* test with various (or missing) config file for what RFEPOs to search


#### normal ops

* export a simple commit, just one file, just one hunk:

** export to a dir/file, using defaults                     -- done (2 cases)
   repeat with a suffix

** export to a dir/file, using numeric values,              -- done (3 cases)
   repeat with non-default starting number
   repeat with non-default width

** export to a dir/file, using 'force' to overwrite         -- done (2 cases)
   repeat without force set

** export to stdout                                         -- done (1 case)

** export to current dir                                    -- done (1 case)

** export to dir/file, testing reference                    -- done (1 case)

** export to stdout, but exclude whoe file

** export to sdout, using extract of whole file



* export a tag (not a commit)


* export a commit that has multiple files
** ensure extract works
** ensure exclude works

* test various commits to ensure "Patch-mainline" is correct

### error ops

* test "num-width" limits

* test bogus params, such as
** bogus commit
** no commit
** bad arguments
** illegal values for num-width?
