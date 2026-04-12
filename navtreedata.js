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
      [ "2.4 Install MKX", "p_2.html#p_2_4", null ],
      [ "2.5 Optional", "p_2.html#p_2_5", [
        [ "2.5.1 Optional - Build Binary MKX Library", "p_2.html#p_2_5_1", null ],
        [ "2.5.2 Optional - Synchronize Github repository with the CIRCUITPY drive", "p_2.html#p_2_5_2", null ],
        [ "2.5.3 Optional - Testing Tools", "p_2.html#p_2_5_3", null ],
        [ "2.5.4 Optional - Build HTML documentation with Doxygen", "p_2.html#p_2_5_4", null ]
      ] ]
    ] ],
    [ "3 Get Started", "p_3.html", [
      [ "3.1 Basic Usage", "p_3.html#p_3_1", [
        [ "3.1.1 Files Structure", "p_3.html#p_3_1_1", null ],
        [ "3.1.2 Programming", "p_3.html#p_3_1_2", null ]
      ] ],
      [ "3.2 Hardware Keypass", "p_3.html#p_3_2", null ],
      [ "3.3 Booster Keyboard", "p_3.html#p_3_3", null ],
      [ "3.4 Square Keyboard", "p_3.html#p_3_4", null ],
      [ "3.5 Hackpad Keyboard", "p_3.html#p_3_5", null ]
    ] ],
    [ "4 MKX API", "p_4.html", [
      [ "4.1 Boot Config", "p_4.html#p_4_1", null ],
      [ "4.2 MKX Single", "p_4.html#p_4_2", null ],
      [ "4.3 MKX Central", "p_4.html#p_4_3", [
        [ "4.3.1 add_periphery_central", "p_4.html#p_4_3_1", null ],
        [ "4.3.2 add_interface", "p_4.html#p_4_3_2", null ],
        [ "4.3.3 add_layer_status_led", "p_4.html#p_4_3_3", null ],
        [ "4.3.4 add_backlight", "p_4.html#p_4_3_4", null ],
        [ "4.3.5 add_keymap", "p_4.html#p_4_3_5", null ],
        [ "4.3.6 use_ble", "p_4.html#p_4_3_6", null ],
        [ "4.3.7 run_forever", "p_4.html#p_4_3_7", null ]
      ] ],
      [ "4.4 MKX Periphery", "p_4.html#p_4_4", [
        [ "4.4.1 PeripherySingle", "p_4.html#p_4_4_1", null ],
        [ "4.4.2 PeripheryCentral", "p_4.html#p_4_4_2", null ],
        [ "4.4.3 PeripheryUART", "p_4.html#p_4_4_3", null ],
        [ "4.4.4 PeripheryTouch", "p_4.html#p_4_4_4", null ]
      ] ],
      [ "4.5 MKX Touch", "p_4.html#p_4_5", null ],
      [ "4.6 Interface", "p_4.html#p_4_6", [
        [ "4.6.1 InterfaceSingle", "p_4.html#p_4_6_1", null ],
        [ "4.6.2 InterfaceCentral", "p_4.html#p_4_6_2", null ],
        [ "4.6.3 InterfaceUART", "p_4.html#p_4_6_3", null ],
        [ "4.6.4 InterfaceTouch", "p_4.html#p_4_6_4", null ],
        [ "4.6.5 InterfaceTouchSlider", "p_4.html#p_4_6_5", null ],
        [ "4.6.6 InterfaceTouchWheel", "p_4.html#p_4_6_6", null ]
      ] ],
      [ "4.7 Layer Status LED", "p_4.html#p_4_7", [
        [ "4.7.1 LayerStatusLedRgbNeoPixel", "p_4.html#p_4_7_1", null ],
        [ "4.7.2 LayerStatusLedRgbThreePin", "p_4.html#p_4_7_2", null ],
        [ "4.7.3 LayerStatusLedArray", "p_4.html#p_4_7_3", null ]
      ] ],
      [ "4.8 Backlight", "p_4.html#p_4_8", [
        [ "4.8.1 BacklightNeopixelStatic", "p_4.html#p_4_8_1", null ],
        [ "4.8.2 BacklightNeopixelRainbow", "p_4.html#p_4_8_2", null ],
        [ "4.8.2.1 faster()", "p_4.html#p_4_8_2_1", null ],
        [ "4.8.2.2 slower()", "p_4.html#p_4_8_2_2", null ],
        [ "4.8.2.3 set_swirl()", "p_4.html#p_4_8_2_3", null ]
      ] ],
      [ "4.9 I2C Helper", "p_4.html#p_4_9", null ],
      [ "4.10 Haptic", "p_4.html#p_4_10", null ]
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
      [ "6.1 Code rules", "p_6.html#p_6_1", null ],
      [ "6.2 Build Binary MKX Library", "p_6.html#p_6_2", null ],
      [ "6.3 Synchronize Github repository with the CIRCUITPY drive", "p_6.html#p_6_3", null ],
      [ "6.4 Testing", "p_6.html#p_6_4", [
        [ "6.4.1 Run Tests", "p_6.html#p_6_4_1", null ],
        [ "6.4.2 Code Coverage", "p_6.html#p_6_4_2", null ],
        [ "6.4.3 Write New Tests", "p_6.html#p_6_4_3", null ]
      ] ],
      [ "6.5 Build HTML docs", "p_6.html#p_6_5", null ]
    ] ]
  ] ]
];

var NAVTREEINDEX =
[
"index.html"
];

var SYNCONMSG = 'click to disable panel synchronisation';
var SYNCOFFMSG = 'click to enable panel synchronisation';