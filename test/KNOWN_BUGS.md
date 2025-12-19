# Bugs that are known

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
