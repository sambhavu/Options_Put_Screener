import yfinance as yf
import pandas as pd
import numpy as np
from math import log, sqrt, exp
from scipy import stats
from matplotlib import pyplot as plt
from yahoo_fin import stock_info as si
import xlsxwriter

def d1_(S, K, t, r, iv):
    return (log(S/K) + ((iv*iv)/2.0 + r)*t)/(iv*sqrt(t))

def BS_call(S, K , t, r, iv):
    S = float(S)
    d1 = d1_(S, K, t, r, iv)
    d2 = d1 - iv*sqrt(t)
    price = S * stats.norm.cdf(d1, 0.0, 1.0) - K * np.exp(-r * t) * stats.norm.cdf(d2, 0.0, 1.0)

    delta = stats.norm.cdf(d1, 0.0, 1.0)
    return price, delta

def BS_put(S, K, t, r, iv):
    S = float(S)
    d1 = d1_(S, K, t, r, iv)
    d2 = d1 - iv*sqrt(t)
    price = K * np.exp(-r*t) * stats.norm.cdf(-d2, 0.0, 1.0) - S * stats.norm.cdf(-d1, 0.0, 1.0)

    delta = stats.norm.cdf(-d1, 0.0, 1.0)
    return price, delta


#constants
r = .026
t = 3.0/252

#Data to be stored and Displayed
tickers = []
current = []
prices = []
strikes = []
deltas = []
return_ = []

stx = ['^RUT', 'SPY', 'NTNX', 'AAPL', 'NVDA', 'BAC',
                 'BX', 'TGT', 'AWK', 'FB', 'AMD', 'BA',
                 'JPM', 'TSLA', 'AMZN', 'BABA','C', 'GE', 'MGM', 'SQ'
                 ,'DIS', 'NKE', 'GE', 'F', 'NFLX', 'MSFT', 'CLDR', 'XOM', 'X',
                 'ROKU', 'ORCL', 'SBUX', 'KO', 'QCOM', 'IBM',
                 'AAPL', 'BAC',	'GPS',	'AAL',	'MSFT',	'AMD',	'WFC',	'TWTR',	'BA',	'PCG',	'SNAP',	'JPM',	'LK',	'TSLA',	'INO',	'AMZN',	'BABA',	'CCL',	'DIS',	'C',	'NKE',	'AZN',	'F',	'GE',	'IDEX',	'T',	'PFE',	'UBER',	'DKNG',	'NVDA',	'SQ',	'MU',	'MGM',	'WKHS',	'NFLX',	'DAL',	'UAL',	'SEAS',	'ZGNX',	'CLDR',	'GS',	'SPCE',	'FSLY',	'XOM',	'X',	'ZM',	'NIO',	'ROKU',	'M',	'CSCO',	'PBR',	'TLRY',	'GNUS',	'WORK',	'PTON',	'NCLH',	'ORCL',	'ET',	'VZ',	'INTC',	'BYND',	'HTZ',	'OXY',	'GM',	'PLUG',	'SPOT',	'WYNN',	'SBUX',	'CRWD',	'KO',	'MRNA',	'NOK',	'WMT',	'V',	'EBAY',	'PYPL',	'RCL',	'SONO',	'GOOGL',	'DOCU',	'QCOM',	'CTL',	'CRM',	'VIAC',	'LUV',	'GILD',	'BIG',	'GOLD',	'BMY',	'CHWY',	'AGNC',	'JD',	'FCX',	'RAD',	'SRNE',	'DB',	'COST',	'BSX',	'VALE',	'PENN',	'MTCH',	'PINS',	'JNJ',	'MS',	'LYFT',	'SHOP',	'MRK',	'BBBY',	'ERI',	'NEM',	'VBIV',	'SPG',	'BP',	'AMC',	'PLAY',	'DVAX',	'CVX',	'CZR',	'GNC',	'CVS',	'SAVE',	'AXP',	'GSX',	'LVS',	'CGC',	'TGT',	'CHK',	'ZS',	'ZNGA',	'EXPE',	'MCD',	'SABR',	'UPWK',	'FDX',	'HD',	'KR',	'IAC',	'MOMO',	'CAKE',	'MRO',	'IQ',	'ABBV',	'ACB',	'MO',	'HAL',	'NVAX',	'LULU',	'MPC',	'SYF',	'DISH',	'PEP',	'SLB',	'NLY',	'SLM',	'IVR',	'COF',	'MA',	'CMCSA',	'RTX',	'WDC',	'APT',	'DRI',	'BCRX',	'KMI',	'ATVI',	'OKTA',	'UFS',	'FLIR',	'TEVA',	'EPD',	'TWLO',	'TME',	'IBM',	'OPK',	'CPRI',	'KHC',	'USB',	'CLX',	'PG',	'MOS',	'AIG',	'AUY',	'ADBE',	'PDCE',	'UNH',	'NVTA',	'ULTA',	'SCHW',	'STNG',	'HBAN',	'SDC',	'BIDU',	'DDOG',	'ALLY',	'MAR',	'CAR',	'AKAM',	'AG',	'LB',	'NTR',	'TECD',	'CAT',	'JWN',	'Z',	'LEVI',	'MRVL',	'DD',	'BOX',	'JBLU',	'HEXO',	'ABT',	'AMAT',	'ETSY',	'NTNX',	'BB',	'KGC',	'AVGO',	'HBI',	'ALT',	'UPS',	'ERIC',	'UAA',	'RIG',	'TTD',	'GME',	'DBX',	'DOW',	'LLY',	'LLNW',	'FCEL',	'HOG',	'LOW',	'W',	'AMRN',	'ZYNE',	'TSN',	'FITB',	'BUD',	'APA',	'BHC',	'EOG',	'WBA',	'COTY',	'DHI',	'WPM',	'LVGO',	'NOV',	'KSS',	'TDOC',	'RDS.A',	'GDS',	'RF',	'CLF',	'DG',	'MFA',	'PDD',	'MDT',	'COUP',	'INSG',	'ATHX',	'DLTR',	'TMUS',	'TWO',	'VLO',	'HST',	'WU',	'CRBP',	'SSNC',	'LRCX',	'PLNT',	'TRIP',	'WW',	'LYV',	'DELL',	'DFS',	'COP',	'STX',	'PRU',	'PAYS',	'MITT',	'TXN',	'CHGG',	'PNC',	'NET',	'CNC',	'RNG',	'HSBC',	'FOXA',	'BIIB',	'MUX',	'BKNG',	'TAL',	'BK',	'WLL',	'KBH',	'FIT',	'VMW',	'FTCH',	'MAC',	'FEYE',	'ODP',	'SIRI',	'CODX',	'TEAM',	'SPLK',	'SFIX',	'TSM',	'ENPH',	'SHAK',	'HPQ',	'CVNA',	'SIX',	'STZ',	'GIS',	'GPRO',	'DUK',	'NE',	'LITE',	'ACN',	'EROS',	'APHA',	'TAP',	'PM',	'BILI',	'MMM',	'CMG',	'CAG',	'SO',	'XLNX',	'NOW',	'SGMO',	'GLW',	'HRTX',	'TBIO',	'OAS',	'SPR',	'CMA',	'NUE',	'OSTK',	'AXSM',	'CLGX',	'DE',	'BE',	'MARK',	'USFD',	'LC',	'EA',	'SWKS',	'CVM',	'CLVS',	'BGG',	'COG',	'CBOE',	'DBD',	'RIOT',	'IGT',	'SYY',	'QURE',	'CXO',	'KSU',	'MET',	'NRZ',	'BBY',	'TJX',	'MYL',	'XSPA',	'TECK',	'DGLY',	'HPE',	'OKE',	'EAT',	'STNE',	'PD',	'AA',	'GLUU',	'XRX',	'VRTX',	'LH',	'ARLP',	'WSC',	'AEO',	'MPLX',	'UA',	'WMB',	'HCA',	'JNPR',	'CL',	'PZZA',	'MT',	'AMGN',	'JMIA',	'HES',	'RRC',	'CNK',	'DHT',	'HLT',	'BHF',	'KEY',	'FISV',	'CME',	'NXPI',	'WDAY',	'MAXR',	'HL',	'HHC',	'CRC',	'HON',	'NOG',	'SPWR',	'MDCA',	'PAAS',	'CIT',	'SWN',	'OVV',	'APPS',	'FSM',	'ALK',	'SM',	'BGS',	'BPY',	'MVIS',	'WING',	'NAT',	'FANG',	'LMT',	'HTHT',	'AMT',	'MDB',	'PLCE',	'EGO',	'CHMA',	'DVN',	'GNW',	'XPER',	'AR',	'EVRI',	'ERJ',	'LEN',	'EURN',	'ADSK',	'TTWO',	'IRBT',	'IP',	'NAK',	'DPZ',	'BCLI',	'NEE',	'FRO',	'FL',	'DDD',	'LNG',	'BLMN',	'CGNX',	'ZTS',	'GDDY',	'ATH',	'ANF',	'WGO',	'CPE',	'MKC',	'FLXN',	'YETI',	'VSTM',	'CIEN',	'SFM',	'STAA',	'BILL',	'SEDG',	'MCRB',	'TOL',	'PGR',	'PSX',	'BG',	'GRUB',	'SKT',	'CLR',	'ALXN',	'CFG',	'NGD',	'PRGS',	'MDLZ',	'DENN',	'DOOR',	'KL',	'NTAP',	'TTM',	'BBD',	'BLNK',	'KMX',	'COLD',	'CIM',	'SNX',	'XERS',	'PXD',	'APRN',	'CSX',	'AMPE',	'QQQ',	'IWM',	'XLF',	'HYG',	'GLD',	'SLV',	'EEM',	'VXX',	'EFA',	'GDX',	'EWZ',	'XLE',	'DIA',	'TLT',	'KRE',	'XBI',	'TQQQ',	'XLU',	'SQQQ',	'FXI',	'UVXY',	'IYR',	'SPXS',	'XLK',	'USO',	'UNG',	'TNA',	'XOP',	'SPXU',	'FAS',	'GDXJ',	'XLY',	'SMH',	'SDS',	'XLV',	'TZA',	'SPXL',	'UUP',	'RSX',	'XLI',	'BKLN',	'UPRO',	'IBB',	'SDOW',	'JETS',	'NUGT',	'UCO',	'LQD',	'XRT',	'TBT',	'EMB',	'ITB',	'SH',	'GUSH',	'FAZ',	'XHB',	'LABU',	'EWW',	'ASHR',	'IYT',	'XLP',	'KWEB',	'IEF',	'XME',	'SVXY',	'SOXS',	'MDY',	'INDA',	'UDOW',	'CHAD',	'JNUG',	'ERX',	'LABD',	'IGV',	'AMLP',	'SHY',	'QID',	'OIH',	'SRTY',	'VNQ',	'FXE',	'VIXY',	'VTI',	'UDN',	'DXD',	'KBE',	'SSO',	'DFEN',	'DRIP',	'TMF',	'XLB',	'XIU.TO',	'IAU',	'VOO',	'EWP',	'UGA',	'FXY',	'SOXL',	'EWJ',	'TWM',	'DRV',	'XLC',	'SCO',	'EWU',	'DBA',	'FEZ',	'MJ',	'DUST',	'SIL',	'VIG',	'EWH',	'JDST',	'DOG',	'NAIL',	'EWQ',	'BNO',	'JNK',	'SILJ',	'DDM',	'VYM',	'YINN',	'VWO',	'RSP',	'TECL',	'TIP',	'CORN',	'USL',	'TECS',	'PFF',	'HMMJ.TO',	'BRZU',	'HDGE',	'IVV',	'BETZ',	'QLD',	'SOXX',	'EWT',	'CHAU',	'XLRE',	'RWM',	'EDC',	'AGQ',	'INDL',	'ILF',	'FXA',	'REM',	'PSQ',	'IJH',	'SPYG',	'EWG',	'ARKK',	'IJR',	'LIT',	'HYD',	'FXB',	'IWN',	'BOIL',	'DVY',	'SCHD',	'VTV',	'SKYY',	'YANG',	'MCHI',	'SPYV',	'IEI',	'UWM',	'BIB',	'EWY',	'FDN',	'SCHV',	'IEMG',	'SDIV',	'USMV',	'ZPR.TO',	'SPHD',	'BJK',	'URTY',	'PGX',	'SJB',	'TAN',	'DBO',	'EUFN',	'PBW',	'JO',	'DRN',	'SOYB',	'SKF',	'VUG',	'EFZ',	'SPDN',	'IWF',	'PSP',	'GSG',	'BOTZ',	'ITA',	'MUB',	'SPLV',	'IHF',	'VIXM',	'WEAT',	'IWO',	'EZA',	'BZQ',	'VGK',	'UGL',	'EZU',	'PGF',	'QUAL',	'TMV',	'KBWB',	'REMX',	'EWA',	'XDV.TO',	'CIBR',	'COW',	'ROM',	'SGOL',	'FXF',	'SOCL',	'MLPA',	'KBA',	'XGD.TO',	'VT',	'VBR',	'DBC',	'XRE.TO',	'EUO',	'TUR',	'RUSL',	'VEA',	'EWS',	'SDY',	'EDZ',	'GREK',	'SCHB',	'VXZ',	'ERY',	'RPV',	'UYG',	'VGT',	'FXC',	'AMZA',	'OEF',	'AMJ',	'VDE',	'TBF',	'KOLD',	'ARKW',	'MBB',	'URA',	'SIVR',	'IWD',	'ZQQ.TO',	'HGU.TO',	'FENY',	'DUG',	'IYZ',	'BND',	'DIG',	'VTWO',	'SRS',	'XPH',	'HNU.TO',	'NERD',	'NOBL',	'IWR',	'ZEB.TO',	'XSP.TO',	'BLOK',	'VFH',	'IVE',	'IXC',	'VB',	'XES',	'VPU',	'EWI',	'SBIO',	'AGG',	'EMLC',	'LBJ',	'SGG',	'IHI',	'ZROZ',	'ITOT',	'YOLO',	'MOO',	'TYD',	'PEY',	'XEG.TO',	'MGK',	'EUM',	'MIDU',	'IEFA',	'REW',	'PICK',	'BFOR',	'FNCL',	'ANGL',	'XFN.TO',	'EPI',	'CURE',	'DDG',	'SCHG',	'VHT',	'USD',	'EWM',	'DGRO',	'XIC.TO',	'IYG',	'PIN',	'BOND',	'ICLN',	'REK',	'DXJ',	'VOX',	'IJT',	'VCIT',	'IYW',	'ARKG',	'UNL',	'HACK',	'SPLG',	'THCX',	'IYF',	'IAT',	'NIB',	'PDBC',	'VPL',	'MXI',	'VXUS',	'ZSL',	'TLH',	'FIW',	'EFG',	'POTX',	'IPO',	'SCHE',	'HYLB',	'MTUM',	'PDP',	'SCHH',	'EET',	'JPNL',	'FHLC',	'DBE',	'CROP',	'EWC',	'IVW',	'RING',	'BLV',	'QYLD',	'CANE',	'GLL',	'HYS',	'VOE',	'IEZ',	'VCR',	'ACWI',	'ARGT',	'HND.TO',	'WOOD',	'PNQI',	'OUNZ',	'ZUT.TO',	'VNQI',	'FTEC',	'UBT',	'SJNK',	'ZSP.TO',	'BIS',	'PPH',	'IDNA',	'DEM',	'UMDD',	'GXC',	'SCHM',	'DFE',	'TDIV',	'VOT',	'ASHS',	'XSD',	'VAW',	'BAL',	'VDC',	'KIE',	'RXL',	'FXL',	'VO',	'EMLP',	'TTT',	'LTPZ',	'QQQE',	'IWV',	'URE',	'IYE',	'FNGS',	'IEO',	'YCS',	'BLCN',	'GOVT',	'RETL',	'VIIX',	'JJC',	'FCG',	'CHIX',	'VFV.TO',	'BRF',	'DTN',	'PGJ',	'PZA',	'SPSM',	'IGM',	'CWB',	'ESPO',	'PHO',	'IWB',	'KOL',	'SPHB',	'IEUR',	'IWP',	'VXF',	'USHY',	'IYJ',	'PXJ',	'XHE',	'JJG',	'FDIS',	'HEFA',	'IJS',	'SCHX',	'REZ',	'GSIE',	'PPA',	'BIV',	'FNDX',	'IRBO',	'SEF',	'TFI',	'EIDO',	'SPTM',	'BNDX',	'CNXT',	'MDIV',	'RWR',	'UTSL',	'BBH',	'SCZ',	'SIZE',	'GWX',	'VBK',	'HYMB',	'THD',	'DBB',	'QQEW',	'IDV',	'IWC',	'XPP',	'ITM',	'IEV',	'VEU',	'XAR',	'FXP',	'CROC',	'PST',	'SCHP',	'SRVR',	'IWS',	'HOD.TO',	'IOO',	'VCLT',	'ECH',	'IGF',	'YXI']


test = ['NVDA']

total_tickers = len(stx)
counter = 0

for tick in stx:
    if counter % 10 == 0:
        print("Processing data...", counter,"of",total_tickers,"complete")

    try:
        data = yf.Ticker(tick)
        #print(data.recommendations)


        dates = data.options
        expiry = dates[0]
        options = data.option_chain(expiry)


        #get current stock Price
        s = si.get_live_price(tick)


        #get Call & Put Prices
        call_price = options.calls.lastPrice
        call_implied_vol = options.calls.impliedVolatility
        call_strike = options.calls.strike

        put_price = options.puts.lastPrice
        put_implied_vol = options.puts.impliedVolatility
        put_strike = options.puts.strike


        #calculation parameters
        interest_rate = 0
        time = 0
        sigma = 0
        strike = 0
        stock = 0



        #Calculating Puts
        for i in range (len(put_strike)):

            interest_rate = r
            time = t
            stock = s
            sigma = put_implied_vol[i]
            strike = put_strike[i]


            price , delta = BS_put(stock, strike, time, interest_rate, sigma)

            delta = round(delta,3)

            if strike < s:
                tickers.append(tick)
                current.append(stock)
                prices.append(price)
                strikes.append(strike)
                deltas.append(delta)
                return_.append(round(100*((put_price[i]*100)/ (stock*100)),3))



    except:
        print("Failed for stock: ", tick)

    counter = counter +1


print("Creating Excel File...")
file = pd.DataFrame({
    'Ticker' : tickers,
    'Current Price' : current,
    'Strike Price' : strikes,
    'Put Price' : prices,
    'Delta' : deltas,
    'Return(%)' : return_,
})

writer = pd.ExcelWriter('/users/satish/Desktop/put_screener.xlsx', engine = 'xlsxwriter')
file.to_excel(writer, sheet_name= 'screener')
writer.save()





