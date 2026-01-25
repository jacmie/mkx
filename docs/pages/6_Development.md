@page p_6 6 Development
@tableofcontents


@section p_6_1 6.1 Code rules
- keep files structure flat
- place the library on board in the default **CIRCUITPYTHON/lib** directory

To add functionality, inherit from the **Abstract** classes if possible, and use them like the already implemented functions and keys.  

@section p_6_2 6.2 Build Binary MKX Library

Install *Adafruit* **mpy-cross** *for CircuitPython*, see @ref p_2
Use the **build** tool from the **MKX** repository:

```
usage: build.py [-h] [-d DRIVE] [--compile] [--upload] [--clean] [--tidy]

Compile/upload mkx to a CIRCUITPY device.

options:
  -h, --help            show this help message and exit
  -d DRIVE, --drive DRIVE
                        Name of the mounted drive (default: CIRCUITPY) or full mount path
  --compile             Compile .py files to .mpy (use with --upload to compile before upload)
  --upload              Upload compiled .mpy files to the drive (does not compile unless --compile given)
  --clean               Remove compiled files (.compiled)
  --tidy                Removing all content from the mkx dir on the MCU mountpoint
```

@section p_6_3 6.3 Synchronize Github repository with the CIRCUITPY drive

Install **watchdog** tool, see @ref p_2
Use the **auto_sync** tool from the **MKX** repository:

```
usage: auto_sync.py [-h] [-d DRIVE] [--diff] [--Vdiff] [--build] [--clean] [--tidy]

Sync mkx local files to a CIRCUITPY device.

options:
  -h, --help            show this help message and exit
  -d DRIVE, --drive DRIVE
                        Name of the mounted drive (default: CIRCUITPY)
  --diff                Which files are different and should be updated.
  --Vdiff               Verbose differences between files.
  --build               Build .mpy binaries using build.py and upload instead of .py files.
  --clean               Remove compiled files (.compiled directory).
  --tidy                Remove all uploaded content from the MCU mountpoint.
```

@section p_6_4 6.4 Build HTML docs

The documentation is build with Doxygen:  
https://www.doxygen.nl/

From the **docs** directory, run:
```
doxygen ./Doxyfile
```
Open the documentation **docs/html/index.html**  

If you update the content of the documentation run **doxygen** again.  
Don't close the browser, just refresh the documentation page - **F5**.

