@page p_1 1 Istallation
@tableofcontents

@section p_1_1 1.1 Install Circuit Python

You probably already know it, that first you need to install the [Circuit Python](https://circuitpython.org/) on the supported board. Go to the [Circuit Python Downloads](https://circuitpython.org/downloads), find your board and follow the installation instructions. In many cases it's just plugging the board to USB and dragging the downloaded <b>*.uf2</b> file on the mounted **CIRCUITPY** drive.  
<br>

@section p_1_2 1.2 Set Python environment (optional)

Installing [Python](https://www.python.org/) is optional, but convienint for users and developers of the **MKX**.  
Set Python environment **dev** and activate:

```
python3 -m dev ../dev
source ../dev/bin/activate
```
<br>

@section p_1_3 1.3 Install adafruit bundles

**MKX** needs additional adafruit libraries. You can download them manually from the [Circuit Python Libraries](https://circuitpython.org/libraries) and copy to the **CIRCUITPY/lib** directory.  

More clean and recommended way is to use the **circup** tool. For that you need installed Python and activated environment (<i>see section 1.2</i>).  
In the **dev** environment:
```
pip install circup
```

The boards drive must to be named **CIRCUITPY** (default).
If the drive has different name, rename it back to the CIRCUITPY:
[Renaming CIRCUITPY](https://learn.adafruit.com/welcome-to-circuitpython/renaming-circuitpy)  
Later on you may want to rename the drive on purpose. 
This is often the case for split keyboards. 
Install the adafruit libraries:

```
circup install adafruit_ble adafruit_hid
```
<br>

@section p_1_4  1.4 Install MKX

Download the latest release, unpack and copy the **mkx** folder to the **CIRCUITPY/lib** directory.  

@subsection p_1_4_1  1.4.1 Synchronize Github repository with the CIRCUITPY drive

MKX repository has a tool **auto_sync** to synchronize repository content with the CIRCUITPY drive. 
This is especially convenient for developers but not only.  
The tool requires installed **watchdog** module. Activate your Python **dev** environment and install:

```
pip install watchdog
```

Clone the **MKX** repository, or your fork:

```
git clone git@github.com:jacmie/mkx.git
```

When you run the **auto_sync** in the repository it will copy the **mkx** foler from the repository to the the **CIRCUITPY/lib** directory.  
Next, every time file in the repository is saved it will be also copied on the board.  
Stop the tool by **CTRL+C**.

```
python auto_sync.py
```

If the drive was renamed use flag **-d** and the new drives name:

```
python auto_sync.py -d MY_CIRCUITPY_DRIVE_NAME
```

For more **auto_sync** options try:

```
python auto_sync.py -h
```
