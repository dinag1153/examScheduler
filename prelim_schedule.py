import re
from icalendar import Event, Calendar
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk, messagebox

import requests
from bs4 import BeautifulSoup

course_entries = []

def generate_schedule():
    # Define schedule data
    schedule_data = """AEM 2100       10/17/2023    KND116
    AEM 2100       11/14/2023    WRN151, WRN175, WRNB25 

    AEM 2210       9/21/2023     BKL200, BKL219
    AEM 2210       10/26/2023    KND116  

    AEM 2225       9/21/2023     WRN175, WRNB25
    AEM 2225       10/26/2023    WRN175, WRNB25  

    AEM 2241       9/21/2023     MRS146
    AEM 2241       10/24/2023    MRS146
    AEM 2241       11/30/2023    MRS146  

    AEM 2350       10/5/2023     WRNB25  

    AEM 2600 001   9/26/2023     WRN175, WRNB25
    AEM 2600 001   11/9/2023     WRN175, WRNB25  

    AEM 2600 002   9/26/2023     WRN175, WRNB25
    AEM 2600 002   11/9/2023     WRN175, WRNB25  

    AEM 2600 003   9/26/2023     KND116
    AEM 2600 003   11/7/2023     WRN175, WRNB25  

    AEM 2600 004   9/26/2023     KND116
    AEM 2600 004   11/7/2023     WRN175, WRNB25  

    AEM 3100       10/19/2023    WRN151  

    AEM 3360       10/3/2023     WRNB25, WRNB75
    AEM 3360       10/31/2023    WRN175, WRNB25
    AEM 3360       11/30/2023    KND116  

    AEM 4100       10/3/2023     WRN175
    AEM 4100       11/14/2023    WRN150, WRN173  

    AEP 1200       10/17/2023    HLS110  

    AEP 4130       9/28/2023     PHL219
    AEP 4130       11/7/2023     PHL219  

    AEP 4200       9/21/2023     PHS120
    AEP 4200       11/2/2023     PHS120  

    AEP 4230       10/17/2023    RCK203
    AEP 4230       11/30/2023    RCK203  

    AEP 5200       9/21/2023     PHS120
    AEP 5200       11/2/2023     PHS120  

    AEP 5230       10/17/2023    RCK203
    AEP 5230       11/30/2023    RCK203  

    ANSC 1500      10/26/2023    MRS146  

    ANSC 4200      9/21/2023     WRN151
    ANSC 4200      11/2/2023     MRS146  

    ANSC 4270      9/28/2023     STK146
    ANSC 4270      11/2/2023     STK146  

    ANSC 6200      9/21/2023     WRN151
    ANSC 6200      11/2/2023     MRS146  

    ANSC 6270      9/28/2023     STK146
    ANSC 6270      11/2/2023     STK146  

    ASL 1101       9/21/2023     GSH132, GSH142
    ASL 1101       11/2/2023     GSH132, GSH142
    ASL 1101       11/30/2023    GSH132, GSH142  

    BEE 2510       9/19/2023     RRB125
    BEE 2510       11/16/2023    RRB125  

    BEE 3310       9/21/2023     RRB105
    BEE 3310       11/2/2023     RRB105  

    BEE 3500       9/28/2023     RRBB15
    BEE 3500       11/9/2023     RRB125

    BEE 5310       9/21/2023     RRB105
    BEE 5310       11/2/2023     RRB105  

    BEE 5500       9/28/2023     RRBB15
    BEE 5500       11/9/2023     RRB125

    BIOAP 3110     9/19/2023     CVMS1210
    BIOAP 3110     10/24/2023    CVMS1210

    BIOAP 4270     9/28/2023     STK146
    BIOAP 4270     11/2/2023     STK146  

    BIOAP 6270     9/28/2023     STK146
    BIOAP 6270     11/2/2023     STK146  

    BIOEE 1780     9/28/2023     MRS146, RRB105, RRB125
    BIOEE 1780     11/7/2023     KND116  

    BIOMG 2800     9/12/2023     BKL200
    BIOMG 2800     10/17/2023    MRS146, RRB125
    BIOMG 2800     11/14/2023    MRS146, RRB125  

    BIOMG 2801     10/12/2023    RCK201  

    BIOMG 3300     9/28/2023     WRN175, WRNB25
    BIOMG 3300     10/31/2023    BKL200  

    BIOMG 3310     10/12/2023    GSHG64, KLRKG70 

    BIOMG 6300     9/28/2023     WRN175, WRNB25
    BIOMG 6300     10/31/2023    BKL200  

    BIOMG 6311     10/12/2023    GSHG64, KLRKG70 

    BIOMI 2900     10/5/2023     KND116  

    BIOMS 3110     9/19/2023     CVMS1210
    BIOMS 3110     10/24/2023    CVMS1210

    BME 1310       10/17/2023    KMBB11
    BME 1310       11/16/2023    WRN175  

    BME 2000       10/19/2023    HLSB14

    BME 3030       10/5/2023     KMBB11
    BME 3030       11/14/2023    PHL101  

    BME 4010       10/5/2023     GTSG01
    BME 4010       11/16/2023    IVS105  

    BME 4190       10/19/2023    PHL203  

    BME 5500       10/31/2023    HLSB14

    BME 6210       9/21/2023     OLH255
    BME 6210       11/2/2023     OLH255  

    BSOC 2101      10/3/2023     STL185  
    BSOC 2101      11/7/2023     MRS146, RRB125

    BTRY 3010      9/26/2023     IVS305
    BTRY 3010      11/2/2023     IVS305  

    BTRY 5010      9/26/2023     IVS305
    BTRY 5010      11/2/2023     IVS305  

    BTRY 6010      10/3/2023     IVS305
    BTRY 6010      10/31/2023    IVS305  

    CEE 1160       9/19/2023     PHL219
    CEE 1160       10/26/2023    PHL219  

    CEE 3040       10/3/2023     HLS110, HLSB14
    CEE 3040       11/7/2023     KLRKG70 

    CEE 3310       10/17/2023    HLSB14  

    CEE 4535       10/19/2023    HLS366

    CEE 5900       10/19/2023    OLH155, OLH165  

    CEE 6530       10/19/2023    HLS366

    CEE 6560       10/3/2023     THR203
    CEE 6560       11/7/2023     THR203  

    CHEM 1150      10/3/2023     BKL219, BKL335
    CHEM 1150      11/14/2023    BKL135, BKL335  

    CHEM 1560      10/3/2023     RCK201
    CHEM 1560      11/16/2023    MLT251, MLT253  

    CHEM 2070      10/5/2023     BKL119, BKL135, BKL200, BKL219, BKL335, RCK201, RCK203, RCK230
    CHEM 2070      11/16/2023    BKL119, BKL135, BKL200, BKL219, BKL335, RCK201, RCK203, RCK230

    CHEM 2080      9/26/2023     BKL200
    CHEM 2080      10/26/2023    BKL200  

    CHEM 2090      10/5/2023     MCG165, STL165, STL185, STL196, STL198
    CHEM 2090      11/16/2023    GSH132, GSH142, GSHG64, GSHG76, KLRKG70, PHS120

    CHEM 2150      10/5/2023     GSHG76
    CHEM 2150      11/16/2023    MLT228  

    CHEM 2510      10/3/2023     BKL200
    CHEM 2510      11/30/2023    BKL200, BKL219  

    CHEM 3570      9/19/2023     BKL200, BKL219, KND116, RCK201
    CHEM 3570      10/19/2023    BKL200, BKL219, BKL335, STL185
    CHEM 3570      11/16/2023    STL185, STL196, STL265, URHG01 

    CHEM 3600      9/26/2023     RCK115
    CHEM 3600      10/24/2023    BKL335
    CHEM 3600      11/14/2023    BKL125A  

    CHEM 3870      10/5/2023     RCK122
    CHEM 3870      11/16/2023    MCG165  

    CHEM 3890      10/19/2023    RCK203
    CHEM 3890      11/16/2023    RCK115, RCK122  

    CHEM 4500      9/21/2023     BKL335
    CHEM 4500      10/26/2023    BKL335  

    CHEM 6450      9/21/2023     BKL335
    CHEM 6450      10/26/2023    BKL335  

    CHEM 6890      10/19/2023    RCK203
    CHEM 6890      11/16/2023    MLT228  

    CHEME 3130     9/26/2023     OLH165
    CHEME 3130     11/14/2023    OLH165  

    CHEME 3240     9/28/2023     OLH165
    CHEME 3240     11/9/2023     OLH165  

    CHEME 4130     9/28/2023     PHL219
    CHEME 4130     11/7/2023     PHL219  

    CHEME 5320     10/5/2023     PHL219
    CHEME 5320     10/26/2023    OLH165
    CHEME 5320     11/16/2023    OLH165  

    CHEME 5610     10/19/2023    OLH255  

    CHEME 5730     10/17/2023    PHL203  

    CHEME 6110     10/12/2023    OLH245
    CHEME 6110     11/28/2023    OLH245

    CHEME 6130     10/5/2023     HLS110

    CHEME 6310     9/21/2023     OLH255
    CHEME 6310     11/2/2023     OLH255  

    COGST 1500     10/3/2023     BKL119, BKL135, KND116
    COGST 1500     11/14/2023    KND116, MVRG151, MVRG155

    COGST 1501     10/3/2023     BKL119, BKL135, KND116
    COGST 1501     11/14/2023    KND116, MVRG151, MVRG155

    COGST 2230     9/19/2023     IVS305
    COGST 2230     10/24/2023    WRNB25  

    COGST 2310     10/3/2023     GSHG76
    COGST 2310     11/7/2023     GSHG76  

    COGST 4740     10/12/2023    OLH155, OLH255  

    CS 1110        10/12/2023    IVS105, IVS305, STL185, URHG01
    CS 1110        11/21/2023    IVS105, IVS305, STL185, URHG01 

    CS 1112        10/17/2023    BKL200
    CS 1112        11/14/2023    GSHG76, KLRKG70 

    CS 2110        9/19/2023     STL185, STL196, URHG01
    CS 2110        11/14/2023    BKL200, BKL219, RCK201, RCK203 

    CS 2800        9/26/2023     GSH132, GSHG64, GSHG76, MRS146, RRB125
    CS 2800        11/16/2023    GTSG01, HLSB14, KMBB11, MRS146, OLH155

    CS 3410        9/19/2023     GSH132, GSHG64, GSHG76, KLRKG70
    CS 3410        11/14/2023    STL185, STL196  

    CS 4320        10/24/2023    GSH132, GSHG76, KLRKG70

    CS 4410        9/28/2023     GSH132, GSHG76, KLRKG70
    CS 4410        11/21/2023    GSHG64, GSHG76, KLRKG70

    CS 4420        10/12/2023    KMBB11
    CS 4420        11/21/2023    KMBB11  

    CS 4620        10/19/2023    RCK201  

    CS 4700        10/24/2023    OLH155, OLH165  

    CS 4740        10/12/2023    OLH155, OLH255  

    CS 4780        10/17/2023    STL185, STL196  

    CS 4787        10/31/2023    OLH155  

    CS 4820        10/5/2023     OLH155, OLH165, URHG01
    CS 4820        11/16/2023    KND116, WRNB25  

    CS 5154        10/5/2023     OLH255
    CS 5154        11/14/2023    OLH255  

    CS 5320        10/24/2023    GSH132, GSHG76, KLRKG70

    CS 5410        9/28/2023     GSH132, GSHG76, KLRKG70
    CS 5410        11/21/2023    GSHG64, GSHG76, KLRKG70

    CS 5430        10/26/2023    KMBB11  

    CS 5620        10/19/2023    RCK201  

    CS 5700        10/24/2023    OLH155, OLH165  

    CS 5740        10/12/2023    OLH155, OLH255  

    CS 5777        10/31/2023    OLH155  

    CS 5780        10/17/2023    STL185, STL196  

    CS 5820        10/5/2023     OLH155, OLH165, URHG01
    CS 5820        11/16/2023    KND116, WRNB25  

    DEA 1500       10/3/2023     BKL119, BKL135, KND116
    DEA 1500       11/14/2023    KND116, MVRG151, MVRG155

    DEA 1501       10/3/2023     BKL119, BKL135, KND116
    DEA 1501       11/14/2023    KND116, MVRG151, MVRG155

    EAS 3050       10/5/2023     WRN175  

    EAS 5051       10/5/2023     WRN175  

    ECE 2100       9/21/2023     HLSB14
    ECE 2100       10/26/2023    PHL101

    ECE 2300       10/5/2023     HLSB14
    ECE 2300       11/21/2023    PHL101  

    ECE 2720       10/19/2023    PHL101  

    ECE 3030       10/3/2023     OLH165
    ECE 3030       11/9/2023     PHL101  

    ECE 3250       10/5/2023     PHL101
    ECE 3250       11/16/2023    PHL101  

    ECE 4130       9/28/2023     PHL219
    ECE 4130       11/7/2023     PHL219  

    ECE 4360       10/19/2023    MCG165
    ECE 4360       11/30/2023    PHL101  

    ECE 4570       10/3/2023     PHL203
    ECE 4570       11/9/2023     PHL203  

    ECE 4750       10/12/2023    KMBB11
    ECE 4750       11/21/2023    KMBB11  

    ECE 4880       10/19/2023    IVS105  

    ECE 5690       10/19/2023    IVS105  

    ECE 5740       10/12/2023    KMBB11
    ECE 5740       11/21/2023    KMBB11  

    ECE 6630       10/24/2023    PHL203

    ECON 3030      9/26/2023     KLRKG70
    ECON 3030      10/24/2023    IVS305 

    ECON 3130      10/3/2023     KLRKG70
    ECON 3130      10/26/2023    KLRKG70 

    ECON 6190      11/7/2023     GSHG64  

    ENGRD 2020     9/21/2023     STL185
    ENGRD 2020     10/26/2023    STL185  

    ENGRD 2100     9/21/2023     HLSB14
    ENGRD 2100     10/26/2023    PHL101  

    ENGRD 2110     9/19/2023     STL185, STL196, URHG01
    ENGRD 2110     11/14/2023    BKL200, BKL219, RCK201, RCK203 

    ENGRD 2190     10/3/2023     OLH245
    ENGRD 2190     10/31/2023    OLH245
    ENGRD 2190     11/21/2023    OLH245 

    ENGRD 2202     10/19/2023    HLSB14

    ENGRD 2210     9/26/2023     OLH155, OLH255
    ENGRD 2210     10/31/2023    STL185  

    ENGRD 2300     10/5/2023     HLSB14
    ENGRD 2300     11/21/2023    PHL101  

    ENGRD 2510     9/19/2023     RRB125
    ENGRD 2510     11/16/2023    RRB125  

    ENGRD 2610     9/26/2023     THR203
    ENGRD 2610     11/7/2023     THR205  

    ENGRD 2700     10/3/2023     OLH155, OLH255
    ENGRD 2700     11/7/2023     OLH155, OLH255  

    ENGRD 2720     10/19/2023    PHL101  

    ENGRG 2270     10/19/2023    KMBB11  

    ENGRI 1101     10/3/2023     KMBB11
    ENGRI 1101     11/14/2023    KMBB11  

    ENGRI 1120     10/3/2023     PHL403, PHL407

    ENGRI 1140     10/3/2023     STL196
    ENGRI 1140     11/14/2023    HLSB14  

    ENGRI 1160     9/19/2023     PHL219
    ENGRI 1160     10/26/2023    PHL219  

    ENGRI 1190     10/19/2023    RCK115  

    ENGRI 1200     10/17/2023    HLS110  

    ENGRI 1270     10/19/2023    KMBB11  

    ENGRI 1310     10/17/2023    KMBB11
    ENGRI 1310     11/16/2023    WRN175  

    ENMGT 5900     10/19/2023    OLH155, OLH165  

    ENTOM 2100     10/3/2023     STL185  
    ENTOM 2100     11/7/2023     MRS146, RRB125

    ENTOM 3755     10/17/2023    CMS2123

    FDSC 3940      10/31/2023    STK146  

    FDSC 4210      9/21/2023     STK146
    FDSC 4210      11/16/2023    STK146  

    FDSC 5210      9/21/2023     STK146
    FDSC 5210      11/16/2023    STK146  

    FSAD 1250      11/9/2023     MVRG151, MVRG155

    GDEV 3280      9/14/2023     KND116, MLT228
    GDEV 3280      10/19/2023    KND116, MVRG151
    GDEV 3280      11/21/2023    KND116, MVRG151 

    HADM 1210      9/21/2023     STL198, STL398
    HADM 1210      11/2/2023     STL196, STL265  

    HADM 1350      10/19/2023    IVS305  

    HADM 1361      10/5/2023     GSH132, GSH142
    HADM 1361      11/16/2023    IVS305  

    HADM 1740 001  9/28/2023     STL365
    HADM 1740 001  11/7/2023     STL365

    HADM 1740 002  10/17/2023    STL365
    HADM 1740 002  11/14/2023    STL365  

    HADM 1740 003  10/17/2023    STL365
    HADM 1740 003  11/14/2023    STL365  

    HADM 1740 004  10/17/2023    STL365
    HADM 1740 004  11/14/2023    STL365

    HADM 2021      9/26/2023     MLT228, MLT251, MLT253, MLT406
    HADM 2021      10/24/2023    HLS110, HLSB14, KMBB11 

    HADM 2210      9/21/2023     GSHG64, GSHG76
    HADM 2210      10/26/2023    IVS305  

    HADM 2220 002  9/19/2023     STL165, STL198, STL396, STL398
    HADM 2220 002  10/17/2023    STL165, STL198, STL396, STL398
    HADM 2220 002  11/14/2023    STL165, STL198, STL396, STL398 

    HADM 2220 003  9/19/2023     STL165, STL198, STL396, STL398
    HADM 2220 003  10/17/2023    STL165, STL198, STL396, STL398
    HADM 2220 003  11/14/2023    STL165, STL198, STL396, STL398 

    HADM 2560      10/19/2023    WRNB25

    HADM 3010      9/26/2023     MLT228, MLT251, MLT253, MLT406
    HADM 3010      10/24/2023    HLS110, HLSB14, KMBB11 

    HADM 3870      10/3/2023     URH202, URHG01
    HADM 3870      11/2/2023     STL185  

    HADM 4130      11/7/2023     STL398  

    HADM 4140      11/9/2023     STL265  

    HADM 4300      10/24/2023    STL185, STL196, STL265, URHG01 

    HADM 4360      10/19/2023    STL265  

    HADM 4470      10/26/2023    STL196  

    HADM 4810      10/5/2023     STL265
    HADM 4810      11/7/2023     STL198  

    HADM 5360      10/19/2023    STL265  

    HADM 6130      11/7/2023     STL398  

    HADM 6140      11/9/2023     STL265  

    HADM 7230      9/21/2023     KMBB11
    HADM 7230      10/19/2023    STL196, STL198
    HADM 7230      11/16/2023    OLH255  

    HD 2230        9/19/2023     IVS305
    HD 2230        10/24/2023    WRNB25  

    ILRID 1520     10/12/2023    KND116  

    ILRLR 4890     10/17/2023    IVS105  

    ILRLR 6890     10/17/2023    IVS105  

    ILRST 2100     10/17/2023    IVS305, URHG01
    ILRST 2100     11/14/2023    IVS305, URHG01  

    ILRST 6100     10/3/2023     IVS305
    ILRST 6100     10/31/2023    IVS305  

    INFO 1200      10/19/2023    GSH132, GSHG64, GSHG76, KLRKG70

    LATIN 1201     10/3/2023     GSH142

    LATIN 5211     10/3/2023     GSH142

    LING 4474      10/12/2023    OLH155, OLH255  

    MAE 1270       10/19/2023    KMBB11  

    MAE 2020       9/21/2023     STL185
    MAE 2020       10/26/2023    STL185  

    MAE 2210       9/26/2023     OLH155, OLH255
    MAE 2210       10/31/2023    STL185  

    MAE 2270       10/19/2023    KMBB11  

    MAE 3050       9/19/2023     GTSG01
    MAE 3050       10/31/2023    GTSG01  

    MAE 3120       9/28/2023     KMBB11
    MAE 3120       11/9/2023     KMBB11

    MAE 3230       9/21/2023     OLH155, OLH165
    MAE 3230       10/26/2023    OLH155, OLH255  

    MAE 3260       10/17/2023    OLH155, OLH165
    MAE 3260       11/7/2023     URHG01  

    MAE 3270       10/5/2023     IVS305
    MAE 3270       11/2/2023     URHG01  

    MAE 3870       9/26/2023     GTSG01
    MAE 3870       11/9/2023     GTSG01  

    MAE 4060       10/19/2023    THR205  

    MAE 4351       10/17/2023    PHL203  

    MAE 4580       9/28/2023     PHL219
    MAE 4580       11/7/2023     PHL219  

    MAE 4660       10/5/2023     GTSG01
    MAE 4660       11/16/2023    IVS105  

    MAE 4700       10/12/2023    GTSG01
    MAE 4700       11/2/2023     GTSG01  

    MAE 4701       10/12/2023    GTSG01
    MAE 4701       11/2/2023     GTSG01  

    MAE 4730       11/2/2023     PHL203  

    MAE 4780       10/3/2023     BRD140
    MAE 4780       10/31/2023    BRD140  

    MAE 5065       10/19/2023    THR205  

    MAE 5700       10/12/2023    GTSG01
    MAE 5700       11/2/2023     GTSG01  

    MAE 5730       11/2/2023     PHL203  

    MAE 5780       10/3/2023     BRD140
    MAE 5780       10/31/2023    BRD140  

    MAE 5930       10/26/2023    GTSG01  

    MATH 1110      9/26/2023     STL185, STL196, URHG01
    MATH 1110      11/9/2023     IVS217, IVS305, STL185, STL196

    MATH 1120      9/21/2023     IVS105, IVS305
    MATH 1120      11/9/2023     GSHG76, MLT228

    MATH 1910      9/28/2023     BKL200, BKL219, RCK201, RCK203
    MATH 1910      11/7/2023     BKL200, BKL219, RCK201, RCK203 

    MATH 1920      9/28/2023     MLT228, STL165, STL185, STL196, STL265
    MATH 1920      11/7/2023     MLT228, STL165, STL185, STL196, STL265 

    MATH 2210      9/21/2023     URHG01
    MATH 2210      11/9/2023     GSHG64, KLRKG70 

    MATH 2220      9/28/2023     MLT406
    MATH 2220      11/9/2023     MLT406

    MATH 2930      9/28/2023     HLSB14, OLH155, OLH255, URHG01
    MATH 2930      11/9/2023     BKL200, BKL219, RCK201, RCK203 

    MATH 2940      9/28/2023     GSHG64, IVS105, IVS217, IVS305, KND116
    MATH 2940      11/9/2023     IVS105, KND116, URHG01

    MATH 3110      10/5/2023     MLT228
    MATH 3110      11/9/2023     GSH132  

    MATH 3320      10/31/2023    MLT228  

    MSE 1140       10/3/2023     STL196
    MSE 1140       11/14/2023    HLSB14  

    MSE 1190       10/19/2023    RCK115  

    MSE 2610       9/26/2023     THR203
    MSE 2610       11/7/2023     THR205  

    MSE 3010       10/12/2023    HLSB14
    MSE 3010       11/30/2023    HLSB14  

    MSE 3030       10/3/2023     GTSG01
    MSE 3030       11/14/2023    GTSG01  

    MSE 4020       9/28/2023     KMBB11
    MSE 4020       11/9/2023     KMBB11

    MSE 5070       10/17/2023    PHL203  

    MSE 5210       10/17/2023    PHL219  

    MSE 5320       10/5/2023     PHL219
    MSE 5320       10/26/2023    OLH165
    MSE 5320       11/16/2023    OLH165  

    MSE 5410       10/19/2023    MCG165
    MSE 5410       11/30/2023    PHL101  

    MSE 5801       10/19/2023    HLS110  

    MSE 5810       10/12/2023    HLSB14
    MSE 5810       11/30/2023    HLSB14  

    MSE 5820       9/28/2023     KMBB11
    MSE 5820       11/9/2023     KMBB11

    MSE 5830       10/3/2023     GTSG01
    MSE 5830       11/14/2023    GTSG01  

    NS 3200        9/14/2023     MVRG151, MVRG155
    NS 3200        10/12/2023    MVRG151, MVRG155
    NS 3200        11/7/2023     MVRG151, MVRG155
    NS 3200        11/30/2023    MVRG151, MVRG155

    NTRES 4560     9/21/2023     FERNOW
    NTRES 4560     10/26/2023    FERNOW

    ORIE 3150      10/17/2023    KLRKG70
    ORIE 3150      11/14/2023    OLH155  

    ORIE 3300      10/3/2023     GSH132, GSHG64
    ORIE 3300      11/7/2023     IVS305  

    ORIE 3500      9/21/2023     PHL101, PHL219
    ORIE 3500      11/2/2023     OLH155  

    ORIE 4330      10/5/2023     PHL203  

    ORIE 4580      10/19/2023    URHG01  

    ORIE 5300      10/3/2023     GSH132, GSHG64
    ORIE 5300      11/7/2023     IVS305  

    ORIE 5330      10/5/2023     PHL203  

    ORIE 5500      9/21/2023     PHL101, PHL219
    ORIE 5500      11/2/2023     OLH155  

    ORIE 5580      10/19/2023    URHG01  

    ORIE 5581      10/24/2023    PHL219  

    ORIE 6700      10/19/2023    BRD140  

    PUBPOL 2101    10/3/2023     RCK203
    PUBPOL 2101    11/2/2023     MVRG151, MVRG155

    PUBPOL 2300    10/3/2023     MVRG151, MVRG155
    PUBPOL 2300    11/16/2023    MVRG151, MVRG155

    PUBPOL 2350    9/21/2023     KND116, MVRG151, MVRG155
    PUBPOL 2350    10/31/2023    KND116, MVRG151, MVRG155

    PUBPOL 3280    9/14/2023     KND116, MLT228
    PUBPOL 3280    10/19/2023    KND116, MVRG151
    PUBPOL 3280    11/21/2023    KND116, MVRG151 

    PHIL 2310      10/3/2023     GSHG76
    PHIL 2310      11/7/2023     GSHG76  

    PHYS 1112      9/21/2023     RCK201, RCK203
    PHYS 1112      10/26/2023    RCK201, RCK203  

    PHYS 1116      9/14/2023     RCK203
    PHYS 1116      10/26/2023    RCK230, RCK231  

    PHYS 2207      9/26/2023     RCK122, RCK201, RCK203, RCK230
    PHYS 2207      10/24/2023    KND116, MLT228, MLT253 

    PHYS 2213      10/24/2023    BKL200, BKL219, RCK201, RCK203 

    PHYS 2214      9/21/2023     BKL119, BKL135
    PHYS 2214      10/24/2023    BKL119, BKL135  

    PHYS 2218      10/19/2023    RCK230  

    PHYS 4230      10/17/2023    RCK203
    PHYS 4230      11/30/2023    RCK203  

    PLSCI 1101     9/14/2023     WRNB25
    PLSCI 1101     10/24/2023    RRB125  

    PSYCH 1500     10/3/2023     BKL119, BKL135, KND116
    PSYCH 1500     11/14/2023    KND116, MVRG151, MVRG155

    PSYCH 1501     10/3/2023     BKL119, BKL135, KND116
    PSYCH 1501     11/14/2023    KND116, MVRG151, MVRG155

    PSYCH 2230     9/19/2023     IVS305
    PSYCH 2230     10/24/2023    WRNB25  

    STS 1201       10/19/2023    GSH132, GSHG64, GSHG76, KLRKG70

    STSCI 2100     10/17/2023    IVS305, URHG01
    STSCI 2100     11/14/2023    IVS305, URHG01  

    STSCI 2150     10/3/2023     MLT228, MLT251, MLT253
    STSCI 2150     10/26/2023    MLT228, MLT251, MLT253
    STSCI 2150     11/9/2023     OLH155, OLH255  

    STSCI 2200     9/26/2023     IVS305
    STSCI 2200     11/2/2023     IVS305  

    STSCI 5150     10/3/2023     MLT228, MLT251, MLT253
    STSCI 5150     10/26/2023    MLT228, MLT251, MLT253
    STSCI 5150     11/9/2023     OLH155, OLH255  

    STSCI 5200     9/26/2023     IVS305
    STSCI 5200     11/2/2023     IVS305  

    SYSEN 5300     10/26/2023    GTSG01  

    SYSEN 6300     10/26/2023    GTSG01  

    VTBMS 3460     9/19/2023     CVMS1210
    VTBMS 3460     10/24/2023    CVMS1210
    """

    # Prompt the user to input their enrolled courses
    print("Enter your enrolled courses (one per line), and press Enter twice when you're done:")
    enrolled_courses = [course_entry.get() for course_entry in course_entries]

    while True:
        course_input = input()
        if not course_input:
            break
        enrolled_courses.append(course_input)

    # Create a new iCal calendar
    cal = Calendar()

    # Loop through the schedule data and filter based on enrolled courses
    for line in schedule_data.split('\n'):
        if line.strip():  # Ignore empty lines
            course, date_str, location = re.split(r'\s{2,}', line.strip())

            # Check if the course is in the list of enrolled courses
            if course in enrolled_courses:
                # Parse date string
                date_parts = date_str.split('/')
                month, day, year = map(int, date_parts)
                start_time = "19:30"  # 7:30 PM
                end_time = "21:00"    # 9:00 PM

                # Create iCal event
                event = Event()
                event.add('summary', course)
                start_datetime = datetime(year, month, day, int(start_time[:2]), int(start_time[3:]))
                end_datetime = start_datetime + timedelta(hours=1, minutes=30)
                event.add('dtstart', start_datetime)
                event.add('dtend', end_datetime)            
                event.add('location', location)

                # Add event to the calendar
                cal.add_component(event)

    # Save the iCal data to a file
    with open('prelim_schedule.ics', 'wb') as f:
        f.write(cal.to_ical())
    messagebox.showinfo("Success", "Course schedule generated and saved as 'course_schedule.ics'")

app = tk.Tk()
app.title("Prelim Schedule Generator")

frame = ttk.Frame(app)
frame.grid(column=0, row=0, padx=10, pady=10)

generate_button = ttk.Button(frame, text="Generate Schedule", command=generate_schedule)
generate_button.grid(column=0, row=0, padx=10, pady=5)

app.mainloop()
