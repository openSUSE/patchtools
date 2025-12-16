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

* export a "known patch" (to stdout?), make sure it matches the known output? (what about 'signed-off-by')
* export a tag (not a commit)
* write a patch -- default, no number, and no suffix, in current dir
* write to a good dir and to current dir
* write with and without suffix
* write with and without numbering
* write with non-default starting number
* can write over a patch if and only if --force is supplied
* write with and without reference
* make sure extract and exclude work
* ensure signed-off-by works
* test various commits to ensure "Patch-mainline" is correct
* test "num-width"?
