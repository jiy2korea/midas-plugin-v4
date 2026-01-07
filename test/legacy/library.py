import math
from re import U

# Rolled H-section Data
HBeamData =  {
    "H-100X50X5X7": {"H": 100, "B": 50, "t1": 5, "t2": 7, "r": 8, "W": 9.3, "A": 11.85, "Ix": 180, "Iy": 14.8, "ix": 3.96, "iy": 1.12, "Zx": 44.1, "Zy": 9.52},
    "H-150X75X5X7": {"H": 150, "B": 75, "t1": 5, "t2": 7, "r": 8, "W": 14, "A": 17.85, "Ix": 666, "Iy": 49.5, "ix": 6.11, "iy": 1.66, "Zx": 102, "Zy": 20.8},
    "H-148X100X6X9": {"H": 148, "B": 100, "t1": 6, "t2": 9, "r": 11, "W": 21.1, "A": 26.84, "Ix": 1020, "Iy": 151, "ix": 6.17, "iy": 2.37, "Zx": 157, "Zy": 46.7},
    "H-198X99X4.5X7": {"H": 198, "B": 99, "t1": 4.5, "t2": 7, "r": 11, "W": 18.2, "A": 23.18, "Ix": 1580, "Iy": 114, "ix": 8.26, "iy": 2.21, "Zx": 180, "Zy": 35.7},
    "H-200X100X5.5X8": {"H": 200, "B": 100, "t1": 5.5, "t2": 8, "r": 11, "W": 21.3, "A": 27.16, "Ix": 1840, "Iy": 134, "ix": 8.24, "iy": 2.22, "Zx": 209, "Zy": 41.9},
    "H-194X150X6X9": {"H": 194, "B": 150, "t1": 6, "t2": 9, "r": 13, "W": 30.6, "A": 39.01, "Ix": 2690, "Iy": 507, "ix": 8.3, "iy": 3.61, "Zx": 309, "Zy": 104},
    "H-248X124X5X8": {"H": 248, "B": 124, "t1": 5, "t2": 8, "r": 12, "W": 25.7, "A": 32.68, "Ix": 3540, "Iy": 255, "ix": 10.4, "iy": 2.79, "Zx": 319, "Zy": 63.6},
    "H-250X125X6X9": {"H": 250, "B": 125, "t1": 6, "t2": 9, "r": 12, "W": 29.6, "A": 37.66, "Ix": 4050, "Iy": 294, "ix": 10.4, "iy": 2.79, "Zx": 366, "Zy": 73.1},
    "H-244X175X7X11": {"H": 244, "B": 175, "t1": 7, "t2": 11, "r": 16, "W": 44.1, "A": 56.24, "Ix": 6120, "Iy": 984, "ix": 10.4, "iy": 4.18, "Zx": 558, "Zy": 173},
    "H-298X149X5.5X8": {"H": 298, "B": 149, "t1": 5.5, "t2": 8, "r": 13, "W": 32, "A": 40.8, "Ix": 6320, "Iy": 442, "ix": 12.4, "iy": 3.29, "Zx": 475, "Zy": 91.8},
    "H-300X150X6.5X9": {"H": 300, "B": 150, "t1": 6.5, "t2": 9, "r": 13, "W": 36.7, "A": 46.78, "Ix": 7210, "Iy": 508, "ix": 12.4, "iy": 3.29, "Zx": 542, "Zy": 105},
    "H-294X200X8X12": {"H": 294, "B": 200, "t1": 8, "t2": 12, "r": 18, "W": 56.8, "A": 72.38, "Ix": 11300, "Iy": 1600, "ix": 12.5, "iy": 4.71, "Zx": 859, "Zy": 247},
    "H-298X201X9X14": {"H": 298, "B": 201, "t1": 9, "t2": 14, "r": 18, "W": 65.4, "A": 83.36, "Ix": 13300, "Iy": 1900, "ix": 12.6, "iy": 4.77, "Zx": 1000, "Zy": 291},
    "H-346X174X6X9": {"H": 346, "B": 174, "t1": 6, "t2": 9, "r": 14, "W": 41.4, "A": 52.68, "Ix": 11100, "Iy": 792, "ix": 14.5, "iy": 3.88, "Zx": 716, "Zy": 140},
    "H-350X175X7X11": {"H": 350, "B": 175, "t1": 7, "t2": 11, "r": 14, "W": 49.6, "A": 63.14, "Ix": 13600, "Iy": 984, "ix": 14.7, "iy": 3.95, "Zx": 868, "Zy": 174},
    "H-354X176X8X13": {"H": 354, "B": 176, "t1": 8, "t2": 13, "r": 14, "W": 57.8, "A": 73.68, "Ix": 16100, "Iy": 1180, "ix": 14.8, "iy": 4.01, "Zx": 1020, "Zy": 208},
    "H-336X249X8X12": {"H": 336, "B": 249, "t1": 8, "t2": 12, "r": 20, "W": 69.2, "A": 88.15, "Ix": 18500, "Iy": 3090, "ix": 14.5, "iy": 5.92, "Zx": 1220, "Zy": 380},
    "H-340X250X9X14": {"H": 340, "B": 250, "t1": 9, "t2": 14, "r": 20, "W": 79.7, "A": 101.5, "Ix": 21700, "Iy": 3650, "ix": 14.6, "iy": 6, "Zx": 1410, "Zy": 447},
    "H-396X199X7X11": {"H": 396, "B": 199, "t1": 7, "t2": 11, "r": 16, "W": 56.6, "A": 72.16, "Ix": 20000, "Iy": 1450, "ix": 16.7, "iy": 4.48, "Zx": 1130, "Zy": 224},
    "H-400X200X8X13": {"H": 400, "B": 200, "t1": 8, "t2": 13, "r": 16, "W": 66, "A": 84.12, "Ix": 23700, "Iy": 1740, "ix": 16.8, "iy": 4.54, "Zx": 1330, "Zy": 268},
    "H-404X201X9X15": {"H": 404, "B": 201, "t1": 9, "t2": 15, "r": 16, "W": 75.5, "A": 96.16, "Ix": 27500, "Iy": 2030, "ix": 16.9, "iy": 4.6, "Zx": 1530, "Zy": 312},
    "H-386X299X9X14": {"H": 386, "B": 299, "t1": 9, "t2": 14, "r": 22, "W": 94.3, "A": 120.1, "Ix": 33700, "Iy": 6240, "ix": 16.7, "iy": 7.81, "Zx": 1920, "Zy": 637},
    "H-390X300X10X16": {"H": 390, "B": 300, "t1": 10, "t2": 16, "r": 22, "W": 107, "A": 136, "Ix": 38700, "Iy": 7210, "ix": 16.9, "iy": 7.28, "Zx": 2190, "Zy": 733},
    "H-446X199X8X12": {"H": 446, "B": 199, "t1": 8, "t2": 12, "r": 18, "W": 66.2, "A": 84.3, "Ix": 28700, "Iy": 1580, "ix": 18.5, "iy": 4.33, "Zx": 1450, "Zy": 247},
    "H-450X200X9X14": {"H": 450, "B": 200, "t1": 9, "t2": 14, "r": 18, "W": 76, "A": 96.76, "Ix": 33500, "Iy": 1870, "ix": 18.6, "iy": 4.4, "Zx": 1680, "Zy": 291},
    "H-434X299X10X15": {"H": 434, "B": 299, "t1": 10, "t2": 15, "r": 24, "W": 106, "A": 135, "Ix": 46800, "Iy": 6690, "ix": 18.6, "iy": 7.04, "Zx": 2380, "Zy": 686},
    "H-440X300X11X18": {"H": 440, "B": 300, "t1": 11, "t2": 18, "r": 24, "W": 124, "A": 157.4, "Ix": 56100, "Iy": 8110, "ix": 18.9, "iy": 7.18, "Zx": 2820, "Zy": 828},
    "H-496X199X9X14": {"H": 496, "B": 199, "t1": 9, "t2": 14, "r": 20, "W": 79.5, "A": 101.3, "Ix": 41900, "Iy": 1840, "ix": 20.3, "iy": 4.27, "Zx": 1910, "Zy": 290},
    "H-500X200X10X16": {"H": 500, "B": 200, "t1": 10, "t2": 16, "r": 20, "W": 89.6, "A": 114.2, "Ix": 47800, "Iy": 2140, "ix": 20.5, "iy": 4.33, "Zx": 2180, "Zy": 335},
    "H-506X201X11X19": {"H": 506, "B": 201, "t1": 11, "t2": 19, "r": 20, "W": 103, "A": 131.3, "Ix": 56500, "Iy": 2580, "ix": 20.7, "iy": 4.43, "Zx": 2540, "Zy": 401},
    "H-482X300X11X15": {"H": 482, "B": 300, "t1": 11, "t2": 15, "r": 26, "W": 114, "A": 145.5, "Ix": 60400, "Iy": 6760, "ix": 20.4, "iy": 6.82, "Zx": 2790, "Zy": 695},
    "H-488X300X11X18": {"H": 488, "B": 300, "t1": 11, "t2": 18, "r": 26, "W": 128, "A": 163.5, "Ix": 71000, "Iy": 8110, "ix": 20.8, "iy": 7.04, "Zx": 3230, "Zy": 830},
    "H-596X199X10X15": {"H": 596, "B": 199, "t1": 10, "t2": 15, "r": 22, "W": 94.6, "A": 120.5, "Ix": 68700, "Iy": 1980, "ix": 23.9, "iy": 4.05, "Zx": 2650, "Zy": 315},
    "H-600X200X11X17": {"H": 600, "B": 200, "t1": 11, "t2": 17, "r": 22, "W": 106, "A": 134.4, "Ix": 77600, "Iy": 2280, "ix": 24, "iy": 4.12, "Zx": 2980, "Zy": 361},
    "H-606X201X12X20": {"H": 606, "B": 201, "t1": 12, "t2": 20, "r": 22, "W": 120, "A": 152.5, "Ix": 90400, "Iy": 2720, "ix": 24.3, "iy": 4.22, "Zx": 3430, "Zy": 429},
    "H-612X202X13X23": {"H": 612, "B": 202, "t1": 13, "t2": 23, "r": 22, "W": 134, "A": 170.7, "Ix": 103000, "Iy": 3180, "ix": 24.6, "iy": 4.31, "Zx": 3890, "Zy": 498},
    "H-582X300X12X17": {"H": 582, "B": 300, "t1": 12, "t2": 17, "r": 28, "W": 137, "A": 174.5, "Ix": 103000, "Iy": 7670, "ix": 24.3, "iy": 6.63, "Zx": 3960, "Zy": 793},
    "H-588X300X12X20": {"H": 588, "B": 300, "t1": 12, "t2": 20, "r": 28, "W": 151, "A": 192.5, "Ix": 118000, "Iy": 9020, "ix": 24.8, "iy": 6.85, "Zx": 4490, "Zy": 928},
    "H-594X302X14X23": {"H": 594, "B": 302, "t1": 14, "t2": 23, "r": 28, "W": 175, "A": 222.4, "Ix": 137000, "Iy": 10600, "ix": 24.9, "iy": 6.9, "Zx": 5200, "Zy": 1080},
    "H-692X300X13X20": {"H": 692, "B": 300, "t1": 13, "t2": 20, "r": 28, "W": 166, "A": 211.5, "Ix": 172000, "Iy": 9020, "ix": 28.6, "iy": 6.53, "Zx": 5630, "Zy": 936},
    "H-700X300X13X24": {"H": 700, "B": 300, "t1": 13, "t2": 24, "r": 28, "W": 185, "A": 235.5, "Ix": 201000, "Iy": 10800, "ix": 29.3, "iy": 6.78, "Zx": 6460, "Zy": 1120},
    "H-708X302X15X28": {"H": 708, "B": 302, "t1": 15, "t2": 28, "r": 28, "W": 215, "A": 273.6, "Ix": 237000, "Iy": 12900, "ix": 29.4, "iy": 6.86, "Zx": 7560, "Zy": 1320},
    "H-792X300X14X22": {"H": 792, "B": 300, "t1": 14, "t2": 22, "r": 28, "W": 191, "A": 243.4, "Ix": 254000, "Iy": 9930, "ix": 32.3, "iy": 6.39, "Zx": 7290, "Zy": 1040},
    "H-800X300X14X26": {"H": 800, "B": 300, "t1": 14, "t2": 26, "r": 28, "W": 210, "A": 267.4, "Ix": 292000, "Iy": 11700, "ix": 33, "iy": 6.62, "Zx": 8240, "Zy": 1220},
    "H-808X302X16X30": {"H": 808, "B": 302, "t1": 16, "t2": 30, "r": 28, "W": 241, "A": 307.6, "Ix": 339000, "Iy": 13800, "ix": 33.2, "iy": 6.7, "Zx": 9530, "Zy": 1430},
    "H-890X299X15X23": {"H": 890, "B": 299, "t1": 15, "t2": 23, "r": 18, "W": 210, "A": 266.8, "Ix": 339000, "Iy": 10300, "ix": 35.6, "iy": 6.2, "Zx": 8910, "Zy": 1080},
    "H-900X300X16X28": {"H": 900, "B": 300, "t1": 16, "t2": 28, "r": 18, "W": 240, "A": 305.8, "Ix": 404000, "Iy": 12600, "ix": 36.4, "iy": 6.43, "Zx": 10500, "Zy": 1320},
    "H-912X302X18X34": {"H": 912, "B": 302, "t1": 18, "t2": 34, "r": 18, "W": 283, "A": 360.1, "Ix": 491000, "Iy": 15700, "ix": 36.9, "iy": 6.56, "Zx": 12500, "Zy": 1630},
    "H-918X303X19X37": {"H": 918, "B": 303, "t1": 19, "t2": 37, "r": 18, "W": 304, "A": 387.4, "Ix": 535000, "Iy": 17200, "ix": 37.2, "iy": 6.67, "Zx": 13400, "Zy": 1780},
    "H-100X100X6X8": {"H": 100, "B": 100, "t1": 6, "t2": 8, "r": 10, "W": 17.2, "A": 21.9, "Ix": 383, "Iy": 134, "ix": 4.18, "iy": 2.47, "Zx": 87.6, "Zy": 41.2},
    "H-125X125X6.5X9": {"H": 125, "B": 125, "t1": 6.5, "t2": 9, "r": 10, "W": 23.8, "A": 30.31, "Ix": 847, "Iy": 293, "ix": 5.29, "iy": 3.11, "Zx": 154, "Zy": 71.9},
    "H-150X150X7X10": {"H": 150, "B": 150, "t1": 7, "t2": 10, "r": 11, "W": 31.5, "A": 40.14, "Ix": 1640, "Iy": 563, "ix": 6.39, "iy": 3.75, "Zx": 246, "Zy": 115},
    "H-200X200X8X12": {"H": 200, "B": 200, "t1": 8, "t2": 12, "r": 13, "W": 49.9, "A": 63.53, "Ix": 4720, "Iy": 1600, "ix": 8.62, "iy": 5.02, "Zx": 525, "Zy": 244},
    "H-200X204X12X12": {"H": 200, "B": 204, "t1": 12, "t2": 12, "r": 13, "W": 56.2, "A": 71.53, "Ix": 4980, "Iy": 1700, "ix": 8.35, "iy": 4.88, "Zx": 565, "Zy": 257},
    "H-208X202X10X16": {"H": 208, "B": 202, "t1": 10, "t2": 16, "r": 13, "W": 65.7, "A": 83.69, "Ix": 6530, "Iy": 2200, "ix": 8.83, "iy": 5.13, "Zx": 710, "Zy": 332},
    "H-244X252X11X11": {"H": 244, "B": 252, "t1": 11, "t2": 11, "r": 16, "W": 64.4, "A": 82.06, "Ix": 8790, "Iy": 2940, "ix": 10.3, "iy": 5.98, "Zx": 805, "Zy": 358},
    "H-248X249X8X13": {"H": 248, "B": 249, "t1": 8, "t2": 13, "r": 16, "W": 66.5, "A": 84.7, "Ix": 9930, "Iy": 3350, "ix": 10.8, "iy": 6.29, "Zx": 883, "Zy": 408},
    "H-250X250X9X14": {"H": 250, "B": 250, "t1": 9, "t2": 14, "r": 16, "W": 72.4, "A": 92.18, "Ix": 10800, "Iy": 3650, "ix": 10.8, "iy": 6.29, "Zx": 960, "Zy": 444},
    "H-250X255X14X14": {"H": 250, "B": 255, "t1": 14, "t2": 14, "r": 16, "W": 82.2, "A": 104.7, "Ix": 11500, "Iy": 3880, "ix": 10.5, "iy": 6.09, "Zx": 1040, "Zy": 468},
    "H-294X302X12X12": {"H": 294, "B": 302, "t1": 12, "t2": 12, "r": 18, "W": 84.5, "A": 107.7, "Ix": 16900, "Iy": 5520, "ix": 12.5, "iy": 7.16, "Zx": 1280, "Zy": 560},
    "H-298X299X9X14": {"H": 298, "B": 299, "t1": 9, "t2": 14, "r": 18, "W": 87, "A": 110.8, "Ix": 18800, "Iy": 6240, "ix": 13, "iy": 7.5, "Zx": 1390, "Zy": 634},
    "H-304X301X11X17": {"H": 304, "B": 301, "t1": 11, "t2": 17, "r": 18, "W": 106, "A": 134.8, "Ix": 23400, "Iy": 7730, "ix": 13.2, "iy": 7.57, "Zx": 1710, "Zy": 781},
    "H-310X305X15X20": {"H": 310, "B": 305, "t1": 15, "t2": 20, "r": 18, "W": 130, "A": 165.3, "Ix": 28150, "Iy": 9460, "ix": 13.2, "iy": 7.6, "Zx": 2080, "Zy": 949},
    "H-310X310X20X20": {"H": 310, "B": 310, "t1": 20, "t2": 20, "r": 18, "W": 142, "A": 180.8, "Ix": 29390, "Iy": 9940, "ix": 12.8, "iy": 7.5, "Zx": 2200, "Zy": 992},
    "H-338X351X13X13": {"H": 338, "B": 351, "t1": 13, "t2": 13, "r": 20, "W": 106, "A": 135.3, "Ix": 28200, "Iy": 9380, "ix": 14.4, "iy": 8.33, "Zx": 1850, "Zy": 872},
    "H-344X348X10X16": {"H": 344, "B": 348, "t1": 10, "t2": 16, "r": 20, "W": 115, "A": 146, "Ix": 33300, "Iy": 11200, "ix": 15.1, "iy": 8.78, "Zx": 2120, "Zy": 980},
    "H-344X354X16X16": {"H": 344, "B": 354, "t1": 16, "t2": 16, "r": 20, "W": 131, "A": 166.6, "Ix": 35300, "Iy": 11800, "ix": 14.6, "iy": 8.43, "Zx": 2250, "Zy": 1020},
    "H-350X350X12X19": {"H": 350, "B": 350, "t1": 12, "t2": 19, "r": 20, "W": 137, "A": 173.9, "Ix": 40300, "Iy": 13600, "ix": 15.2, "iy": 8.84, "Zx": 2550, "Zy": 1180},
    "H-350X357X19X19": {"H": 350, "B": 357, "t1": 19, "t2": 19, "r": 20, "W": 156, "A": 191.4, "Ix": 42800, "Iy": 14400, "ix": 14.7, "iy": 8.53, "Zx": 2760, "Zy": 1240},
    "H-388X402X15X15": {"H": 388, "B": 402, "t1": 15, "t2": 15, "r": 22, "W": 140, "A": 178.5, "Ix": 49000, "Iy": 16300, "ix": 16.6, "iy": 9.54, "Zx": 2800, "Zy": 1240},
    "H-394X398X11X18": {"H": 394, "B": 398, "t1": 11, "t2": 18, "r": 22, "W": 147, "A": 186.8, "Ix": 56100, "Iy": 18900, "ix": 17.3, "iy": 10.1, "Zx": 3120, "Zy": 1440},
    "H-394X405X18X18": {"H": 394, "B": 405, "t1": 18, "t2": 18, "r": 22, "W": 168, "A": 214.4, "Ix": 59700, "Iy": 20000, "ix": 16.7, "iy": 9.65, "Zx": 3390, "Zy": 1510},
    "H-400X400X13X21": {"H": 400, "B": 400, "t1": 13, "t2": 21, "r": 22, "W": 172, "A": 218.7, "Ix": 66600, "Iy": 22400, "ix": 17.5, "iy": 10.1, "Zx": 3670, "Zy": 1700},
    "H-400X408X21X21": {"H": 400, "B": 408, "t1": 21, "t2": 21, "r": 22, "W": 197, "A": 250.7, "Ix": 70900, "Iy": 23800, "ix": 16.8, "iy": 9.75, "Zx": 3990, "Zy": 1790},
    "H-406X403X16X24": {"H": 406, "B": 403, "t1": 16, "t2": 24, "r": 22, "W": 200, "A": 254.9, "Ix": 78000, "Iy": 26200, "ix": 17.5, "iy": 10.1, "Zx": 4280, "Zy": 1980},
    "H-414X405X18X28": {"H": 414, "B": 405, "t1": 18, "t2": 28, "r": 22, "W": 232, "A": 295.4, "Ix": 92800, "Iy": 31000, "ix": 17.7, "iy": 10.2, "Zx": 5030, "Zy": 2330},
    "H-428X407X20X35": {"H": 428, "B": 407, "t1": 20, "t2": 35, "r": 22, "W": 283, "A": 360.7, "Ix": 119000, "Iy": 39400, "ix": 18.2, "iy": 10.4, "Zx": 6310, "Zy": 2940},
    "H-458X417X30X50": {"H": 458, "B": 417, "t1": 30, "t2": 50, "r": 22, "W": 415, "A": 528.6, "Ix": 187000, "Iy": 60500, "ix": 18.8, "iy": 10.7, "Zx": 9540, "Zy": 4440},
    "H-498X432X45X70": {"H": 498, "B": 432, "t1": 45, "t2": 70, "r": 22, "W": 605, "A": 770.1, "Ix": 298000, "Iy": 94000, "ix": 19.7, "iy": 11.1, "Zx": 14400, "Zy": 6720}
}

# H형강 이음 스플라이스 무게(N), 볼트 개수
HPlateConnectionData = {    
    'H-150X150X7X10': {'total_weight': 19.13, 'bolt_count': 20},
    'H-200X200X8X12': {'total_weight': 269.09, 'bolt_count': 32},
    'H-300X150X6.5X9': {'total_weight': 159.31, 'bolt_count': 24},
    'H-350X175X7X11': {'total_weight': 245.35, 'bolt_count': 36},
    'H-390X300X10X16': {'total_weight': 672.18, 'bolt_count': 52},
    'H-396X199X7X11': {'total_weight': 250.94, 'bolt_count': 34},
    'H-400X200X8X13': {'total_weight': 289.65, 'bolt_count': 34},
    'H-404X201X9X15': {'total_weight': 422.91, 'bolt_count': 44},
    'H-440X300X11X18': {'total_weight': 774.01, 'bolt_count': 68},
    'H-446X199X8X12': {'total_weight': 279.68, 'bolt_count': 36},
    'H-450X200X9X14': {'total_weight': 397.50, 'bolt_count': 44},
    'H-482X300X11X15': {'total_weight': 648.83, 'bolt_count': 60},
    'H-488X300X11X18': {'total_weight': 829.73, 'bolt_count': 68},
    'H-496X199X9X14': {'total_weight': 443.12, 'bolt_count': 48},
    'H-500X200X10X16': {'total_weight': 500.51, 'bolt_count': 48},
    'H-582X300X12X17': {'total_weight': 894.67, 'bolt_count': 72},
    'H-588X300X12X20': {'total_weight': 1104.31, 'bolt_count': 80},
    'H-594X302X14X23': {'total_weight': 1416.47, 'bolt_count': 92},
    'H-596X199X10X15': {'total_weight': 516.79, 'bolt_count': 52},
    'H-600X200X11X17': {'total_weight': 624.41, 'bolt_count': 56},
    'H-606X201X12X20': {'total_weight': 803.93, 'bolt_count': 68},
    'H-612X202X13X23': {'total_weight': 894.77, 'bolt_count': 68},
    'H-692X300X13X20': {'total_weight': 1188.68, 'bolt_count': 88},
    'H-700X300X13X24': {'total_weight': 1480.23, 'bolt_count': 96},
    'H-708X302X15X28': {'total_weight': 1821.74, 'bolt_count': 108},
    'H-792X300X14X22': {'total_weight': 1465.61, 'bolt_count': 100},
    'H-800X300X14X26': {'total_weight': 1797.09, 'bolt_count': 108},
    'H-808X302X16X30': {'total_weight': 2252.48, 'bolt_count': 120},
    'H-890X299X15X23': {'total_weight': 1597.75, 'bolt_count': 108},
    'H-900X300X16X28': {'total_weight': 2304.27, 'bolt_count': 128},
    'H-912X302X18X34': {'total_weight': 3363.56, 'bolt_count': 156},
    'BH-450X350X14X28': {'total_weight': 1476.31, 'bolt_count': 96},
    'BH-450X350X14X35': {'total_weight': 1941.01, 'bolt_count': 88},
    'BH-450X350X30X50': {'total_weight': 4133.15, 'bolt_count': 160},
    'BH-550X300X12X25': {'total_weight': 1214.09, 'bolt_count': 76},
    'BH-550X350X20X50': {'total_weight': 3999.93, 'bolt_count': 158},
    'BH-600X300X14X25': {'total_weight': 1283.44, 'bolt_count': 80},
    'BH-600X300X16X35': {'total_weight': 2340.96, 'bolt_count': 108},
    'BH-600X300X20X45': {'total_weight': 3399.26, 'bolt_count': 120},
    'BH-700X300X13X24': {'total_weight': 1479.23, 'bolt_count': 96},
    'BH-800X300X14X20': {'total_weight': 1222.92, 'bolt_count': 92},
    'BH-800X350X30X60': {'total_weight': 9381.70, 'bolt_count': 230},
    'BH-800X400X14X26': {'total_weight': 1889.92, 'bolt_count': 132},
    'BH-900X300X16X35': {'total_weight': 2675.27, 'bolt_count': 120},
    'BH-900X300X20X45': {'total_weight': 4253.92, 'bolt_count': 152},
    'BH-950X300X14X20': {'total_weight': 1340.34, 'bolt_count': 92},
    'BH-1000X300X16X20': {'total_weight': 1637.68, 'bolt_count': 116},
    'BH-1000X350X20X38': {'total_weight': 3380.04, 'bolt_count': 164},
    'BH-1000X400X20X45': {'total_weight': 5430.72, 'bolt_count': 184},
    'BH-1200X300X20X45': {'total_weight': 4363.88, 'bolt_count': 168}
}

# 베스토 핀이음 스플라이스 무게(N), 볼트 개수
BestoPinConnectionData = {
    'BT-200X300X6': {'total_weight': 87.97, 'bolt_count': 8},
    'BT-250X300X6': {'total_weight': 101.44, 'bolt_count': 8},
    'BT-300X300X6': {'total_weight': 114.98, 'bolt_count': 12},
    'BT-350X300X6': {'total_weight': 97.61, 'bolt_count': 10},
    'BT-350X300X7': {'total_weight': 140.48, 'bolt_count': 12},
    'BT-400X300X6': {'total_weight': 141.85, 'bolt_count': 12},
    'BT-400X300X7': {'total_weight': 155.88, 'bolt_count': 16},
    'BT-400X300X8': {'total_weight': 169.71, 'bolt_count': 16},
    'BT-400X300X9': {'total_weight': 183.25, 'bolt_count': 20},
    'BT-450X300X6': {'total_weight': 155.39, 'bolt_count': 16},
    'BT-450X300X7': {'total_weight': 171.28, 'bolt_count': 16},
    'BT-450X300X8': {'total_weight': 186.98, 'bolt_count': 20},
    'BT-450X300X9': {'total_weight': 202.48, 'bolt_count': 20},
    'BT-500X300X6': {'total_weight': 201.79, 'bolt_count': 20},
    'BT-500X300X7': {'total_weight': 208.95, 'bolt_count': 20},
    'BT-500X300X8': {'total_weight': 204.34, 'bolt_count': 20},
    'BT-500X300X9': {'total_weight': 260.22, 'bolt_count': 24},
    'BT-550X400X6': {'total_weight': 147.35, 'bolt_count': 16},
    'BT-550X400X7': {'total_weight': 213.66, 'bolt_count': 20},
    'BT-550X300X8': {'total_weight': 221.71, 'bolt_count': 20},
    'BT-550X400X9': {'total_weight': 252.51, 'bolt_count': 24},
    'BT-600X400X7': {'total_weight': 229.06, 'bolt_count': 20},
    'BT-600X300X6': {'total_weight': 195.02, 'bolt_count': 20},
    'BT-600X300X7': {'total_weight': 217.49, 'bolt_count': 20},
    'BT-600X400X8': {'total_weight': 250.55, 'bolt_count': 24},
    'BT-600X300X8': {'total_weight': 238.97, 'bolt_count': 24},
    'BT-600X300X9': {'total_weight': 260.22, 'bolt_count': 28},
    'BT-600X400X10': {'total_weight': 290.48, 'bolt_count': 28},
    'BT-600X300X10': {'total_weight': 278.99, 'bolt_count': 28},
    'BT-600X300X12': {'total_weight': 323.34, 'bolt_count': 32},
    'BT-600X300X14': {'total_weight': 367.68, 'bolt_count': 36},
    'BT-600X300X16': {'total_weight': 434.03, 'bolt_count': 36},
    'BT-650X400X7': {'total_weight': 244.47, 'bolt_count': 24},
}

# H형강 핀이음 스플라이스 무게(N), 볼트 개수
HPinConnectionData = {    
    'H-150X75X5X7': {'total_weight': 10.69, 'bolt_count': 2},
    'H-200X100X5.5X8': {'total_weight': 10.99, 'bolt_count': 2},
    'H-200X200X8X12': {'total_weight': 108.11, 'bolt_count': 10},
    'H-250X125X6X9': {'total_weight': 13.34, 'bolt_count': 2},
    'H-300X150X6.5X9': {'total_weight': 18.35, 'bolt_count': 3},
    'H-300X300X10X15': {'total_weight': 40.22, 'bolt_count': 4},
    'H-340X250X9X14': {'total_weight': 34.03, 'bolt_count': 4},
    'H-350X175X7X11': {'total_weight': 20.40, 'bolt_count': 3},
    'H-396X199X7X11': {'total_weight': 37.77, 'bolt_count': 6},
    'H-400X200X8X13': {'total_weight': 30.61, 'bolt_count': 4},
    'H-446X199X8X12': {'total_weight': 33.56, 'bolt_count': 5},
    'H-450X200X9X14': {'total_weight': 37.67, 'bolt_count': 5},
    'H-482X300X11X15': {'total_weight': 78.19, 'bolt_count': 8},
    'H-500X200X10X16': {'total_weight': 49.74, 'bolt_count': 6},
    'H-582X300X12X17': {'total_weight': 16.49, 'bolt_count': 2},
    'H-588X300X12X20': {'total_weight': 98.30, 'bolt_count': 10},
    'H-596X199X10X15': {'total_weight': 51.80, 'bolt_count': 7},
    'H-600X200X11X17': {'total_weight': 65.43, 'bolt_count': 8},
    'H-700X300X13X24': {'total_weight': 63.89, 'bolt_count': 6},
    'BH-450X200X12X20': {'total_weight': 96.64, 'bolt_count': 10},
    'BH-450X300X12X25': {'total_weight': 54.45, 'bolt_count': 5},
    'BH-550X200X12X20': {'total_weight': 147.35, 'bolt_count': 14}
}

structuralSteelYieldStressData = {
    "SM355": {16: 355, 40: 345, 75: 335, 100: 325},
    "SM420": {16: 420, 40: 410, 75: 400, 100: 390},
    "SM460": {16: 460, 40: 450, 75: 430, 100: 420},
    "SN355": {16: 355, 40: 355, 75: 335, 100: 335},
    "SHN355": {16: 355, 40: 355, 75: 355, 100: 355}
}

def StructuralSteelYieldStress(steel, thickness):
    if (thickness <= 16):
        yieldStress = structuralSteelYieldStressData[steel][16]
    elif (thickness <= 40):
        yieldStress = structuralSteelYieldStressData[steel][40]
    elif (thickness <= 75):
        yieldStress = structuralSteelYieldStressData[steel][75]
    elif (thickness <= 100):
        yieldStress = structuralSteelYieldStressData[steel][100]
    return yieldStress

# 철근 단면적 (mm²)
reBarArea = {
    10: 71.33,
    13: 126.7,
    16: 198.6,
    19: 286.5,
    22: 387.1,
    25: 506.7,
    29: 642.4,
    32: 794.2,
    35: 956.6,
    38: 1140
}

# 철근 단위중량 (N/m)
reBarUnitWeight = {
    10: 5.4917,
    13: 9.8056,
    16: 15.292,
    19: 22.065,
    22: 29.822,
    25: 39.012,
    29: 49.682,
    32: 61.099,
    35: 73.627,
    38: 87.168
}

# 엑셀에서 최종 값을 가져오게 만들었지만 향후 필요시 사용하기 위해 남겨둠
liveLoad = {
    "주택": {
        "주거용 건축물의 거실": 2.0,
        "공동주택의 공용실": 5.0
    },
    "병원": {
        "병실": 2.0,
        "수술실, 공용실, 실험실": 3.0,
        "1층 외의 모든 층 복도": 4.0
    },
    "숙박시설": {
        "객실": 2.0,
        "공용실": 5.0
    },
    "사무실": {
        "일반 사무실": 2.5,
        "특수용도 사무실": 5.0,
        "문서보관실": 5.0,
        "1층 외의 모든 층 복도": 4.0
    },
    "학교": {
        "교실": 3.0,
        "일반 실험실": 3.0,
        "중량물 실험실": 5.0,
        "1층 외의 모든 층 복도": 4.0
    },
    "판매장": {
        "상점, 백화점 (1층)": 5.0,
        "상점, 백화점 (2층 이상)": 6.0,
        "창고형 매장": 6.0,
        "모든 층 복도": 5.0
    },
    "집회 및 유흥장": {
        "무대": 5.0,
        "식당": 5.0,
        "주방": 7.0,
        "극장 및 집회장 (고정 좌석)": 4.0,
        "집회장 (이동 좌석)": 5.0,
        "연회장, 무도장": 5.0
    },
    "체육시설": {
        "체육관 바닥, 옥외 경기장": 5.0,
        "스탠드 (고정 좌석)": 5.0,
        "스탠드 (이동 좌석)": 4.0
    },
    "도서관": {
        "열람실": 3.0,
        "서고": 6.0,
        "1층 외의 모든 층 복도": 4.0
    },
    "주차장 및 옥외 차도": {
        "총중량 30kN 이하의 차량 (옥내)": 3.0,
        "총중량 30kN 이하의 차량 (옥외)": 5.0,
        "총중량 30kN 초과 90kN 이하의 차량": 6.0,
        "총중량 90kN 초과 180kN 이하의 차량": 12.0,
        "옥외 차도와 차도 양쪽의 보도": 12.0
    },
    "창고": {
        "경량품 저장창고": 6.0,
        "중량품 저장창고": 12.0
    },
    "공장": {
        "경공업 공장": 6.0,
        "중공업 공장": 12.0
    },
    "지붕": {
        "점유, 사용하지 않는 지붕(지붕활하중)": 1.0,
        "산책로 용도": 3.0,
        "정원 또는 집회 용도": 5.0,
        "출입이 제한된 조경 구역": 1.0,
        "헬리콥터 이착륙장": 5.0
    },
    "기계실": {
        "공조실, 전기실, 기계실 등": 5.0
    },
    "광장": {
        "옥외광장": 12.0
    },
    "발코니": {
        "출입 바닥 활하중의 1.5배 (최대 5.0kN/m2)": 1.0
    },
    "로비 및 복도": {
        "로비, 1층 복도": 5.0,
        "1층 외의 모든 층 복도": "출입 바닥 활하중"
    },
    "계단": {
        "단독주택 또는 2세대 거주 주택": 2.0,
        "기타의 계단": 5.0
    }
}


# 단일직사각형단면
class SquareSection:
    
    # 가로, 세로, 중심 좌표(x,y), 가장자리 좌표
    def __init__(self, *, height, width, x, y) -> None:        
        self.height = height
        self.width = width
        self.centerX = x
        self.centerY = y
        self.topCoordinate = self.centerY + self.height / 2
        self.bottomCoordinate = self.centerY - self.height / 2
        self.rightCoordinate = self.centerX + self.width / 2
        self.leftCoordinate = self.centerX - self.width / 2
        self.area = self.height * self.width
        self.inertiaX = self.width * self.height ** 3 / 12
        self.inertiaY = self.height * self.width ** 3 / 12
        self.sectionModulusX = self.inertiaX / (self.height / 2) if self.height != 0 else None
        self.sectionModulusY = self.inertiaY / (self.width / 2) if self.width != 0 else None


# 조합단면
class CombinedSection:
    
    def __init__(self,*squares) -> None:
        self.area = sum(square.area for square in squares)
        self.momentAtAxisX = sum(square.area * square.centerY for square in squares)
        self.momentAtAxisY = sum(square.area * square.centerX for square in squares)
        self.centerX = self.momentAtAxisY / self.area
        self.centerY = self.momentAtAxisX / self.area
        self.inertiaX = sum(square.inertiaX + square.area * (square.centerY - self.centerY) ** 2
                            for square in squares)
        self.inertiaY = sum(square.inertiaY + square.area * (square.centerX - self.centerX) ** 2
                            for square in squares)        
        
        squareTopCoordinates = [square.topCoordinate for square in squares]
        squareBottomCoordinates = [square.bottomCoordinate for square in squares]
        squareRightCoordinates = [square.rightCoordinate for square in squares]
        squareLeftCoordinates = [square.leftCoordinate for square in squares]
        self.topCoordinate = max(squareTopCoordinates)
        self.bottomCoordinate = min(squareBottomCoordinates)
        self.rightCoordinate = max(squareRightCoordinates)
        self.leftCoordinate = min(squareLeftCoordinates)
        
        self.height = self.topCoordinate - self.bottomCoordinate
        self.width = self.rightCoordinate - self.leftCoordinate        
        
        self.sectionModulusX1 = self.inertiaX / (self.topCoordinate - self.centerY)
        self.sectionModulusX2 = self.inertiaX / (self.centerY - self.bottomCoordinate)        
        self.sectionModulusY1 = self.inertiaY / (self.rightCoordinate - self.centerX)
        self.sectionModulusY2 = self.inertiaY / (self.centerX - self.leftCoordinate)
                
        self.radiusGyrationY = (self.inertiaY / self.area)**(1/2)
        self.torsionalConstant = sum(square.width * square.height ** 3 / 3 for square in squares)
        
        # 소성중립축
        self.plasticNeutralAxis = self.height / 2
        # NOTE:
        # - 기존 구현은 round(self.area/2) == round(bottomArea) 조건으로 종료하여,
        #   수치 오차로 bottomArea가 x.50000000006 처럼 0.5 경계를 넘어가면 영원히 종료되지 않을 수 있음.
        # - 허용오차(tolerance) 기반으로 안전하게 종료한다.
        bottomArea = 0
        targetArea = self.area / 2
        tolerance = 0.1
        max_iter = 10000

        topSections = []
        bottomSections = []
        dividedSections = []

        for _ in range(max_iter):
            topSections = [square for square in squares if square.bottomCoordinate >= self.plasticNeutralAxis]
            bottomSections = [square for square in squares if square.topCoordinate <= self.plasticNeutralAxis]
            dividedSections = [
                square
                for square in squares
                if square.bottomCoordinate < self.plasticNeutralAxis and square.topCoordinate > self.plasticNeutralAxis
            ]

            bottomArea = sum(square.area for square in bottomSections) + sum(
                (self.plasticNeutralAxis - square.bottomCoordinate) * square.width for square in dividedSections
            )

            # 종료 조건: 면적이 절반에 충분히 근접하면 종료
            if abs(targetArea - bottomArea) <= tolerance:
                break

            denom = sum(square.width for square in dividedSections)
            if denom == 0:
                # 분할되는 단면이 없으면 더 이상 PNA 갱신 불가 → 현재값 유지 후 종료
                break

            self.plasticNeutralAxis = (
                targetArea
                - sum(square.area for square in bottomSections)
                + sum(square.bottomCoordinate * square.width for square in dividedSections)
            ) / denom

            if (self.plasticNeutralAxis >= self.topCoordinate):
                self.plasticNeutralAxis = self.topCoordinate - 1
            if (self.plasticNeutralAxis <= self.bottomCoordinate):
                self.plasticNeutralAxis = self.bottomCoordinate + 1
            
        
        # 소성단면계수
        self.plasticSectionCoefficient = sum(square.area * (square.centerY - self.plasticNeutralAxis) for square in topSections) \
                                       + sum((square.width * (square.topCoordinate - self.plasticNeutralAxis) * (square.topCoordinate - self.plasticNeutralAxis) / 2) for square in dividedSections) \
                                       + sum(square.area * (self.plasticNeutralAxis - square.centerY) for square in bottomSections) \
                                       + sum((square.width * (self.plasticNeutralAxis - square.bottomCoordinate) * (self.plasticNeutralAxis - square.bottomCoordinate) / 2) for square in dividedSections)
        

# 판폭두께비 KDS 14 31 10 표 4.3-2
class WidthThicknessRatio:
    coeff_lambda_p = [0, 0.38, 0.38, 0.54, 0.38, 0.84, 3.76, 0, 1.12, 1.12, 2.42, 0.07]
    coeff_lambda_r = [0, 1.0, 0.95, 0.91, 1.0, 1.52, 5.70, 5.70, 1.40, 1.40, 5.70, 0.31]
    
    def __init__ (self, width, thickness, elasticModulus, yieldStress, typeNumber) -> None:
        
        self.lambda_p = self.coeff_lambda_p[typeNumber] * (elasticModulus/yieldStress)**(1/2)
        self.lambda_r = self.coeff_lambda_r[typeNumber] * (elasticModulus/yieldStress)**(1/2)
        self.wtRatio = width / thickness
        
    def check(self):
        if (self.wtRatio <= self.lambda_p):
            return 'Compact'
        elif (self.wtRatio <= self.lambda_r):
            return 'NonCompact'
        else:
            return 'Slender'


# 부재력 계산
class BeamForceCalculator:
    def __init__(self, length: float) -> None:
        """
        초기화: 보의 길이를 설정합니다.
        
        Args:
        length (float): 보의 길이 (단위: m)
        """
        self.length = length

    def calculate_forces(self, load_type: str, support_type: str, position: float, **kwargs) -> dict:
        """
        하중 유형, 지지 조건, 특정 위치에서의 모멘트 및 전단력을 계산합니다.
        
        Args:
        load_type (str): 하중 유형. "Uniform" 또는 "Point" 중 하나.
        support_type (str): 지지 조건. "FixedEnd", "SimpleBeam", "FixPin", "FixFree" 중 하나.
        position (float): 부재력 계산을 위한 위치 (0 <= position <= length).
        kwargs:
            - lineLoad (float): 등분포 하중 크기 (kN/m) (load_type이 "Uniform"일 때 필요)
            - pointLoad (float): 집중하중 크기 (kN) (load_type이 "Point"일 때 필요)
            - pointLocation (float): 집중하중 위치 (m) (load_type이 "Point"일 때 필요)
        
        Returns:
        dict: 계산된 모멘트와 전단력 (kN, kN·m 단위)
        """
        l = self.length
        
        # 위치 검증
        if position < 0 or position > l:
            raise ValueError("position 값은 0과 보의 길이 사이여야 합니다.")
        
        if load_type == "Uniform":
            # 등분포 하중 처리
            w = kwargs.get("lineLoad")
            if w is None:
                raise ValueError("lineLoad는 Uniform 하중 유형에서 필수입니다.")
            
            if support_type == "SimpleBeam":
                shearForce = w * (l / 2 - position)
                moment = -w * position / 2 * (l - position)
            elif support_type == "FixedEnd":
                shearForce = w * (l / 2 - position)
                moment = -w * position / 2 * (l - position) + (w * l**2 / 12)            
            elif support_type == "Pin-Fix":
                shearForce = (3/8) * w * l - w * position
                moment = ((3/8) * w * l) * position - (1/2) * w * position**2
            elif support_type == "Free-Fix":
                shearForce = w * position
                moment = w / 2 * position**2
            else:
                raise ValueError(f"지원하지 않는 지지 조건입니다: {support_type}")
        
        elif load_type == "Point":
            # 집중하중 처리
            p = kwargs.get("pointLoad")
            a = kwargs.get("pointLocation")
            if p is None or a is None:
                raise ValueError("pointLoad와 pointLocation은 Point 하중 유형에서 필수입니다.")
            b = l - a
            if support_type == "SimpleBeam":                
                if position <= a:
                    shearForce = b / l * p
                    moment = b / l * p * position
                else:
                    shearForce = - a / l * p
                    moment = p * a / l * (l - position)
            if support_type == "FixedEnd":                
                if position <= a:
                    shearForce = p * b**2 / l**3 * (3 * a + b)
                    moment = - p * a * b**2 / l**2 + shearForce * position
                else:
                    shearForce = - p *a**2 / l **3 * (a * 3 * b)
                    moment = 2 * p * a**2 * b**2 / l**3 +shearForce * position
            if support_type == "Pin-Fix":                
                if position <= a:
                    shearForce = p * b**2 / (2 * l**3) * (3*a + 2*b)
                    moment = shearForce * position
                else:
                    shearForce = -(p - (p * b**2 / (2 * l**3) * (3*a + 2*b)))
                    moment = p * a * b**2 / (2 * l**3) * (3*a + 2*b) + shearForce * position
            elif support_type == "Free-Fix":
                if position <= a:
                    shearForce = 0
                    moment = 0
                else:
                    shearForce = p
                    moment = p * position
            else:
                raise ValueError(f"지원하지 않는 지지 조건입니다: {support_type}")
        
        else:
            raise ValueError("지원하지 않는 하중 유형입니다. ('Uniform' 또는 'Point' 중 하나를 선택하세요.)")
        
        return {            
            "ShearForce": shearForce,
            "Moment": moment,
        }


# 유효폭 KBC2016 0709.3.1.1
def EffectiveWidth(*, span, bay):          
    b1 = span / 8
    b2 = bay / 2
    # b3 = "보 중심선에서 슬래브 가장자리까지의 거리"       <== 추후 구현
    return min(b1, b2)


def ConcreteElasticModulus(fck):
    delta_f = 4 if fck <= 40 else 6 if fck >= 60 else (fck - 40) / 10
    Ec = 8500 * (fck + delta_f) ** (1/3)
    return Ec


# 스터드 전단연결재 KDS 41 30 20 (4.1.8.2) 합성보의 강재앵커
def StudAnchorStrength(studAnchorArea, f_ck, concreteElasticModulus, studAnchorStrength):
    unitStrength = min(0.5 * studAnchorArea * (f_ck * concreteElasticModulus)**(1/2), 
                       1.0 * 0.75 * studAnchorArea * studAnchorStrength)
    return unitStrength


# 앵글 전단연결재
def AngleAnchorStrength(height, U_width, f_ck):
    unitStrength = 31000 * height**(3/4) * f_ck**(2/3) / U_width**(1/2)  # 실험결과 반영
    return unitStrength


# 합성단면 정모멘트 강도 KDS 41 30 20 (4.1.3.2) ①정모멘트에 대한 휨강도
def CompositeSectionMomentStrength_positive (**properties):
    C1 = properties["P_y"] + properties["P_rb"]           # 강재+철근의 인장강도
    C2 = 0.85 * properties["f_ck"] * properties["A_s"]    # 콘크리트 슬래브 압축강도
    C3 = properties["Q_n"]                                  # 전단연결재 강도
    C = min(C1, C2, C3)                                       # 콘크리트 슬래브의 압축력 산정
    a = C / (0.85 * properties["f_ck"] * properties["b_eff"])       # 압축블럭의 깊이
    # [KDS 41 30 20 해그림 4.1-7] 정모멘트 산정용 소성응력분포
    d1 = properties["d_s"] - a/2
    d2 = 0
    dw = 0
    if (C1 > C):
        compressiveAreaInS = (C1 - C) / 2 / properties["F_y"]
        flangesArea = sum(flange.area for flange in properties["compressiveFlanges"])
        flangesWidth = sum(flange.width for flange in properties["compressiveFlanges"])
        flangesThickness = sum(flange.height for flange in properties["compressiveFlanges"]) / len(properties["compressiveFlanges"])
        websArea = sum(web.area for web in properties["webs"])
        websWidth = sum(web.width for web in properties.get("webs",[]))
        if (compressiveAreaInS < flangesArea):
            d2 = compressiveAreaInS / flangesWidth / 2
        elif (compressiveAreaInS < (flangesArea + websArea)):
            dw = (compressiveAreaInS - flangesArea) / websWidth
            d2 = (flangesArea * flangesThickness / 2 + (compressiveAreaInS - flangesArea) * (dw / 2)) / compressiveAreaInS  # U형 단면에서만 유효한 계산!! (web의 높이가 flange 상단까지 측정됨)
        else:
            print('합성단면 소성중립축 오류!')
    d3 = properties["steelSection"].height - properties["steelSection"].centerY
    if all(ratio == 'Compact' for ratio in properties["widthThicknessRatio"]):
        # KDS 41 30 20 (해식 4.1.3-7)
        M_n_Composite = C * (d1 + d2) + properties["P_y"] * (d3 - d2) + properties["tensionRebarStrength"] * (properties["steelSection"].height - d2 - 33)
    else:
        print('항복모멘트강도로 계산필요. 계산된 값은 소성모멘트임!!')
        M_n_Composite = C * (d1 + d2) + properties["P_y"] * (d3 - d2) + properties["tensionRebarStrength"] * (properties["steelSection"].height - d2 - 33)          # <== 추후 수정 필요!!
    return M_n_Composite


# 합성단면 부모멘트 강도 KDS 41 30 20 (4.1.3.2) ②부모멘트에 대한 휨강도
def CompositeSectionMomentStrength_Negative (**properties):
    T1 = properties['topRebarStrength']
    T2 = properties['Qn']
    T3 = properties['Pyc']
    T = min(T1, T2)
    # [KDS 41 30 20 해그림 4.1-8] 부모멘트 산정용 소성응력분포
    d1 = properties['ds'] - properties['slabCoverConcreteDepth']
    d2 = 0
    if (T < T3):
        tenstionAreaInS = (T3 - T) / 2 / properties['Fy']
        flangesArea = sum(flange.area for flange in properties.get('tensileFlanges',[]))
        flangesThickness = sum(flange.height for flange in properties.get('tensileFlanges',[])) / len(properties['tensileFlanges'])
        websArea = sum(web.area for web in properties.get("webs",[]))
        websWidth = sum(web.width for web in properties.get("webs",[]))
        if (tenstionAreaInS < flangesArea):
            d2 = tenstionAreaInS / sum(flange.width for flange in properties.get('tensileFlanges',[])) /2
        elif (tenstionAreaInS < (flangesArea + websArea)):
            dw = (tenstionAreaInS - flangesArea) / websWidth
            d2 = (flangesArea * flangesThickness / 2 + (tenstionAreaInS - flangesArea) * (dw / 2 + flangesThickness)) / tenstionAreaInS
        else:
            print('합성단면 소성중립축 오류!')
    d3 = properties["steelSection"].height - properties["steelSection"].centerY
    if all(ratio == 'Compact' for ratio in properties["widthThicknessRatio"]):
        # KDS 41 30 20 (해식 4.1.3-9)
        nominalMomentStrength_Negative = T * (d1 + d2) + properties["Pyc"] * (d3 - d2)
    else:
        print('항복모멘트강도로 계산필요. 계산된 값은 소성모멘트임!!')
        nominalMomentStrength_Negative = T * (d1 + d2) + properties["Pyc"] * (d3 - d2)          # <== 추후 수정 필요!!
    return nominalMomentStrength_Negative


# 강도검토
def StrengthCheck (designStrength, requiredStrength):
    if (designStrength >= requiredStrength):        
        return True
    else:        
        return False


# [KDS 14 31 10] 4.3.2.1.1.1 설계휨강도
def DesignMomentStrength (nominalStrength):
    Cb = 1 # 횡좌굴모멘트수정계수 (추후 구현 필요!!)
    designStrength = 0.9 * Cb * nominalStrength
    return designStrength
        

# [KDS 14 31 10] 4.3.2.1.1.2 강축 휨을 받는 2축대칭 H형강 또는 ㄷ형강 조밀단면 부재
class NominalMomentStrength_2:
    
    def __init__(self, section, Steel_elasticModulus, Steel_yieldStress, unbracedLength) -> None:
        self.elasticMomentStrength = section.sectionModulusX1 * Steel_yieldStress
        print(section.sectionModulusX1, Steel_yieldStress)
        self.plasticMomentStrength = Steel_yieldStress * section.plasticSectionCoefficient
        self.unbracedLength = unbracedLength
        self.plasticUnbracedLength = 1.76 * section.radiusGyrationY * (Steel_elasticModulus / Steel_yieldStress) ** (1/2)
        C_w = section.height ** 2 * section.inertiaY / 4 # H형강 뒤틀림상수 (몇 가지 버전이 있음, 표로 제공된 값을 사용하는 것이 마음 편함)
        r_ts = ( (section.inertiaY * C_w) ** (1/2)  / section.sectionModulusX1 ) ** (1/2)
        self.elasticUnbracedLength = 1.95 * r_ts * (Steel_elasticModulus / (0.7 * Steel_yieldStress)) * (section.torsionalConstant / (section.sectionModulusX1 * section.height)) **(1/2) *(1+(1+6.76*((0.7*Steel_yieldStress/Steel_elasticModulus)*(section.sectionModulusX1*section.height/section.torsionalConstant))**2)**(1/2)) **(1/2)
        if (self.unbracedLength <= self.plasticUnbracedLength):
            self.lateralBucklingStrength = self.plasticMomentStrength
        elif (self.unbracedLength <= self.elasticUnbracedLength):
            self.lateralBucklingStrength = self.plasticMomentStrength - (self.plasticMomentStrength - 0.7 * Steel_yieldStress * section.sectionModulusX1) * ((self.unbracedLength - self.plasticUnbracedLength) / (self.elasticUnbracedLength - self.plasticUnbracedLength))
        else:
            self.lateralBucklingStrength = self.plasticMomentStrength # 수정 필요!!
        self.nominalMomentStrength_Positive = min(self.plasticMomentStrength, self.lateralBucklingStrength)
        self.nominalMomentStrength_Negative = min(self.plasticMomentStrength, self.lateralBucklingStrength)
        

# [KDS 14 31 10] 4.3.2.1.1.6 약축 휨을 받는 H형강 또는 ㄷ형강 부재
class NominalMomentStrength_6:
    
    def __init__(self, section, flange, Steel_elasticModulus, Steel_yieldStress, direction, typeNumber) -> None:
        sectionModulus = section.sectionModulusX2 if direction == "P" else section.sectionModulusX1
        self.plasticMomentStrength = Steel_yieldStress * section.plasticSectionCoefficient    
        self.elasticMomentStrength = Steel_yieldStress * sectionModulus
        self.yieldMomentStrength = self.plasticMomentStrength if self.plasticMomentStrength <= 1.6 * self.elasticMomentStrength else self.elasticMomentStrength
        self.flange_WTRatio = WidthThicknessRatio(width=flange.width, thickness=flange.height, elasticModulus=Steel_elasticModulus, yieldStress=Steel_yieldStress, typeNumber=typeNumber)
        if (self.flange_WTRatio.check() == 'Compact'):
            self.localBucklingStrength = self.plasticMomentStrength if self.plasticMomentStrength <= 1.6 * self.elasticMomentStrength else self.elasticMomentStrength
        elif (self.flange_WTRatio.check() == 'NonCompact'):
            self.localBucklingStrength = (self.plasticMomentStrength - (self.plasticMomentStrength - 0.7 * Steel_yieldStress * sectionModulus) * (self.flange_WTRatio.wtRatio - self.flange_WTRatio.lambda_p) / (self.flange_WTRatio.lambda_r - self.flange_WTRatio.lambda_p))
        else:
            self.localBucklingStrength = (0.69 * Steel_elasticModulus) / ((flange.width / (2*flange.height))**2) * sectionModulus
        self.nominalMomentStrength = min(self.yieldMomentStrength, self.localBucklingStrength)


# [KDS 14 31 10] 4.3.2.1.2.1 (2) 설계전단강도
def DesignShearStrength (nominalStrength):
    phi = 0.9
    designStrength = phi * nominalStrength
    return designStrength


# [KDS 14 31 10] 4.3.2.1.2.2 비보강 또는 보강 웨브를 가진 부재
class NominalShearStrength:
    
    def __init__(self, square, shearArea, yieldStress, elasticModulus) -> None:
        self.slendernessRatio = square.height / square.width
        k_v = 5     # 필요하면 세부적인 계산식 구현 해야 함
        shearRatio = (k_v * elasticModulus / yieldStress) ** (1/2)
        self.yieldLimit = 1.1 * shearRatio
        self.bucklingLimit = 1.37 * shearRatio
        if (self.slendernessRatio <= self.yieldLimit):
            self.shearCoefficient = 1.0
        elif (self.slendernessRatio <= self.bucklingLimit):
            self.shearCoefficient = 1.1 * shearRatio / self.slendernessRatio
        else:
            self.shearCoefficient = 1.51 * shearRatio**2 / self.slendernessRatio**2    
        self.shearStrength = 0.6 * yieldStress * shearArea
        self.nominalShearStrength = self.shearStrength * self.shearCoefficient


# 사용성 검토
def ServiceabilityCheck (capacity, demand):
    if (capacity <= demand):        
        return True
    else:        
        return False


# 처짐
def Deflection (endCondition, load, length, elasticModulus, inertia):
    deflection = 0
    error_message = None
    
    if (endCondition == 'Fix-Fix'):   # 양단고정 wl^4/384EI
        endConditionCoefficient = 1
    elif (endCondition == 'Pin-Pin'):   # 단순보 5wl^4/384EI
        endConditionCoefficient = 5
    elif (endCondition == 'Fix-Pin'):   # 고정+힌지 wl^4/185EI
        endConditionCoefficient = 384/185
    elif (endCondition == 'Fix-Free'):  # 캔틸레버 wl^4/8EI
        endConditionCoefficient = 384/8
    else:
        error_message = "endCondition을 바르게 입력해 주세요!!"
        return 0, error_message
    
    deflection = endConditionCoefficient * (load * length**4) / (384 * elasticModulus * inertia)
    return deflection, error_message


# 합성단면 유효단면2차모멘트
def EffectiveInertia (steelSectionInertia, compositeRatio, compositeSectionInertia):
    I_equiv = steelSectionInertia + (compositeRatio)**(1/2) * (compositeSectionInertia-steelSectionInertia)    # 불완전합성보 유효단면2차모멘트 / 완전합성일 경우 I_com과 같음
    I_eff = 0.75 * I_equiv
    return I_eff


# 진동검토 [강구조설계 7.8.2]
class Vibration:
    P_o = {'사무실': 0.29, '쇼핑몰': 0.29, '육교(실내)': 0.41, '육교(실외)': 0.41}  #상수력
    beta = {'사무실': 0.03, '쇼핑몰': 0.02, '육교(실내)': 0.01, '육교(실외)': 0.01} #감쇠력
    accRatioLimit = {'사무실': 0.005, '쇼핑몰': 0.015, '육교(실내)': 0.015, '육교(실외)': 0.05}  #가속도 한계비
    g = 9.81    # 중력가속도 [m/sec^2]
    
    def __init__(self, useage, deflection_L, weight) -> None:
        self.naturalFrequency = 0.18 * (self.g*1000 / deflection_L)**(1/2)
        self.maxAccelerationRatio = self.P_o[useage] * math.exp(-0.35*self.naturalFrequency) / (self.beta[useage] * weight)


# 철근 최소순간격
def MinimumRebarSpacingCheck (beamwidth, rebarDiameter, rebarQuantity):
    rebarSpacing = (beamwidth - (10 * 2) - (40 * 2) - rebarDiameter * rebarQuantity) / max(rebarQuantity - 1, 1)
    if (rebarSpacing >= max(25, rebarDiameter, 33)): #25mm, 철근지름, 굵은골재(25mm)의 4/3
        return True
    else:
        return False


# 상부플랜지 시공하중 검토
def TopFlangeConstructionLoadCheck (thickness, constructionLoad, steelYieldStress):
    inertia_X = 1000 * thickness**3 / 12
    sectionModulus = inertia_X / (thickness / 2)
    nominalMomentStrength = steelYieldStress * sectionModulus
    designMomentStrength = DesignMomentStrength(nominalMomentStrength)
    requiredMomentStrength = constructionLoad * 40
    if designMomentStrength <requiredMomentStrength:
        return False
    else:
        return True

# 물량계산
class CostCalculation:
    def __init__(
        self,
        section1_length: float,
        section2_length: float,
        unitWeight_Section1: float = 0,
        unitWeight_Section2: float = 0,
        angleShearConnector_spacing: float = 0,
        studShearConnector_spacing: float = 0,
        topRebarDiameter: float | int = 0,
        topRebarQuantity: float = 0,
        bottomRebarDiameter: float | int = 0,
        bottomRebarQuantity: float = 0,
        H_Section_List: str | None = None,
        volumn_concInU: float = 0,
        overlappedLength: float = 0
    ):
        
        # 전체 보 길이 계산
        beamLength = section1_length + section2_length
        
        # 무게 계산
        self.weight_Section1 = unitWeight_Section1 * section1_length *1.07
        self.weight_Section2 = unitWeight_Section2 * (section2_length + 2 * overlappedLength) *1.07
        # 단면1 길이가 0이면 단면2 길이를 사용
        effective_length = section1_length if section1_length > 0 else section2_length
        self.angle_weight = (4.43 * 9.8) * (0.3) * effective_length / angleShearConnector_spacing *1.07 if angleShearConnector_spacing != 0 else 0
        self.stud_number = math.ceil(effective_length / studShearConnector_spacing) * 2 if studShearConnector_spacing != 0 else 0
        # H형강의 플랜지 너비(두 번째 값)에 따라 곱셈 계수 결정
        if H_Section_List and H_Section_List != 'none' and H_Section_List != 'Built Up':
            # H형강 명칭에서 플랜지 너비(두 번째 값) 추출
            try:
                flange_width = int(H_Section_List.split('X')[1])
                multiplier = 1 if flange_width <= 200 else 2
            except (IndexError, ValueError):
                multiplier = 2  # 파싱 실패시 기본값 2
        else:
            multiplier = 2  # H_Section_List가 없거나 'none', 'Built Up'인 경우 기본값 2
            
        self.section2_stud_Number = math.ceil(section2_length / 200) * multiplier if section2_length != 0 else 0
        self.topRebar_weight = 0
        self.bottomRebar_weight = 0
        
        if (
            H_Section_List
            and isinstance(H_Section_List, str)
            and H_Section_List.lower() != 'none'
            and H_Section_List in HPlateConnectionData
        ):
            self.bestoGirderSplice_weight = HPlateConnectionData[H_Section_List]['total_weight'] * 2
        else:
            self.bestoGirderSplice_weight = 0
            
        if topRebarDiameter and topRebarQuantity:
            self.topRebar_weight = reBarUnitWeight[int(topRebarDiameter)] * topRebarQuantity * beamLength * 0.6 / 1000 *1.07
        if bottomRebarDiameter and bottomRebarQuantity:
            self.bottomRebar_weight = reBarUnitWeight[int(bottomRebarDiameter)] * bottomRebarQuantity * beamLength * 0.6 / 1000 *1.07
        
        # 비용 계산
        self.Section1_cost = self.weight_Section1/9800 * 1150000 #톤당 115만원
        self.Section2_cost = self.weight_Section2/9800 * 1200000 #톤당 120만원
        self.angle_cost = self.angle_weight/9800 * 1100000 #톤당 110만원
        self.stud_cost = (self.stud_number + self.section2_stud_Number) * 650 #개당 650원
        self.topRebar_cost = self.topRebar_weight/9800 * 1100000 #톤당 110만원
        self.bottomRebar_cost = self.bottomRebar_weight/9800 * 1100000 #톤당 110만원
        self.bestoGirderSplice_cost = self.bestoGirderSplice_weight/9800 * 1150000 #톤당 115만원

        self.steel_cost = self.Section1_cost + self.Section2_cost + self.angle_cost + self.stud_cost + self.topRebar_cost + self.bottomRebar_cost + self.bestoGirderSplice_cost
        self.conc_cost = volumn_concInU / 10**9 * 100000 #m^3당 10만원
        self.totalCost = self.steel_cost + self.conc_cost