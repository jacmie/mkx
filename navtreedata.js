/*
 @licstart  The following is the entire license notice for the JavaScript code in this file.

 The MIT License (MIT)

 Copyright (C) 1997-2020 by Dimitri van Heesch

 Permission is hereby granted, free of charge, to any person obtaining a copy of this software
 and associated documentation files (the "Software"), to deal in the Software without restriction,
 including without limitation the rights to use, copy, modify, merge, publish, distribute,
 sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
 furnished to do so, subject to the following conditions:

 The above copyright notice and this permission notice shall be included in all copies or
 substantial portions of the Software.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING
 BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
 DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

 @licend  The above is the entire license notice for the JavaScript code in this file
*/
var NAVTREE =
[
  [ "MKX", "index.html", [
    [ "Introduction", "index.html", null ],
    [ "1 Main Concepts", "p_1.html", [
      [ "1.1 Central", "p_1.html#p_1_1", null ],
      [ "1.2 Periphery", "p_1.html#p_1_2", null ],
      [ "1.3 MKX Keyboard", "p_1.html#p_1_3", null ]
    ] ],
    [ "2 Istallation", "p_2.html", [
      [ "2.1 Install Circuit Python", "p_2.html#p_2_1", null ],
      [ "2.2 Set Python environment (optional)", "p_2.html#p_2_2", null ],
      [ "2.3 Install Adafruit Bundles", "p_2.html#p_2_3", null ],
      [ "2.4 Install MKX", "p_2.html#p_2_4", [
        [ "2.4.1 Synchronize Github repository with the CIRCUITPY drive", "p_2.html#p_2_4_1", null ]
      ] ]
    ] ],
    [ "3 Get Started", "p_3.html", [
      [ "3.1 Hardware Keypass", "p_3.html#p_3_1", null ],
      [ "3.2 Booster Keyboard", "p_3.html#p_3_2", null ],
      [ "3.3 Square Keyboard", "p_3.html#p_3_3", null ]
    ] ],
    [ "4 MKX API", "p_4.html", [
      [ "4.1 Boot Config", "p_4.html#p_4_1", null ],
      [ "4.2 MKX Central", "p_4.html#p_4_2", [
        [ "4.2.1 add_central_periphery", "p_4.html#p_4_2_1", null ],
        [ "4.2.2 add_interface", "p_4.html#p_4_2_2", null ],
        [ "4.2.3 add_layer_status_led", "p_4.html#p_4_2_3", null ],
        [ "4.2.4 add_backlight", "p_4.html#p_4_2_4", null ],
        [ "4.2.5 add_keymap", "p_4.html#p_4_2_5", null ],
        [ "4.2.6 use_ble", "p_4.html#p_4_2_6", null ],
        [ "4.2.7 run_forever", "p_4.html#p_4_2_7", null ]
      ] ],
      [ "4.3 MKX Periphery", "p_4.html#p_4_3", [
        [ "4.3.1 PeripheryCentral", "p_4.html#p_4_3_1", null ],
        [ "4.3.2 PeripheryUART", "p_4.html#p_4_3_2", null ]
      ] ],
      [ "4.4 Interface", "p_4.html#p_4_4", [
        [ "4.4.1 InterphaceCentral", "p_4.html#p_4_4_1", null ],
        [ "4.4.2 InterphaceUART", "p_4.html#p_4_4_2", null ]
      ] ],
      [ "4.5 Layer Status LED", "p_4.html#p_4_5", [
        [ "4.5.1 LayerStatusLedRgbNeoPixel", "p_4.html#p_4_5_1", null ],
        [ "4.5.2 LayerStatusLedRgbThreePin", "p_4.html#p_4_5_2", null ],
        [ "4.5.3 LayerStatusLedArray", "p_4.html#p_4_5_3", null ]
      ] ],
      [ "4.6 Backlight", "p_4.html#p_4_6", [
        [ "4.6.1 BacklightNeopixelStatic", "p_4.html#p_4_6_1", null ],
        [ "4.6.2 BacklightNeopixelRainbow", "p_4.html#p_4_6_2", null ],
        [ "4.6.2.1 faster()", "p_4.html#p_4_6_2_1", null ],
        [ "4.6.2.2 slower()", "p_4.html#p_4_6_2_2", null ],
        [ "4.6.2.3 set_swirl()", "p_4.html#p_4_6_2_3", null ]
      ] ]
    ] ],
    [ "5 Keys", "p_5.html", [
      [ "5.1 Standard Keys", "p_5.html#p_5_1", null ],
      [ "5.2 Modifiers Keys", "p_5.html#p_5_2", null ],
      [ "5.3 Layers Keys", "p_5.html#p_5_3", [
        [ "5.3.1 DF - Default Layer", "p_5.html#p_5_3_1", null ],
        [ "5.3.2 RL - Replace Layer", "p_5.html#p_5_3_2", null ],
        [ "5.3.3 MO - Momentary Layer", "p_5.html#p_5_3_3", null ],
        [ "5.3.4 LT - Layer Tap", "p_5.html#p_5_3_4", null ],
        [ "5.3.5 TG - Toggle Layer", "p_5.html#p_5_3_5", null ],
        [ "5.3.6 TO - To Layer (Toggle One-Shot Layer)", "p_5.html#p_5_3_6", null ],
        [ "5.3.7 TT - Tap-Toggle", "p_5.html#p_5_3_7", null ]
      ] ],
      [ "5.4 SEQ - Sequence Keys", "p_5.html#p_5_4", null ],
      [ "5.5 HT - HoldTap Keys", "p_5.html#p_5_5", null ],
      [ "5.6 TD - TapDance Keys", "p_5.html#p_5_6", null ],
      [ "5.7 SK - Sticky Keys", "p_5.html#p_5_7", null ],
      [ "5.8 VIM Keys", "p_5.html#p_5_8", [
        [ "5.8.1 Normal Mode", "p_5.html#p_5_8_1", null ],
        [ "5.8.2 Edit Mode", "p_5.html#p_5_8_2", null ],
        [ "5.8.3 Visual Mode", "p_5.html#p_5_8_3", null ],
        [ "5.8.4 Replace Mode", "p_5.html#p_5_8_4", null ],
        [ "5.8.5 Vim Layout", "p_5.html#p_5_8_5", null ]
      ] ],
      [ "5.9 Media Keys", "p_5.html#p_5_9", null ],
      [ "5.10 Mouse Keys", "p_5.html#p_5_10", null ]
    ] ],
    [ "6 Development", "p_6.html", [
      [ "Dev", "p_6.html#p_6_1", null ],
      [ "Build with mpy", "p_6.html#p_6_2", [
        [ "Code rules", "p_6.html#autotoc_md3", null ]
      ] ]
    ] ]
  ] ]
];

var NAVTREEINDEX =
[
"index.html"
];

var SYNCONMSG = 'click to disable panel synchronisation';
var SYNCOFFMSG = 'click to enable panel synchronisation';