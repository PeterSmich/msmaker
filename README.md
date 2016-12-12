# msmaker
msmaker is a graphical tool to generate manually .mswallet items. You can easily generate beautiful wallet items such as boarding pass, ticket, loyalty card. You can set your unique logo, background, contents and layout. Easy to use and generate wallet item for Windows Phone 8 and Windows 10 mobile.

<img src="/Sample/Card.png" alt="Card img" width="144" height="256">
<img src="/Sample/Front.png" alt="Front img" width="144" height="256">
<img src="/Sample/Back.png" alt="Back img" width="144" height="256">


****

Installation
------------
###With Python:

1. Install Python 2.7 : https://www.python.org/
2. Download msmaker as a [zip](https://github.com/PeterSmich/msmaker/releases) and unzip it
3. Run msmaker.py

###For Windows:

1. Download and run [msmaker_setup.exe](https://github.com/PeterSmich/msmaker/releases/download/v1.0/msmaker_setup.exe)

Usage
-----
- If an atribute is default (as it appears) in the BASIC frame, it will not show on the pass.
- If an atribute is empty in the P.S.F. or BASIC frame, it could result in a failour while adding the pass to the wallet.
- Version atribute is not allowed to be 0.
- Only use ASCII character.
- Only use .png images with sepcific name. (Logog99x99.png ...)
- To make an atribute empty use: &# 160; (yes, with coma, without space between # and 1) 
- To get barcode info from pdf, jpg, etc... use: [ByScout: BarCode Reader](https://bytescout.com/products/developer/barcodereadersdk/bytescoutbarcodereadersdk.html)
- <img src="/Sample/Sample.png" alt="Sample img" width="144" height="256">

Developer
---------
PeterSmich

