# dupes

Find duplicate files and folders.

In a large collection of documents, books, or music, it's pretty common to end up with

* NB_Report_Final_2.pdf
* NB_Report_Final_2 (1).pdf

or

* BACKUPS/Music/Hamilton/
* ~/Music/Hamilton(2)/

or any other amount of mess. `dupes` can help you clean this up by identifying redundant files to delete or folders to merge.

It can also help you ensure that your backups are actually complete copies; though `diff -r` is more useful for that.


## Installation

```
git clone --depth 1 https://github.com/kousu/dupes # I haven't uploaded to pypi yet
pip install dupes
```

## Usage

```
dupes folder [folder folder...]
```

## Example

This example is a bit pythonista navel-gazey, but it is easy to set up and demonstrate:

```
# set up some test data
python -m virtualenv venv1
python -m virtualenv venv2
. venv1/bin/activate
pip install requests dcm2bids
deactivate 
. venv2/bin/activate
pip install dcm2bids future
deactivate
find . -name __pycache__ -exec rm -r {} \; # cruft that makes the example more difficult

# symlinks too:
mkdir links
echo coffee > lol
ln -s ../lol links/a
ln -s ../lol links/b
```

Running `dupes` on this gives

```
$ dupes .
./venv1/.gitignore
./venv2/.gitignore

./venv1/bin/activate.ps1
./venv2/bin/activate.ps1

./venv1/bin/activate_this.py
./venv2/bin/activate_this.py

./venv1/bin/pip
./venv1/bin/pip-3.9
./venv1/bin/pip3
./venv1/bin/pip3.9

./venv1/bin/wheel
./venv1/bin/wheel-3.9
./venv1/bin/wheel3
./venv1/bin/wheel3.9

./venv1/lib/python3.9/site-packages/_distutils_hack/
./venv2/lib/python3.9/site-packages/_distutils_hack/

./venv1/lib/python3.9/site-packages/_virtualenv.pth
./venv2/lib/python3.9/site-packages/_virtualenv.pth

./venv1/lib/python3.9/site-packages/_virtualenv.py
./venv2/lib/python3.9/site-packages/_virtualenv.py

./venv1/lib/python3.9/site-packages/certifi-2020.12.5.dist-info/INSTALLER
./venv1/lib/python3.9/site-packages/chardet-4.0.0.dist-info/INSTALLER
./venv1/lib/python3.9/site-packages/dcm2bids-2.1.5.dist-info/INSTALLER
./venv1/lib/python3.9/site-packages/dupes-0.0.1.dist-info/INSTALLER
./venv1/lib/python3.9/site-packages/future-0.18.2.dist-info/INSTALLER
./venv1/lib/python3.9/site-packages/idna-2.10.dist-info/INSTALLER
./venv1/lib/python3.9/site-packages/pip-21.0.1.dist-info/INSTALLER
./venv1/lib/python3.9/site-packages/pip-21.0.1.dist-info/top_level.txt
./venv1/lib/python3.9/site-packages/requests-2.25.1.dist-info/INSTALLER
./venv1/lib/python3.9/site-packages/setuptools-52.0.0.dist-info/INSTALLER
./venv1/lib/python3.9/site-packages/tqdm-4.56.0.dist-info/INSTALLER
./venv1/lib/python3.9/site-packages/urllib3-1.26.3.dist-info/INSTALLER
./venv1/lib/python3.9/site-packages/wheel-0.36.2.dist-info/INSTALLER
./venv2/lib/python3.9/site-packages/dcm2bids-2.1.5.dist-info/INSTALLER
./venv2/lib/python3.9/site-packages/future-0.18.2.dist-info/INSTALLER
./venv2/lib/python3.9/site-packages/pip-21.0.1.dist-info/INSTALLER
./venv2/lib/python3.9/site-packages/pip-21.0.1.dist-info/top_level.txt
./venv2/lib/python3.9/site-packages/setuptools-52.0.0.dist-info/INSTALLER
./venv2/lib/python3.9/site-packages/wheel-0.36.2.dist-info/INSTALLER

./venv1/lib/python3.9/site-packages/certifi-2020.12.5.dist-info/WHEEL
./venv1/lib/python3.9/site-packages/chardet-4.0.0.dist-info/WHEEL

./venv1/lib/python3.9/site-packages/certifi/cacert.pem
./venv1/lib/python3.9/site-packages/pip/_vendor/certifi/cacert.pem
./venv2/lib/python3.9/site-packages/pip/_vendor/certifi/cacert.pem

./venv1/lib/python3.9/site-packages/chardet/metadata/__init__.py
./venv1/lib/python3.9/site-packages/dcm2bids-2.1.5.dist-info/REQUESTED
./venv1/lib/python3.9/site-packages/dupes-0.0.1.dist-info/REQUESTED
./venv1/lib/python3.9/site-packages/easy-install.pth
./venv1/lib/python3.9/site-packages/future/backports/email/mime/__init__.py
./venv1/lib/python3.9/site-packages/future/backports/http/__init__.py
./venv1/lib/python3.9/site-packages/future/backports/test/nullcert.pem
./venv1/lib/python3.9/site-packages/future/backports/urllib/__init__.py
./venv1/lib/python3.9/site-packages/future/moves/xmlrpc/__init__.py
./venv1/lib/python3.9/site-packages/future/tests/__init__.py
./venv1/lib/python3.9/site-packages/pip-21.0.1.virtualenv
./venv1/lib/python3.9/site-packages/pip/_internal/operations/__init__.py
./venv1/lib/python3.9/site-packages/pip/_internal/operations/build/__init__.py
./venv1/lib/python3.9/site-packages/pip/_internal/resolution/__init__.py
./venv1/lib/python3.9/site-packages/pip/_internal/resolution/legacy/__init__.py
./venv1/lib/python3.9/site-packages/pip/_internal/resolution/resolvelib/__init__.py
./venv1/lib/python3.9/site-packages/pip/_internal/utils/__init__.py
./venv1/lib/python3.9/site-packages/pip/_vendor/chardet/metadata/__init__.py
./venv1/lib/python3.9/site-packages/pip/_vendor/html5lib/filters/__init__.py
./venv1/lib/python3.9/site-packages/pip/_vendor/resolvelib/compat/__init__.py
./venv1/lib/python3.9/site-packages/pip/_vendor/urllib3/contrib/__init__.py
./venv1/lib/python3.9/site-packages/pip/_vendor/urllib3/contrib/_securetransport/__init__.py
./venv1/lib/python3.9/site-packages/pip/_vendor/urllib3/packages/backports/__init__.py
./venv1/lib/python3.9/site-packages/pkg_resources/_vendor/__init__.py
./venv1/lib/python3.9/site-packages/requests-2.25.1.dist-info/REQUESTED
./venv1/lib/python3.9/site-packages/setuptools-52.0.0.virtualenv
./venv1/lib/python3.9/site-packages/setuptools/_vendor/__init__.py
./venv1/lib/python3.9/site-packages/urllib3/contrib/__init__.py
./venv1/lib/python3.9/site-packages/urllib3/contrib/_securetransport/__init__.py
./venv1/lib/python3.9/site-packages/urllib3/packages/backports/__init__.py
./venv1/lib/python3.9/site-packages/wheel-0.36.2.virtualenv
./venv1/lib/python3.9/site-packages/wheel/vendored/__init__.py
./venv1/lib/python3.9/site-packages/wheel/vendored/packaging/__init__.py
./venv2/lib/python3.9/site-packages/dcm2bids-2.1.5.dist-info/REQUESTED
./venv2/lib/python3.9/site-packages/future-0.18.2.dist-info/REQUESTED
./venv2/lib/python3.9/site-packages/future/backports/email/mime/__init__.py
./venv2/lib/python3.9/site-packages/future/backports/http/__init__.py
./venv2/lib/python3.9/site-packages/future/backports/test/nullcert.pem
./venv2/lib/python3.9/site-packages/future/backports/urllib/__init__.py
./venv2/lib/python3.9/site-packages/future/moves/xmlrpc/__init__.py
./venv2/lib/python3.9/site-packages/future/tests/__init__.py
./venv2/lib/python3.9/site-packages/pip-21.0.1.virtualenv
./venv2/lib/python3.9/site-packages/pip/_internal/operations/__init__.py
./venv2/lib/python3.9/site-packages/pip/_internal/operations/build/__init__.py
./venv2/lib/python3.9/site-packages/pip/_internal/resolution/__init__.py
./venv2/lib/python3.9/site-packages/pip/_internal/resolution/legacy/__init__.py
./venv2/lib/python3.9/site-packages/pip/_internal/resolution/resolvelib/__init__.py
./venv2/lib/python3.9/site-packages/pip/_internal/utils/__init__.py
./venv2/lib/python3.9/site-packages/pip/_vendor/chardet/metadata/__init__.py
./venv2/lib/python3.9/site-packages/pip/_vendor/html5lib/filters/__init__.py
./venv2/lib/python3.9/site-packages/pip/_vendor/resolvelib/compat/__init__.py
./venv2/lib/python3.9/site-packages/pip/_vendor/urllib3/contrib/__init__.py
./venv2/lib/python3.9/site-packages/pip/_vendor/urllib3/contrib/_securetransport/__init__.py
./venv2/lib/python3.9/site-packages/pip/_vendor/urllib3/packages/backports/__init__.py
./venv2/lib/python3.9/site-packages/pkg_resources/_vendor/__init__.py
./venv2/lib/python3.9/site-packages/setuptools-52.0.0.virtualenv
./venv2/lib/python3.9/site-packages/setuptools/_vendor/__init__.py
./venv2/lib/python3.9/site-packages/wheel-0.36.2.virtualenv
./venv2/lib/python3.9/site-packages/wheel/vendored/__init__.py
./venv2/lib/python3.9/site-packages/wheel/vendored/packaging/__init__.py

./venv1/lib/python3.9/site-packages/dcm2bids/
./venv2/lib/python3.9/site-packages/dcm2bids/

./venv1/lib/python3.9/site-packages/dcm2bids-2.1.5.dist-info/LICENSE.txt
./venv2/lib/python3.9/site-packages/dcm2bids-2.1.5.dist-info/LICENSE.txt

./venv1/lib/python3.9/site-packages/dcm2bids-2.1.5.dist-info/METADATA
./venv2/lib/python3.9/site-packages/dcm2bids-2.1.5.dist-info/METADATA

./venv1/lib/python3.9/site-packages/dcm2bids-2.1.5.dist-info/WHEEL
./venv1/lib/python3.9/site-packages/dupes-0.0.1.dist-info/WHEEL
./venv1/lib/python3.9/site-packages/future-0.18.2.dist-info/WHEEL
./venv1/lib/python3.9/site-packages/pip-21.0.1.dist-info/WHEEL
./venv1/lib/python3.9/site-packages/setuptools-52.0.0.dist-info/WHEEL
./venv2/lib/python3.9/site-packages/dcm2bids-2.1.5.dist-info/WHEEL
./venv2/lib/python3.9/site-packages/future-0.18.2.dist-info/WHEEL
./venv2/lib/python3.9/site-packages/pip-21.0.1.dist-info/WHEEL
./venv2/lib/python3.9/site-packages/setuptools-52.0.0.dist-info/WHEEL

./venv1/lib/python3.9/site-packages/dcm2bids-2.1.5.dist-info/entry_points.txt
./venv2/lib/python3.9/site-packages/dcm2bids-2.1.5.dist-info/entry_points.txt

./venv1/lib/python3.9/site-packages/dcm2bids-2.1.5.dist-info/top_level.txt
./venv2/lib/python3.9/site-packages/dcm2bids-2.1.5.dist-info/top_level.txt

./venv1/lib/python3.9/site-packages/distutils-precedence.pth
./venv2/lib/python3.9/site-packages/distutils-precedence.pth

./venv1/lib/python3.9/site-packages/future/
./venv2/lib/python3.9/site-packages/future/

./venv1/lib/python3.9/site-packages/future-0.18.2.dist-info/LICENSE.txt
./venv2/lib/python3.9/site-packages/future-0.18.2.dist-info/LICENSE.txt

./venv1/lib/python3.9/site-packages/future-0.18.2.dist-info/METADATA
./venv2/lib/python3.9/site-packages/future-0.18.2.dist-info/METADATA

./venv1/lib/python3.9/site-packages/future-0.18.2.dist-info/entry_points.txt
./venv2/lib/python3.9/site-packages/future-0.18.2.dist-info/entry_points.txt

./venv1/lib/python3.9/site-packages/future-0.18.2.dist-info/top_level.txt
./venv2/lib/python3.9/site-packages/future-0.18.2.dist-info/top_level.txt

./venv1/lib/python3.9/site-packages/libfuturize/
./venv2/lib/python3.9/site-packages/libfuturize/

./venv1/lib/python3.9/site-packages/libpasteurize/
./venv2/lib/python3.9/site-packages/libpasteurize/

./venv1/lib/python3.9/site-packages/past/
./venv2/lib/python3.9/site-packages/past/

./venv1/lib/python3.9/site-packages/pip/
./venv2/lib/python3.9/site-packages/pip/

./venv1/lib/python3.9/site-packages/pip-21.0.1.dist-info/
./venv2/lib/python3.9/site-packages/pip-21.0.1.dist-info/

./venv1/lib/python3.9/site-packages/pkg_resources/
./venv2/lib/python3.9/site-packages/pkg_resources/

./venv1/lib/python3.9/site-packages/requests-2.25.1.dist-info/WHEEL
./venv1/lib/python3.9/site-packages/tqdm-4.56.0.dist-info/WHEEL
./venv1/lib/python3.9/site-packages/urllib3-1.26.3.dist-info/WHEEL
./venv1/lib/python3.9/site-packages/wheel-0.36.2.dist-info/WHEEL
./venv2/lib/python3.9/site-packages/wheel-0.36.2.dist-info/WHEEL

./venv1/lib/python3.9/site-packages/setuptools/
./venv2/lib/python3.9/site-packages/setuptools/

./venv1/lib/python3.9/site-packages/setuptools-52.0.0.dist-info/
./venv2/lib/python3.9/site-packages/setuptools-52.0.0.dist-info/

./venv1/lib/python3.9/site-packages/tests/
./venv2/lib/python3.9/site-packages/tests/

./venv1/lib/python3.9/site-packages/wheel/
./venv2/lib/python3.9/site-packages/wheel/

./venv1/lib/python3.9/site-packages/wheel-0.36.2.dist-info/
./venv2/lib/python3.9/site-packages/wheel-0.36.2.dist-info/

./venv1/pyvenv.cfg
./venv2/pyvenv.cfg

./venv2/bin/pip
./venv2/bin/pip-3.9
./venv2/bin/pip3
./venv2/bin/pip3.9

./venv2/bin/wheel
./venv2/bin/wheel-3.9
./venv2/bin/wheel3
./venv2/bin/wheel3.9
```

You can see that, for example, these folders are indeed identical:

```
$ diff -r ./venv{1,2}/lib/python3.9/site-packages/_distutils_hack/; echo $?
0
```

while these ones are indeed different -- and hence `dupes` only reported the identical subfiles in them:

```
$ diff -qru ./venv1/lib/python3.9/site-packages/certifi-2020.12.5.dist-info/ ./venv1/lib/python3.9/site-packages/chardet-4.0.0.dist-info/; echo $?
Only in ./venv1/lib/python3.9/site-packages/chardet-4.0.0.dist-info/: entry_points.txt
Files ./venv1/lib/python3.9/site-packages/certifi-2020.12.5.dist-info/LICENSE and ./venv1/lib/python3.9/site-packages/chardet-4.0.0.dist-info/LICENSE differ
Files ./venv1/lib/python3.9/site-packages/certifi-2020.12.5.dist-info/METADATA and ./venv1/lib/python3.9/site-packages/chardet-4.0.0.dist-info/METADATA differ
Files ./venv1/lib/python3.9/site-packages/certifi-2020.12.5.dist-info/RECORD and ./venv1/lib/python3.9/site-packages/chardet-4.0.0.dist-info/RECORD differ
Files ./venv1/lib/python3.9/site-packages/certifi-2020.12.5.dist-info/top_level.txt and ./venv1/lib/python3.9/site-packages/chardet-4.0.0.dist-info/top_level.txt differ
1

$ diff -ru ./venv{1,2}/lib/python3.9/site-packages/future-0.18.2.dist-info/
diff -ru ./venv1/lib/python3.9/site-packages/future-0.18.2.dist-info/RECORD ./venv2/lib/python3.9/site-packages/future-0.18.2.dist-info/RECORD
--- ./venv1/lib/python3.9/site-packages/future-0.18.2.dist-info/RECORD  2021-02-06 17:47:44.955940630 -0500
+++ ./venv2/lib/python3.9/site-packages/future-0.18.2.dist-info/RECORD  2021-02-06 17:48:05.382752458 -0500
@@ -1,9 +1,10 @@
-../../../bin/futurize,sha256=oHgPpd7407aq62xH8d9cqybsMe_BiwplDE1sSpTJ0-E,254
-../../../bin/pasteurize,sha256=7Q_2Zbyozak75T8uFi-SvDaDa925GQXpK_2d4yTdF5o,256
+../../../bin/futurize,sha256=hV3PrmZJLpI0TnPcRpAmuIRZWIXPhJXX8hnvZ0syiv0,254
+../../../bin/pasteurize,sha256=hETyy2Roa-5_DwcgfCgonW4f5__SlwVWQLPibY3BOds,256
 future-0.18.2.dist-info/INSTALLER,sha256=zuuue4knoyJ-UwPPXg8fezS7VCrXJQrAP7zeNuwvFQg,4
 future-0.18.2.dist-info/LICENSE.txt,sha256=kW5WE5LUhHG5wjQ39W4mUvMgyzsRnOqhYu30EBb3Rrk,1083
 future-0.18.2.dist-info/METADATA,sha256=fkY-mhLBh40f490kVFZ3hkvu2OVGdLIp5x-oJpqF91k,3703
 future-0.18.2.dist-info/RECORD,,
+future-0.18.2.dist-info/REQUESTED,sha256=47DEQpj8HBSa-_TImW-5JCeuQeRkm5NMpJWZG3hSuFU,0
 future-0.18.2.dist-info/WHEEL,sha256=OqRkF0eY5GHssMorFjlbTIq072vpHpF60fIQA6lS9xA,92
 future-0.18.2.dist-info/entry_points.txt,sha256=-ATQtLUC2gkzrCYqc1Twac093xrI164NuMwsRALJWnM,89
 future-0.18.2.dist-info/top_level.txt,sha256=DT0C3az2gb-uJaj-fs0h4WwHYlJVDp0EvLdud1y5Zyw,38
Only in ./venv2/lib/python3.9/site-packages/future-0.18.2.dist-info/: REQUESTED
```

## Why?

I find [`fdupes`](https://github.com/adrianlopezroche/fdupes/) extremely useful for managing filesystems,
however on a large dataset (and where else would I need to use it?) it can get overwhelming, fast.
`fdupes` can only handle files; it is not able to find common subtrees, which is usually what I want. Hopefully it's what you want too.

So, in addition to handling regular duplicate files, this version can find duplicate:

- directories
- symlinks (which fdupes seems to ignore)

and report them in a useful way.

<!--

(NOT IMPLEMENTED YET)

- sockets
- fifos
- device files

-->


To highlight the difference that summarizing subtrees makes compare the deep dive `fdupes` produces where `dupes` knows to stop:

```
$ fdupes -r .
[...]
./venv1/lib/python3.9/site-packages/libfuturize/fixes/fix_cmp.py
./venv2/lib/python3.9/site-packages/libfuturize/fixes/fix_cmp.py

./venv1/lib/python3.9/site-packages/libfuturize/fixes/fix_unicode_literals_import.py
./venv2/lib/python3.9/site-packages/libfuturize/fixes/fix_unicode_literals_import.py

./venv1/lib/python3.9/site-packages/libfuturize/fixes/fix_division.py
./venv2/lib/python3.9/site-packages/libfuturize/fixes/fix_division.py

./venv1/lib/python3.9/site-packages/libfuturize/fixes/fix_print_with_import.py
./venv2/lib/python3.9/site-packages/libfuturize/fixes/fix_print_with_import.py
[...]
$ fdupes -r . | wc
   2447    1677  116113                 
$ dupes .
[...]
./venv1/lib/python3.9/site-packages/libfuturize/
./venv2/lib/python3.9/site-packages/libfuturize/
[...]
$ dupes . | wc
    233     201   10829
```

## Bugs

This doesn't yet:

- handle all the kinds of unix file types
- sort output files the same way as `fdupes`
- print filesizes (`-s`)
- support `-1` for printing everything on a single line
- support interactive deletion (I'm not sure it should, though; you can pipe to your own scripts if you want that)
- the progress bars could be more useful


## See Also

`dupes` is useful in combination with:

* [`baobab`](https://wiki.gnome.org/action/show/Apps/DiskUsageAnalyzer)
* [`rsync`](https://rsync.samba.org/)
* [`diff`](https://www.gnu.org/software/diffutils/manual/diffutils.html)
