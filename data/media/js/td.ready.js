$().ready(function() {

    TD.DataFilter.registerFilter({
        name: 'amount',
        label: 'Amount',
        help: 'This is the amount of the contribution',
        field: TD.DataFilter.OperatorField
    });
    
    TD.DataFilter.registerFilter({
        name: 'cycle',
        label: 'Cycle',
        help: 'Election cycles. Odd cycles have only state-level contributions',
        field: TD.DataFilter.DropDownField,
        allowMultipleFields: true,
        options: [
            ['1990','1990'], ['1991','1991'], ['1992','1992'],
            ['1993','1993'], ['1994','1994'], ['1995','1995'],
            ['1996','1996'], ['1997','1997'], ['1998','1998'],
            ['1999','1999'], ['2000','2000'], ['2001','2001'],
            ['2002','2002'], ['2003','2003'], ['2004','2004'],
            ['2005','2005'], ['2006','2006'], ['2007','2007'],
            ['2008','2008'], ['2009','2009'], ['2010','2010']
        ]
    });
    
    TD.DataFilter.registerFilter({
        name: 'contributor_ft',
        label: 'Contributor',
        help: 'Name of individual, employer, or organization that made contribution',
        field: TD.DataFilter.TextField,
        allowMultipleFields: true,
    });

    TD.DataFilter.registerFilter({
        name: 'contributor_state',
        label: 'Contributor State',
        help: 'State from which the contribution was made',
        field: TD.DataFilter.DropDownField,
        allowMultipleFields: true,
        options: [
            ['AL', 'Alabama'],          ['AK', 'Alaska'],       ['AZ', 'Arizona'],      ['AR', 'Arkansas'],
            ['CA', 'California'],       ['CO', 'Colorado'],     ['CT', 'Connecticut'],  ['DE', 'Delaware'],
            ['DC', 'District of Columbia'],
            ['FL', 'Florida'],          ['GA', 'Georgia'],      ['HI', 'Hawaii'],       ['ID', 'Idaho'],
            ['IL', 'Illinois'],         ['IN', 'Indiana'],      ['IA', 'Iowa'],         ['KS', 'Kansas'],
            ['KY', 'Kentucky'],         ['LA', 'Louisiana'],    ['ME', 'Maine'],        ['MD', 'Maryland'],
            ['MA', 'Massachusetts'],    ['MI', 'Michigan'],     ['MN', 'Minnesota'],    ['MS', 'Mississippi'],
            ['MO', 'Missouri'],         ['MT', 'Montana'],      ['NE', 'Nebraska'],     ['NV', 'Nevada'],
            ['NH', 'New Hampshire'],    ['NJ', 'New Jersey'],   ['NM', 'New Mexico'],   ['NY', 'New York'],
            ['NC', 'North Carolina'],   ['ND', 'North Dakota'], ['OH', 'Ohio'],         ['OK', 'Oklahoma'],
            ['OR', 'Oregon'],           ['PA', 'Pennsylvania'], ['RI', 'Rhode Island'], ['SC', 'South Carolina'],
            ['SD', 'South Dakota'],     ['TN', 'Tennessee'],    ['TX', 'Texas'],        ['UT', 'Utah'],
            ['VT', 'Vermont'],          ['VA', 'Virginia'],     ['WA', 'Washington'],   ['WV', 'West Virginia'],
            ['WI', 'Wisconsin'],        ['WY', 'Wyoming']
        ]
    });
    
    TD.DataFilter.registerFilter({
        name: 'date',
        label: 'Date',
        help: 'This is the date of the contribution',
        field: TD.DataFilter.DateRangeField
    });
    
    TD.DataFilter.registerFilter({
        name: 'employer_ft',
        label: 'Employer',
        help: 'Name of employer or organization associated with contribution',
        field: TD.DataFilter.TextField,
    });
    
    TD.DataFilter.registerFilter({
        name: 'transaction_namespace',
        label: 'Federal/State',
        help: 'State or federal office',
        field: TD.DataFilter.DropDownField,
        options: [
            ['urn:fec:transaction','Federal'],
            ['urn:nimsp:transaction','State']
        ]
    });

    TD.DataFilter.registerFilter({
        name: 'for_against',
        label: 'For/against candidate',
        help: 'Contributions can be made in support of or against a candidate',
        field: TD.DataFilter.DropDownField,
        options: [
            ['for','For the candidate'],
            ['against','Against the candidate']
        ]
    });
    
    TD.DataFilter.registerFilter({
        name: 'industry',
        label: 'Industry',
        help: 'The industry in which the person or organization making the contribution is involved',
        field: TD.DataFilter.DualDropDownField,
        allowMultipleFields: true,
        options: [
            ['A01', 'Crop Production & Basic Processing', [
            	['A1000', 'CROP PRODUCTION & BASIC PROCESSING'], ['A1100', 'COTTON'], ['A1200', 'SUGAR CANE & SUGAR BEETS'], ['A1400', 'VEGETABLES, FRUITS AND TREE NUT'], ['A1500', 'WHEAT, CORN, SOYBEANS AND CASH GRAIN'], ['A1600', 'OTHER COMMODITIES (INCL RICE, PEANUTS, HONEY)']
            ]],
            ['A02', 'Tobacco', [
            	['A1300', 'TOBACCO & TOBACCO PRODUCTS']
            ]],
            ['A04', 'Dairy', [
            	['A2000', 'MILK & DAIRY PRODUCERS']
            ]],
            ['A05', 'Poultry & Eggs', [
            	['A2300', 'POULTRY & EGGS']
            ]],
            ['A06', 'Livestock', [
            	['A3000', 'LIVESTOCK'], ['A3200', 'SHEEP AND WOOL PRODUCERS'], ['A3300', 'FEEDLOTS & RELATED LIVESTOCK SERVICES'], ['A3500', 'HORSE BREEDERS']
            ]],
            ['A07', 'Agricultural Services/Products', [
            	['A3100', 'ANIMAL FEED & HEALTH PRODUCTS'], ['A4000', 'AGRICULTURAL SERVICES & RELATED INDUSTRIES'], ['A4100', 'AGRICULTURAL CHEMICALS (FERTILIZERS & PESTICIDES)'], ['A4200', 'FARM MACHINERY & EQUIPMENT'], ['A4300', 'GRAIN TRADERS & TERMINALS'], ['A4500', 'VETERINARIANS'], ['A6000', 'FARM ORGANIZATIONS & COOPERATIVES'], ['A6500', 'FARM BUREAUS'], ['A8000', 'FLORISTS & NURSERY SERVICES']
            ]],
            ['A09', 'Food Processing & Sales', [
            	['G2000', 'FOOD & BEVERAGE PRODUCTS AND SERVICES'], ['G2100', 'FOOD AND KINDRED PRODUCTS MANUFACTURING'], ['G2300', 'MEAT PROCESSING & PRODUCTS'], ['G2400', 'FOOD STORES'], ['G2500', 'FOOD WHOLESALERS']
            ]],
            ['A10', 'Forestry & Forest Products', [
            	['A5000', 'FORESTRY & FOREST PRODUCTS'], ['A5200', 'PAPER & PULP MILLS AND PAPER MANUFACTURING']
            ]],
            ['A11', 'Misc Agriculture', [
            	['A0000', 'AGRICULTURE']
            ]],
            ['B00', 'Misc Communications/Electronics', [
            	['C0000', 'COMMUNICATIONS & ELECTRONICS']
            ]],
            ['B01', 'Printing & Publishing', [
            	['C1000', 'PRINTING AND PUBLISHING (PRINTED & ONLINE)'], ['C1100', 'BOOK, NEWSPAPER & PERIODICAL PUBLISHING'], ['C1300', 'COMMERCIAL PRINTING & TYPESETTING'], ['C1400', 'GREETING CARD PUBLISHING']
            ]],
            ['B02', 'TV/Movies/Music', [
            	['C2000', 'ENTERTAINMENT INDUSTRY/BROADCAST & MOTION PICTURES'], ['C2100', 'COMMERCIAL TV & RADIO STATIONS'], ['C2200', 'CABLE & SATELLITE TV PRODUCTION & DISTRIBUTION'], ['C2300', 'TV PRODUCTION & DISTRIBUTION'], ['C2400', 'MOTION PICTURE PRODUCTION & DISTRIBUTION'], ['C2600', 'RECORDED MUSIC & MUSIC PRODUCTION'], ['C2700', 'MOVIE THEATERS'], ['C2800', 'BANDS, ORCHESTRAS & OTHER LIVE MUSIC PRODUCTION'], ['C2900', 'LIVE THEATER & OTHER ENTERTAINMENT PRODUCTIONS']
            ]],
            ['B08', 'Telephone Utilities', [
            	['C4100', 'TELEPHONE UTILITIES'], ['C4200', 'LONG-DISTANCE TELEPHONE & TELEGRAPH SERVICE']
            ]],
            ['B09', 'Telecom Services & Equipment', [
            	['C4000', 'TELECOMMUNICATIONS'], ['C4300', 'CELLULAR SYSTEMS AND EQUIPMENT'], ['C4400', 'SATELLITE COMMUNICATIONS'], ['C4500', 'OTHER COMMUNICATIONS SERVICES'], ['C4600', 'TELEPHONE & COMMUNICATIONS EQUIPMENT']
            ]],
            ['B11', 'Electronics Mfg & Services', [
            	['C5000', 'ELECTRONICS MANUFACTURING & SERVICES']
            ]],
            ['B12', 'Computers/Internet', [
            	['C5100', 'COMPUTER MANUFACTURE & SERVICES'], ['C5110', 'COMPUTERS, COMPONENTS & ACCESSORIES'], ['C5120', 'COMPUTER SOFTWARE'], ['C5130', 'DATA PROCESSING & COMPUTER SERVICES'], ['C5140', 'ONLINE COMPUTER SERVICES']
            ]],
            ['C01', 'General Contractors', [
            	['B0000', 'CONSTRUCTION & PUBLIC WORKS'], ['B0500', 'BUILDERS ASSOCIATIONS'], ['B1000', 'PUBLIC WORKS, INDUSTRIAL & COMMERCIAL CONSTRUCTION'], ['B1200', 'DREDGING CONTRACTORS'], ['B1500', 'CONSTRUCTION, UNCLASSIFIED']
            ]],
            ['C02', 'Home Builders', [
            	['B2000', 'RESIDENTIAL CONSTRUCTION'], ['B2400', 'MOBILE HOME CONSTRUCTION']
            ]],
            ['C03', 'Special Trade Contractors', [
            	['B3000', 'SPECIAL TRADE CONTRACTORS'], ['B3200', 'ELECTRICAL CONTRACTORS'], ['B3400', 'PLUMBING, HEATING & AIR CONDITIONING'], ['B3600', 'LANDSCAPING & EXCAVATION SVCS']
            ]],
            ['C04', 'Construction Services', [
            	['B4000', 'ENGINEERING, ARCHITECTURE & CONSTRUCTION MGMT SVCS'], ['B4200', 'ARCHITECTURAL SERVICES'], ['B4300', 'SURVEYING'], ['B4400', 'ENGINEERS - TYPE UNKNOWN']
            ]],
            ['C05', 'Building Materials & Equipment', [
            	['B5000', 'BUILDING MATERIALS'], ['B5100', 'STONE, CLAY, GLASS & CONCRETE PRODUCTS'], ['B5200', 'LUMBER AND WOOD PRODUCTS'], ['B5300', 'PLUMBING & PIPE PRODUCTS'], ['B5400', 'OTHER CONSTRUCTION-RELATED PRODUCTS'], ['B5500', 'ELECTRICAL SUPPLY'], ['B6000', 'CONSTRUCTION EQUIPMENT']
            ]],
            ['D01', 'Defense Aerospace', [
            	['D2000', 'DEFENSE AEROSPACE CONTRACTORS']
            ]],
            ['D02', 'Defense Electronics', [
            	['D3000', 'DEFENSE ELECTRONIC CONTRACTORS']
            ]],
            ['D03', 'Misc Defense', [
            	['D0000', 'DEFENSE'], ['D4000', 'DEFENSE RESEARCH & DEVELOPMENT'], ['D5000', 'DEFENSE SHIPBUILDERS'], ['D6000', 'HOMELAND SECURITY CONTRACTORS'], ['D8000', 'GROUND-BASED & OTHER WEAPONS SYSTEMS'], ['D9000', 'DEFENSE-RELATED SERVICES']
            ]],
            ['E01', 'Oil & Gas', [
            	['E1100', 'OIL & GAS'], ['E1110', 'MAJOR (MULTINATIONAL) OIL & GAS PRODUCERS'], ['E1120', 'INDEPENDENT OIL & GAS PRODUCERS'], ['E1140', 'NATURAL GAS TRANSMISSION & DISTRIBUTION'], ['E1150', 'OILFIELD SERVICE, EQUIPMENT & EXPLORATION'], ['E1160', 'PETROLEUM REFINING & MARKETING'], ['E1170', 'GASOLINE SERVICE STATIONS'], ['E1180', 'FUEL OIL DEALERS'], ['E1190', 'LPG/LIQUID PROPANE DEALERS & PRODUCERS']
            ]],
            ['E04', 'Mining', [
            	['E1200', 'MINING'], ['E1210', 'COAL MINING'], ['E1220', 'METAL MINING & PROCESSING'], ['E1230', 'NON-METALLIC MINING'], ['E1240', 'MINING SERVICES & EQUIPMENT']
            ]],
            ['E07', 'Misc Energy', [
            	['E0000', 'ENERGY, NATURAL RESOURCES AND ENVIRONMENT'], ['E1000', 'ENERGY PRODUCTION & DISTRIBUTION'], ['E1500', 'ALTERNATE ENERGY PRODUCTION & SERVICES'], ['E1700', 'POWER PLANT CONSTRUCTION & EQUIPMENT'], ['E5000', 'WATER UTILITIES']
            ]],
            ['E08', 'Electric Utilities', [
            	['E1300', 'NUCLEAR ENERGY'], ['E1320', 'NUCLEAR PLANT CONSTRUCTION, EQUIPMENT & SVCS'], ['E1600', 'ELECTRIC POWER UTILITIES'], ['E1610', 'RURAL ELECTRIC COOPERATIVES'], ['E1620', 'GAS & ELECTRIC UTILITIES'], ['E1630', 'INDEPENDENT POWER GENERATION & COGENERATION']
            ]],
            ['E09', 'Environmental Svcs/Equipment', [
            	['E2000', 'ENVIRONMENTAL SERVICES, EQUIPMENT & CONSULTING']
            ]],
            ['E10', 'Waste Management', [
            	['E3000', 'WASTE MANAGEMENT']
            ]],
            ['E11', 'Fisheries & Wildlife', [
            	['E4000', 'FISHERIES & WILDLIFE'], ['E4100', 'FISHING'], ['E4200', 'HUNTING & WILDLIFE']
            ]],
            ['F03', 'Commercial Banks', [
            	['F1000', 'BANKS & LENDING INSTITUTIONS'], ['F1100', 'COMMERCIAL BANKS & BANK HOLDING COMPANIES']
            ]],
            ['F04', 'Savings & Loans', [
            	['F1200', 'SAVINGS BANKS & SAVINGS AND LOANS']
            ]],
            ['F05', 'Credit Unions', [
            	['F1300', 'CREDIT UNIONS']
            ]],
            ['F06', 'Finance/Credit Companies', [
            	['F1400', 'CREDIT AGENCIES & FINANCE COMPANIES']
            ]],
            ['F07', 'Securities & Investment', [
            	['F2000', 'SECURITIES, COMMODITIES & INVESTMENT'], ['F2100', 'SECURITY BROKERS & INVESTMENT COMPANIES'], ['F2200', 'COMMODITY BROKERS/DEALERS'], ['F2300', 'INVESTMENT BANKING'], ['F2400', 'STOCK EXCHANGES'], ['F2500', 'VENTURE CAPITAL'], ['F2600', 'PRIVATE EQUITY & INVESTMENT FIRMS'], ['F2700', 'HEDGE FUNDS']
            ]],
            ['F09', 'Insurance', [
            	['F3000', 'INSURANCE'], ['F3100', 'INSURANCE COMPANIES, BROKERS & AGENTS'], ['F3200', 'ACCIDENT & HEALTH INSURANCE'], ['F3300', 'LIFE INSURANCE'], ['F3400', 'PROPERTY & CASUALTY INSURANCE']
            ]],
            ['F10', 'Real Estate', [
            	['F4000', 'REAL ESTATE'], ['F4100', 'REAL ESTATE DEVELOPERS & SUBDIVIDERS'], ['F4200', 'REAL ESTATE AGENTS'], ['F4300', 'TITLE INSURANCE & TITLE ABSTRACT OFFICES'], ['F4400', 'MOBILE HOME DEALERS & PARKS'], ['F4500', 'BUILDING OPERATORS AND MANAGERS'], ['F4600', 'MORTGAGE BANKERS AND BROKERS'], ['F4700', 'OTHER REAL ESTATE SERVICES']
            ]],
            ['F11', 'Accountants', [
            	['F5100', 'ACCOUNTANTS']
            ]],
            ['F13', 'Misc Finance', [
            	['F0000', 'FINANCE, INSURANCE & REAL ESTATE'], ['F5000', 'FINANCIAL SERVICES & CONSULTING'], ['F5200', 'CREDIT REPORTING SERVICES & COLLECTION AGENCIES'], ['F5300', 'TAX RETURN SERVICES'], ['F5500', 'OTHER FINANCIAL SERVICES'], ['F7000', 'INVESTORS']
            ]],
            ['H01', 'Health Professionals', [
            	['H1000', 'HEALTH PROFESSIONALS'], ['H1100', 'PHYSICIANS'], ['H1110', 'PSYCHIATRISTS & PSYCHOLOGISTS'], ['H1120', 'OPTOMETRISTS & OPHTHALMOLOGISTS'], ['H1130', 'OTHER PHYSICIAN SPECIALISTS'], ['H1400', 'DENTISTS'], ['H1500', 'CHIROPRACTORS'], ['H1700', 'OTHER NON-PHYSICIAN HEALTH PRACTITIONERS'], ['H1710', 'NURSES'], ['H1750', 'PHARMACISTS']
            ]],
            ['H02', 'Hospitals/Nursing Homes', [
            	['H2000', 'HEALTH CARE INSTITUTIONS'], ['H2100', 'HOSPITALS'], ['H2200', 'NURSING HOMES'], ['H2300', 'DRUG & ALCOHOL TREATMENT HOSPITALS']
            ]],
            ['H03', 'Health Services/HMOs', [
            	['H3000', 'HEALTH CARE SERVICES'], ['H3100', 'HOME CARE SERVICES'], ['H3200', 'OUTPATIENT HEALTH SERVICES (INCL DRUG & ALCOHOL)'], ['H3300', 'OPTICAL SERVICES (GLASSES & CONTACT LENSES)'], ['H3400', 'MEDICAL LABORATORIES'], ['H3500', 'AIDS TREATMENT & TESTING'], ['H3700', 'HMOS'], ['H3800', 'MENTAL HEALTH SERVICES']
            ]],
            ['H04', 'Pharmaceuticals/Health Products', [
            	['H4000', 'HEALTH CARE PRODUCTS'], ['H4100', 'MEDICAL SUPPLIES MANUFACTURING & SALES'], ['H4200', 'PERSONAL HEALTH CARE PRODUCTS'], ['H4300', 'PHARMACEUTICAL MANUFACTURING'], ['H4400', 'PHARMACEUTICAL WHOLESALE'], ['H4500', 'BIOTECH PRODUCTS & RESEARCH'], ['H4600', 'NUTRITIONAL & DIETARY SUPPLEMENTS']
            ]],
            ['H05', 'Misc Health', [
            	['H0000', 'HEALTH, EDUCATION & HUMAN RESOURCES']
            ]],
            ['K01', 'Lawyers/Law Firms', [
            	['K0000', 'LEGAL SERVICES'], ['K1000', 'ATTORNEYS & LAW FIRMS'], ['K1100', 'TRIAL LAWYERS & LAW FIRMS'], ['K1200', 'CORPORATE LAWYERS & LAW FIRMS']
            ]],
            ['K02', 'Lobbyists', [
            	['K2000', 'LOBBYISTS & PUBLIC RELATIONS'], ['K2100', 'REGISTERED FOREIGN AGENTS']
            ]],
            ['M01', 'Air Transport', [
            	['T1000', 'AIR TRANSPORT'], ['T1100', 'AIRLINES'], ['T1200', 'AIRCRAFT MANUFACTURERS'], ['T1300', 'AIRCRAFT PARTS & EQUIPMENT'], ['T1400', 'GENERAL AVIATION (PRIVATE PILOTS)'], ['T1500', 'AIR FREIGHT'], ['T1600', 'AVIATION SERVICES & AIRPORTS'], ['T1700', 'SPACE VEHICLES & COMPONENTS'], ['T7100', 'EXPRESS DELIVERY SERVICES']
            ]],
            ['M02', 'Automotive', [
            	['T2000', 'AUTOMOTIVE, MISC'], ['T2100', 'AUTO MANUFACTURERS'], ['T2200', 'TRUCK/AUTOMOTIVE PARTS & ACCESSORIES'], ['T2300', 'AUTO DEALERS, NEW & USED'], ['T2310', 'AUTO DEALERS, FOREIGN IMPORTS'], ['T2400', 'AUTO REPAIR'], ['T2500', 'CAR RENTAL AGENCIES']
            ]],
            ['M03', 'Trucking', [
            	['T3000', 'TRUCKING'], ['T3100', 'TRUCKING COMPANIES & SERVICES'], ['T3200', 'TRUCK & TRAILER MANUFACTURERS']
            ]],
            ['M04', 'Railroads', [
            	['T5000', 'RAILROAD TRANSPORTATION'], ['T5100', 'RAILROADS'], ['T5200', 'MANUFACTURERS OF RAILROAD EQUIPMENT'], ['T5300', 'RAILROAD SERVICES']
            ]],
            ['M05', 'Sea Transport', [
            	['T6000', 'SEA TRANSPORT'], ['T6100', 'SHIP BUILDING & REPAIR'], ['T6200', 'SEA FREIGHT & PASSENGER SERVICES'], ['T6250', 'CRUISE SHIPS & LINES']
            ]],
            ['M06', 'Misc Transport', [
            	['T0000', 'TRANSPORTATION'], ['T4000', 'BUSES & TAXIS'], ['T4100', 'BUS SERVICES'], ['T4200', 'TAXICABS'], ['T7000', 'FREIGHT & DELIVERY SERVICES'], ['T8000', 'RECREATIONAL TRANSPORT'], ['T8100', 'MOTORCYCLES, SNOWMOBILES & OTHER MOTORIZED VEHICLE'], ['T8200', 'MOTOR HOMES & CAMPER TRAILERS'], ['T8300', 'PLEASURE BOATS'], ['T8400', 'BICYCLES & OTHER NON-MOTORIZED RECREATIONAL TRANSP']
            ]],
            ['N00', 'Business Associations', [
            	['G1000', 'GENERAL BUSINESS ASSOCIATIONS'], ['G1100', 'CHAMBERS OF COMMERCE'], ['G1200', 'SMALL BUSINESS ASSOCIATIONS'], ['G1300', 'PRO-BUSINESS ASSOCIATIONS'], ['G1310', 'BUSINESS TAX COALITIONS'], ['G1400', 'INTERNATIONAL TRADE ASSOCIATIONS']
            ]],
            ['N01', 'Food & Beverage', [
            	['G2110', 'ARTIFICIAL SWEETENERS AND FOOD ADDITIVES'], ['G2200', 'CONFECTIONERY PROCESSORS & MANUFACTURERS'], ['G2350', 'FISH PROCESSING'], ['G2600', 'BEVERAGES (NON-ALCOHOLIC)'], ['G2700', 'BEVERAGE BOTTLING & DISTRIBUTION'], ['G2900', 'RESTAURANTS & DRINKING ESTABLISHMENTS'], ['G2910', 'FOOD CATERING & FOOD SERVICES']
            ]],
            ['N02', 'Beer, Wine & Liquor', [
            	['G2800', 'ALCOHOL'], ['G2810', 'BEER'], ['G2820', 'WINE & DISTILLED SPIRITS MANUFACTURING'], ['G2840', 'LIQUOR STORES'], ['G2850', 'LIQUOR WHOLESALERS']
            ]],
            ['N03', 'Retail Sales', [
            	['G4000', 'RETAIL TRADE'], ['G4100', 'APPAREL & ACCESSORY STORES'], ['G4200', 'CONSUMER ELECTRONICS & COMPUTER STORES'], ['G4300', 'DEPARTMENT, VARIETY & CONVENIENCE STORES'], ['G4400', 'FURNITURE & APPLIANCE STORES'], ['G4500', 'HARDWARE & BUILDING MATERIALS STORES'], ['G4600', 'MISCELLANEOUS RETAIL STORES'], ['G4700', 'CATALOG & MAIL ORDER HOUSES'], ['G4800', 'DIRECT SALES'], ['G4850', 'VENDING MACHINE SALES & SERVICES'], ['G4900', 'DRUG STORES']
            ]],
            ['N04', 'Misc Services', [
            	['G5000', 'SERVICES'], ['G5100', 'BEAUTY & BARBER SHOPS'], ['G5300', 'EQUIPMENT RENTAL & LEASING'], ['G5400', 'FUNERAL SERVICES'], ['G5500', 'LAUNDRIES & DRY CLEANERS'], ['G5600', 'MISCELLANEOUS REPAIR SERVICES'], ['G5700', 'PEST CONTROL'], ['G5800', 'PHYSICAL FITNESS CENTERS'], ['G6800', 'VIDEO TAPE RENTAL']
            ]],
            ['N05', 'Business Services', [
            	['G5200', 'BUSINESS SERVICES'], ['G5210', 'ADVERTISING & PUBLIC RELATIONS SERVICES'], ['G5220', 'DIRECT MAIL ADVERTISING SERVICES'], ['G5230', 'OUTDOOR ADVERTISING SERVICES'], ['G5240', 'COMMERCIAL PHOTOGRAPHY, ART & GRAPHIC DESIGN'], ['G5250', 'EMPLOYMENT AGENCIES'], ['G5260', 'POLITICAL CONSULTANTS/ADVISERS'], ['G5270', 'MANAGEMENT CONSULTANTS & SERVICES'], ['G5280', 'MARKETING RESEARCH SERVICES'], ['G5290', 'SECURITY SERVICES']
            ]],
            ['N06', 'Recreation/Live Entertainment', [
            	['G6000', 'RECREATION/ENTERTAINMENT'], ['G6100', 'AMUSEMENT/RECREATION CENTERS'], ['G6400', 'PROFESSIONAL SPORTS, ARENAS & RELATED EQUIP & SVCS'], ['G6700', 'AMUSEMENT PARKS']
            ]],
            ['N07', 'Casinos/Gambling', [
            	['G6500', 'CASINOS, RACETRACKS & GAMBLING'], ['G6550', 'INDIAN GAMING']
            ]],
            ['N08', 'Lodging/Tourism', [
            	['T9000', 'LODGING & TOURISM'], ['T9100', 'HOTELS & MOTELS'], ['T9300', 'RESORTS'], ['T9400', 'TRAVEL AGENTS']
            ]],
            ['N12', 'Misc Business', [
            	['G0000', 'GENERAL COMMERCE'], ['G3000', 'WHOLESALE TRADE'], ['G3500', 'IMPORT/EXPORT SERVICES'], ['G7000', 'CORRECTIONAL FACILITIES CONSTR & MGMT/FOR-PROFIT'], ['T7200', 'WAREHOUSING']
            ]],
            ['N13', 'Chemical & Related Manufacturing', [
            	['M1000', 'CHEMICALS'], ['M1100', 'EXPLOSIVES'], ['M1300', 'HOUSEHOLD CLEANSERS & CHEMICALS'], ['M1500', 'PLASTICS & RUBBER PROCESSING & PRODUCTS'], ['M1600', 'PAINTS, SOLVENTS & COATINGS'], ['M1700', 'ADHESIVES & SEALANTS']
            ]],
            ['N14', 'Steel Production', [
            	['M2100', 'STEEL']
            ]],
            ['N15', 'Misc Manufacturing & Distributing', [
            	['M0000', 'MANUFACTURING'], ['M1400', 'MANMADE FIBERS'], ['M2000', 'HEAVY INDUSTRIAL MANUFACTURING'], ['M2200', 'SMELTING & NON-PETROLEUM REFINING'], ['M2250', 'ALUMINUM MINING/PROCESSING'], ['M2300', 'INDUSTRIAL/COMMERCIAL EQUIPMENT & MATERIALS'], ['M2400', 'RECYCLING OF METAL, PAPER, PLASTICS, ETC.'], ['M3000', 'PERSONAL PRODUCTS MANUFACTURING'], ['M3100', 'CLOTHING & ACCESSORIES'], ['M3200', 'SHOES & LEATHER PRODUCTS'], ['M3300', 'TOILETRIES & COSMETICS'], ['M3400', 'JEWELRY'], ['M3500', 'TOYS'], ['M3600', 'SPORTING GOODS SALES & MANUFACTURING'], ['M4000', 'HOUSEHOLD & OFFICE PRODUCTS'], ['M4100', 'FURNITURE & WOOD PRODUCTS'], ['M4200', 'OFFICE MACHINES'], ['M4300', 'HOUSEHOLD APPLIANCES'], ['M5000', 'FABRICATED METAL PRODUCTS'], ['M5100', 'HARDWARE & TOOLS'], ['M5200', 'ELECTROPLATING, POLISHING & RELATED SERVICES'], ['M5300', 'SMALL ARMS & AMMUNITION'], ['M6000', 'ELECTRICAL LIGHTING PRODUCTS'], ['M7000', 'PAPER, GLASS & PACKAGING MATERIALS'], ['M7100', 'PAPER PACKAGING MATERIALS'], ['M7200', 'GLASS PRODUCTS'], ['M7300', 'METAL CANS & CONTAINERS'], ['M9000', 'PRECISION INSTRUMENTS'], ['M9100', 'OPTICAL INSTRUMENTS & LENSES'], ['M9200', 'PHOTOGRAPHIC EQUIPMENT & SUPPLIES'], ['M9300', 'CLOCKS & WATCHES']
            ]],
            ['N16', 'Textiles', [
            	['M8000', 'TEXTILES & FABRICS']
            ]],
            ['P01', 'Building Trade Unions', [
            	['LB100', 'BUILDING TRADES UNIONS']
            ]],
            ['P02', 'Industrial Unions', [
            	['LC100', 'COMMUNICATIONS & HI-TECH UNIONS'], ['LC150', 'IBEW (INTL BROTHERHOOD OF ELECTRICAL WORKERS)'], ['LE100', 'MINING UNIONS'], ['LE200', 'ENERGY-RELATED UNIONS (NON-MINING)'], ['LM100', 'MANUFACTURING UNIONS'], ['LM150', 'AUTOMOTIVE UNIONS']
            ]],
            ['P03', 'Transportation Unions', [
            	['LT000', 'TRANSPORTATION UNIONS'], ['LT100', 'AIR TRANSPORT UNIONS'], ['LT300', 'TEAMSTERS UNION'], ['LT400', 'RAILROAD UNIONS'], ['LT500', 'MERCHANT MARINE & LONGSHOREMEN UNIONS'], ['LT600', 'OTHER TRANSPORTATION UNIONS']
            ]],
            ['P04', 'Public Sector Unions', [
            	['L1000', 'CIVIL SERVICE & GOVERNMENT UNIONS'], ['L1100', 'FEDERAL EMPLOYEES UNIONS'], ['L1200', 'STATE & LOCAL GOVT EMPLOYEE UNIONS'], ['L1300', 'TEACHERS UNIONS'], ['L1400', 'POLICE & FIREFIGHTERS UNIONS & ASSOCIATIONS'], ['L1500', 'US POSTAL SERVICE UNIONS & ASSOCIATIONS']
            ]],
            ['P05', 'Misc Unions', [
            	['L0000', 'LABOR UNIONS'], ['L5000', 'OTHER UNIONS'], ['LA100', 'AGRICULTURAL LABOR UNIONS'], ['LD100', 'DEFENSE-RELATED UNIONS'], ['LG000', 'GENERAL COMMERCIAL UNIONS'], ['LG100', 'FOOD SERVICE & RELATED UNIONS'], ['LG200', 'RETAIL TRADE UNIONS'], ['LG300', 'COMMERCIAL SERVICE UNIONS'], ['LG400', 'ENTERTAINMENT UNIONS'], ['LG500', 'OTHER COMMERCIAL UNIONS'], ['LH100', 'HEALTH WORKER UNIONS']
            ]],
            ['Q01', 'Republican/Conservative', [
            	['J1100', 'REPUBLICAN/CONSERVATIVE'], ['J1110', 'CHRISTIAN CONSERVATIVE']
            ]],
            ['Q02', 'Democratic/Liberal', [
            	['J1200', 'DEMOCRATIC/LIBERAL']
            ]],
            ['Q03', 'Leadership PACs', [
            	['J2000', 'LEADERSHIP COMMITTEES'], ['J2100', 'DEMOCRATIC LEADERSHIP PAC'], ['J2200', 'REPUBLICAN LEADERSHIP PAC'], ['J2300', 'DEMOCRATIC OFFICIALS, CANDIDATES & FORMER MEMBERS'], ['J2400', 'REPUBLICAN OFFICIALS, CANDIDATES & FORMER MEMBERS'], ['J2500', 'NON-FEDERAL CANDIDATE COMMITTEES']
            ]],
            ['Q04', 'Foreign & Defense Policy', [
            	['J5000', 'FOREIGN POLICY'], ['J5200', 'ANTI-CASTRO'], ['J5300', 'PUERTO RICO STATEHOOD POLICY'], ['J5400', 'PRO-ARAB'], ['JD100', 'DEFENSE POLICY, HAWKS'], ['JD200', 'DEFENSE POLICY, DOVES']
            ]],
            ['Q05', 'Pro-Israel', [
            	['J5100', 'PRO-ISRAEL']
            ]],
            ['Q08', 'Women\'s Issues', [
            	['J7400', 'WOMEN\'S ISSUES']
            ]],
            ['Q09', 'Human Rights', [
            	['J7000', 'HUMAN RIGHTS'], ['J7300', 'GAY & LESBIAN RIGHTS & ISSUES'], ['J7500', 'MINORITY/ETHNIC GROUPS'], ['J7700', 'CHILDREN\'S RIGHTS'], ['JH100', 'HEALTH & WELFARE POLICY']
            ]],
            ['Q10', 'Misc Issues', [
            	['J0000', 'IDEOLOGICAL & SINGLE ISSUE PACS'], ['J1000', 'GENERAL IDEOLOGICAL'], ['J1300', 'THIRD-PARTY COMMITTEES'], ['J3000', 'CONSUMER GROUPS'], ['J4000', 'FISCAL & TAX POLICY'], ['J6500', 'MILITIAS & ANTI-GOVERNMENT GROUPS'], ['J7200', 'ELDERLY ISSUES/SOCIAL SECURITY'], ['J7210', 'LEGALIZATION OF DOCTOR-ASSISTED SUICIDE'], ['J7600', 'ANIMAL RIGHTS'], ['J8000', 'LABOR, ANTI-UNION'], ['J9000', 'OTHER SINGLE-ISSUE OR IDEOLOGICAL GROUPS'], ['J9100', 'TERM LIMITS'], ['JW100', 'PRO-RESOURCE DEVELOPMENT GROUPS']
            ]],
            ['Q11', 'Environment', [
            	['JE300', 'ENVIRONMENTAL POLICY']
            ]],
            ['Q12', 'Gun Control', [
            	['J6100', 'ANTI-GUNS']
            ]],
            ['Q13', 'Gun Rights', [
            	['J6200', 'PRO-GUNS']
            ]],
            ['Q14', 'Abortion Policy/Pro-Life', [
            	['J7120', 'ABORTION POLICY/PRO-LIFE']
            ]],
            ['Q15', 'Abortion Policy/Pro-Choice', [
            	['J7150', 'ABORTION POLICY/PRO-CHOICE']
            ]],
            ['Q16', 'Candidate Committees', [
            	['Z1000', 'CANDIDATE COMMITTEES'], ['Z1100', 'REPUBLICAN CANDIDATE COMMITTEES'], ['Z1200', 'DEMOCRATIC CANDIDATE COMMITTEES'], ['Z1300', 'THIRD-PARTY CANDIDATE COMMITTEES'], ['Z1400', 'UNKNOWN-PARTY CANDIDATE COMMITTEES']
            ]],
            ['W02', 'Non-Profit Institutions', [
            	['X4000', 'NON-PROFITS'], ['X4100', 'NON-PROFIT FOUNDATIONS'], ['X4110', 'PHILANTHROPISTS'], ['X4200', 'MUSEUMS, ART GALLERIES, LIBRARIES, ETC.']
            ]],
            ['W03', 'Civil Servants/Public Officials', [
            	['X3000', 'CIVIL SERVANT/PUBLIC EMPLOYEE'], ['X3100', 'PUBLIC OFFICIAL (ELECTED OR APPOINTED)'], ['X3200', 'COURTS & JUSTICE SYSTEM'], ['X3300', 'MUNICIPAL & COUNTY GOVERNMENT ORGANIZATIONS'], ['X3700', 'US POSTAL SERVICE']
            ]],
            ['W04', 'Education', [
            	['H5000', 'EDUCATION'], ['H5100', 'SCHOOLS & COLLEGES'], ['H5150', 'MEDICAL SCHOOLS'], ['H5170', 'LAW SCHOOLS'], ['H5200', 'TECHNICAL, BUSINESS AND VOCATIONAL SCHOOLS & SVCS'], ['X3500', 'PUBLIC SCHOOL TEACHERS, ADMINISTRATORS & OFFICIALS']
            ]],
            ['W05', 'Clergy & Religious Organizations', [
            	['X7000', 'CHURCHES, CLERGY & RELIGIOUS ORGANIZATIONS']
            ]],
            ['W06', 'Retired', [
            	['X1200', 'RETIRED']
            ]],
            ['W07', 'Other', [
            	['H6000', 'WELFARE & SOCIAL WORK'], ['X0000', 'OTHER'], ['X5000', 'MILITARY'], ['X9000', 'FOREIGN GOVERNMENTS']
            ]],
            ['X00', 'State specific', [
            	['A4400', 'COMMODITY BROKERS & DEALERS'], ['A7000', 'FARMERS, CROP UNSPECIFIED'], ['F5400', 'PAYDAY/TITLE LOANS'], ['G3100', 'TOBACCO COMPANIES & TOBACCO PRODUCT SALES'], ['J1400', 'NONPARTISAN ELECTED OFFICIALS & CANDIDATES'], ['J2510', 'PACS OPERATED BY REPUBLICAN STATE POLITICIANS'], ['J2520', 'PACS OPERATED BY DEMOCRATIC STATE POLITICIANS'], ['J3500', 'REPUBLICAN-BASED GROUPS (BUT NOT OFFICIAL PARTY COMMITTEES) AND GENERIC CONSERVATIVE ONES'], ['J3600', 'DEMOCRATIC-BASED GROUPS (BUT NOT OFFICIAL PARTY COMMITTEES) AND GENERIC LIBERAL/PROGRESSIVE ONES'], ['J3700', 'CHRISTIAN COALITION, RELIGIOUS RIGHT'], ['LT200', 'AUTOMOTIVE UNIONS'], ['X3400', 'NATIVE AMERICAN TRIBES & GOVERNING UNITS'], ['Z2100', 'CONSERVATIVE/REPUBLICAN UNDER REPORTING THRESHOLD'], ['Z2200', 'LIBERAL/DEMOCRAT UNDER REPORTING THRESHOLD'], ['Z2300', 'THIRD-PARTY UNDER REPORTING THRESHOLD'], ['Z2400', 'NONPARTISAN CONTRIBUTIONS UNDER REPORTING THRESHOLD'], ['Z7777', 'OFFICE USE ONLY'], ['Z8888', 'CATCODE ERROR'], ['Z9010', 'REPUBLICAN CANDIDATE CONTRIBUTIONS TO OWN CAMPAIGN'], ['Z9020', 'DEMOCRATIC CANDIDATE CONTRIBUTIONS TO OWN CAMPAIGN'], ['Z9030', 'THIRD-PARTY CANDIDATE CONTRIBUTIONS TO OWN CAMPAIGN'], ['Z9040', 'NONPARTISAN CANDIDATE CONTRIBUTIONS TO OWN CAMPAIGN'], ['Z9800', 'CAMPAIGN FUNDING FROM PUBLIC SOURCES']
            ]],
            ['Y00', 'Unknown', [
            	['Y0000', 'UNKNOWN']
            ]],
            ['Y01', 'Homemakers/Non-income earners', [
            	['Y1000', 'HOMEMAKERS, STUDENTS & OTHER NON-INCOME EARNERS']
            ]],
            ['Y02', 'No Employer Listed or Found', [
            	['Y2000', 'NO EMPLOYER LISTED OR DISCOVERED']
            ]],
            ['Y03', 'Generic Occupation/Category Unknown', [
            	['Y3000', 'GENERIC OCCUPATION - IMPOSSIBLE TO ASSIGN CATEGORY']
            ]],
            ['Y04', 'Employer Listed/Category Unknown', [
            	['Y4000', 'EMPLOYER LISTED BUT CATEGORY UNKNOWN']
            ]],
            ['Z02', 'Party Committees', [
            	['Z5000', 'PARTY COMMITTEES'], ['Z5100', 'REPUBLICAN PARTY COMMITTEES'], ['Z5200', 'DEMOCRATIC PARTY COMMITTEES'], ['Z5300', 'THIRD-PARTY PARTY COMMITTEES']
            ]],
            ['Z04', 'Joint Candidate Cmte', [
            	['Z4100', 'REPUBLICAN JOINT CANDIDATE COMMITTEE'], ['Z4200', 'DEMOCRATIC JOINT CANDIDATE COMMITTEE'], ['Z4300', 'THIRD-PARTY JOINT CANDIDATE COMMITTEE']
            ]],
            ['Z07', 'Candidate Self-finance', [
            	['Z9000', 'CANDIDATE CONTRIBUTION TO HIS/HER OWN CAMPAIGN']
            ]],
            ['Z08', 'Party Committee Transfer', [
            	['Z9100', 'TRANSFER BETWEEN NATIONAL PARTY COMMITTEES']
            ]],
            ['Z09', 'Non-contribution', [
            	['Z9500', 'TRANSFER FROM INTERMEDIARY ( TYPE 24I OR 24T)'], ['Z9600', 'NON-CONTRIBUTION, MISCELLANEOUS'], ['Z9700', 'UNITEMIZED (SMALL) CONTRIBUTIONS'], ['Z9999', 'INTERNAL TRANSFER AND OTHER NON-CONTRIBUTIONS']
            ]]
        ]
    });
        
    TD.DataFilter.registerFilter({
        label: 'Office',
        name: 'seat',
        help: 'Office for which candidate is running',
        field: TD.DataFilter.DropDownField,
        allowMultipleFields: true,
        options: [
            ['federal:senate', 'US Senate'],
            ['federal:house', 'US House of Representatives'],
            ['federal:president', 'US President'],
            ['state:upper', 'State Upper Chamber'],
            ['state:lower', 'State Lower Chamber'],
            ['state:governor', 'State Governor']
        ]
    });
    
    // TD.DataFilter.registerFilter({
    //     name: 'organization_ft',
    //     label: 'Employer',
    //     help: 'Employer of individual that made contribution',
    //     field: TD.DataFilter.TextField,
    //     allowMultipleFields: true,
    // });
    
    TD.DataFilter.registerFilter({
        name: 'recipient_ft',
        label: 'Recipient',
        help: 'Name of candidate or PAC that received contribution',
        field: TD.DataFilter.TextField,
        allowMultipleFields: true,
    });
    
    TD.DataFilter.registerFilter({
        label: 'Transaction Type',
        name: 'transaction_type',
        help: 'The FEC transaction type of the contribution. You must remove the for/against filter for this filter to work properly.',
        field: TD.DataFilter.DropDownField,
        allowMultipleFields: true,
        options: [
            ['15', 'Contribution (15)'],
            ['15e', 'Earmarked contribution (15e)'],
            ['15j', 'Joint fundraising committee contribution (15j)'],
            ['22y', 'Refund (22y)'],
            ['22z', 'Contribution refund to a candidate or committee (22z)'],
            ['24a', 'Independent expenditure against candidate (24a)'],
            ['24c', 'Coordinated expenditure (24c)'],
            ['24e', 'Independent expenditure for candidate (24e)'],
            ['24f', 'Communication cost for candidate (24f)'],
            ['24g', 'Transfer to affiliated committee (24g)'],
            ['24k', 'Direct contribution (24k)'],
            ['24n', 'Communication cost against candidate (24n)'],
            ['24r', 'Election recount disbursement (24r)'],
            ['24z', 'In kind contribution (24z)'],
            ['10', '"Soft" money or Levin fund (10)'],
            ['11', 'Tribal contribution (11)']
        ]
    });

    TD.DataFilter.init();

});