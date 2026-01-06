"""
BESTO Design Library
구조 설계를 위한 계산 함수 및 클래스 모음
"""
import math

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

# 강재 항복강도 데이터
structuralSteelYieldStressData = {
    "SM355": {16: 355, 40: 345, 75: 335, 100: 325},
    "SM420": {16: 420, 40: 410, 75: 400, 100: 390},
    "SM460": {16: 460, 40: 450, 75: 430, 100: 420},
    "SN355": {16: 355, 40: 355, 75: 335, 100: 335},
    "SHN355": {16: 355, 40: 355, 75: 355, 100: 355}
}


def StructuralSteelYieldStress(steel, thickness):
    """강재 항복강도 계산"""
    if thickness <= 16:
        yieldStress = structuralSteelYieldStressData[steel][16]
    elif thickness <= 40:
        yieldStress = structuralSteelYieldStressData[steel][40]
    elif thickness <= 75:
        yieldStress = structuralSteelYieldStressData[steel][75]
    elif thickness <= 100:
        yieldStress = structuralSteelYieldStressData[steel][100]
    return yieldStress


# 단일직사각형단면
class SquareSection:
    """단일 직사각형 단면 클래스"""
    
    def __init__(self, *, height, width, x, y):
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
    """조합 단면 클래스"""
    
    def __init__(self, *squares):
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
        
        # 소성중립축 계산
        self.plasticNeutralAxis = self.height / 2
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

            if abs(targetArea - bottomArea) <= tolerance:
                break

            denom = sum(square.width for square in dividedSections)
            if denom == 0:
                break

            self.plasticNeutralAxis = (
                targetArea
                - sum(square.area for square in bottomSections)
                + sum(square.bottomCoordinate * square.width for square in dividedSections)
            ) / denom

            if self.plasticNeutralAxis >= self.topCoordinate:
                self.plasticNeutralAxis = self.topCoordinate - 1
            if self.plasticNeutralAxis <= self.bottomCoordinate:
                self.plasticNeutralAxis = self.bottomCoordinate + 1
        
        # 소성단면계수
        self.plasticSectionCoefficient = (
            sum(square.area * (square.centerY - self.plasticNeutralAxis) for square in topSections)
            + sum((square.width * (square.topCoordinate - self.plasticNeutralAxis) ** 2 / 2) for square in dividedSections)
            + sum(square.area * (self.plasticNeutralAxis - square.centerY) for square in bottomSections)
            + sum((square.width * (self.plasticNeutralAxis - square.bottomCoordinate) ** 2 / 2) for square in dividedSections)
        )


def ConcreteElasticModulus(fck):
    """콘크리트 탄성계수 계산"""
    delta_f = 4 if fck <= 40 else 6 if fck >= 60 else (fck - 40) / 10
    Ec = 8500 * (fck + delta_f) ** (1/3)
    return Ec


def EffectiveWidth(*, span, bay):
    """유효폭 계산 KBC2016 0709.3.1.1"""
    b1 = span / 8
    b2 = bay / 2
    return min(b1, b2)


def Deflection(endCondition, load, length, elasticModulus, inertia):
    """처짐 계산"""
    deflection = 0
    error_message = None
    
    if endCondition == 'Fix-Fix':
        endConditionCoefficient = 1
    elif endCondition == 'Pin-Pin':
        endConditionCoefficient = 5
    elif endCondition == 'Fix-Pin':
        endConditionCoefficient = 384/185
    elif endCondition == 'Fix-Free':
        endConditionCoefficient = 384/8
    else:
        error_message = "endCondition을 바르게 입력해 주세요!!"
        return 0, error_message
    
    deflection = endConditionCoefficient * (load * length**4) / (384 * elasticModulus * inertia)
    return deflection, error_message


# 진동검토
class Vibration:
    """진동 검토 클래스 [강구조설계 7.8.2]"""
    P_o = {'사무실': 0.29, '쇼핑몰': 0.29, '육교(실내)': 0.41, '육교(실외)': 0.41}
    beta = {'사무실': 0.03, '쇼핑몰': 0.02, '육교(실내)': 0.01, '육교(실외)': 0.01}
    accRatioLimit = {'사무실': 0.005, '쇼핑몰': 0.015, '육교(실내)': 0.015, '육교(실외)': 0.05}
    g = 9.81
    
    def __init__(self, useage, deflection_L, weight):
        self.naturalFrequency = 0.18 * (self.g*1000 / deflection_L)**(1/2)
        self.maxAccelerationRatio = self.P_o[useage] * math.exp(-0.35*self.naturalFrequency) / (self.beta[useage] * weight)


# React에서 호출할 함수
def get_h_beam_data(section_name):
    """H형강 데이터 조회"""
    if section_name in HBeamData:
        return HBeamData[section_name]
    return None


def calculate_section_properties(height, width, thickness):
    """단면 특성 계산 (간단한 예시)"""
    area = height * width - (height - 2*thickness) * (width - 2*thickness)
    return {
        'area': area,
        'height': height,
        'width': width
    }

