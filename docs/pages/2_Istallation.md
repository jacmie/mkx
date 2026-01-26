@page p_2 2 Istallation
@tableofcontents

@section p_2_1 2.1 Install Circuit Python

You probably already know this, but the first step is to install [Circuit Python](https://circuitpython.org/) on the supported board.  
Go to the [Circuit Python Downloads](https://circuitpython.org/downloads), locate your board, and follow the installation instructions.  
In many cases, it's as simple as plugging the board into your computer via USB and dragging the downloaded <b>*.uf2</b> file onto the mounted **CIRCUITPY** drive.  
<br>

@section p_2_2 2.2 Set Python environment (optional)

Installing [Python](https://www.python.org/) is optional but convenient for users and developers of **MKX**.  
Set up a Python environment named **dev** and activate it:

```
python3 -m dev ../dev
source ../dev/bin/activate
```
<br>

@section p_2_3 2.3 Install Adafruit Bundles

**MKX** requires additional Adafruit libraries.  
You can download them manually from the [Circuit Python Libraries](https://circuitpython.org/libraries) and copy to the **CIRCUITPY/lib** directory.  

Cleaner and more recommended approach is to use the **circup** tool.  
This requires Python to be installed and your environment activated (<i>see section 2.2</i>).  
In the **dev** Python environment:
```
pip install circup
```

The board’s drive must be named **CIRCUITPY** (this is the default).  
If the drive has a different name, rename it back to CIRCUITPY:
[Renaming CIRCUITPY](https://learn.adafruit.com/welcome-to-circuitpython/renaming-circuitpy)  

Later on, you may want to intentionally rename the drive — this is often the case with split keyboards.  

Install the Adafruit libraries:

```
circup install adafruit_ble adafruit_bus_device adafruit_hid neopixel simpleio
```
<br>

@section p_2_4  2.4 Install MKX

Download the latest release, unpack and copy the **mkx** folder to the **CIRCUITPY/lib** directory.  
<br>

@section p_2_5  2.5 Optional

@subsection p_2_5_1  2.5.1 Optional - Build Binary MKX Library

The **MKX** repository includes a tool called **build** that compiles the MKX library into a binary format.  Using the compiled library improves stability and performance.  

The build tool requires *Adafruit* **mpy-cross** *for CircuitPython*.  

You can either download a prebuilt binary for your operating system from:  
https://adafruit-circuit-python.s3.amazonaws.com/index.html?prefix=bin/mpy-cross/

or build it yourself from the CircuitPython repository:  

```
git clone https://github.com/adafruit/circuitpython.git
cd circuitpython/mpy-cross
make
# optionally add mpy-cross to system PATH
# build calls the mpy-cross in the process
# direct use:
./mpy-cross example/adafruit_example.py
```

Clone the **MKX** repository, or your own fork:

```
git clone git@github.com:jacmie/mkx.git
```

Run the build tool from the repository root to compile the MKX library into the local <b>.compile</b> directory:
```
python build.py --compile
```

Upload the whole compiled library to the **CIRCUITPY/lib** directory:

```
python build.py --upload
```

For more **build** options, run:

```
python build.py -h
```

See also @ref p_6

@subsection p_2_5_2  2.5.2 Optional - Synchronize Github repository with the CIRCUITPY drive

The **MKX** repository also includes tool called **auto_sync**, which automatically synchronizes repository files with the **CIRCUITPY** drive.  
This is particularly useful for development, but can benefit other users as well.  

The tool requires installed **watchdog** module. Activate your Python **dev** environment and install it with:

```
pip install watchdog
```

Clone the **MKX** repository, or your own fork:

```
git clone git@github.com:jacmie/mkx.git
```

When you run the **auto_sync** in the repository, it will copy the **mkx** folder from the repository to the **CIRCUITPY/lib** directory.  
After that, every time a file in the repository is saved, it will also be copied to the board.  
To stop the tool, press **CTRL+C**.

```
python auto_sync.py
```

If the drive was renamed, use the **-d** flag followed by the new drive name:

```
python auto_sync.py -d MY_CIRCUITPY_DRIVE_NAME
```

The **auto_sync** can use the **build** tool:
```
python auto_sync.py --build
```

For more **auto_sync** options, run:

```
python auto_sync.py -h
```

See also @ref p_6_2


@subsection p_2_5_3  2.5.3 Optional - Testing Tools

Testing **MKX** requires Python to be installed and your environment activated (<i>see section 2.2</i>).  
In the **dev** Python environment:

```
pip install pytest coverage
```

Additional optional code quality tools can be installed:

```
pip install pylint flake8 mypy
```

See also @ref p_6_4 for how to run and write tests.

@subsection p_2_5_4  2.5.4 Optional - Build HTML documentation with Doxygen

Download Doxygen and install it:
https://www.doxygen.nl/download.html

From the **docs** directory, run:
```
doxygen ./Doxyfile
```
Open the documentation **docs/html/index.html**  

See also @ref p_6_5
