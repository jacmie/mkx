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
circup install adafruit_ble adafruit_hid
```
<br>

@section p_2_4  2.4 Install MKX

Download the latest release, unpack and copy the **mkx** folder to the **CIRCUITPY/lib** directory.  
<br>

@subsection p_2_4_1  2.4.1 Synchronize Github repository with the CIRCUITPY drive

The **MKX** repository includes a tool called **auto_sync** that can synchronize repository content with the **CIRCUITPY** drive.  
This is especially convenient for developers — but useful for other users as well.  
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

For more **auto_sync** options, try:

```
python auto_sync.py -h
```
