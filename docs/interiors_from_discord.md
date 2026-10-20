# Building interiors from the Discord server

Every building's inside follows the Discord server's structure, as the hospital and the National Treasury already do.
The full structure is below, copied from the bot's permission preview. It is the source of truth: do not invent rooms
or change who may enter them.

## How to read it

- **A category is a building** (or one institution's part of a building), for example "🚓 POLICE" is the police
  headquarters. Categories repeated per state (for example a state government or a state bank) become the same building
  design in each of the four towns, with that state's name.
- **A channel is a room**, for example `#evidence-room`, `#jail`, `#igp-office`. Name the room's sign after the channel,
  in plain words ("Evidence Room").
- **"View + send"** means these posts may **enter and use** the room: its desks, terminals and counters.
- **"Read-only"** means these may **enter and look** (a public hall, a notice board, a waiting area) but not use staff desks.
- **@everyone** means anyone, including visitors. **Deltans** means every registered citizen. **Asylum** means people
  who are still applying for citizenship.
- **Chief Administrator** is the game's Chief Admin, who may enter everywhere.
- Post names (Comptroller-General, Doctor, Police Officer and so on) are the game's government posts. A person may enter
  if any post they hold is listed.
- **Clock in** in the room that is the post's own office or staff room (for example a Police Officer in
  `#police-operations`, the Inspector-General in `#igp-office`).
- Categories that are only announcements or chat with no place in the city (for example "📰 NATIONAL MEDIA") become a
  **notice board** in a fitting building rather than a building of their own; list any you are unsure of and ask.
- Already built, leave as they are: the hospital, the banks, Immigration, the government buildings and the National
  Treasury. Check them against this list and report any room that is missing.

## Categories in the server (67)

- ADMINISTRATION
- 📰 NATIONAL MEDIA
- 🛬 ARRIVALS & REGISTRATION
- 🛂 IMMIGRATION AUTHORITY
- 🏙️ASABA — CAPITAL
- ASABA STATE GOVERNMENT
- 🏦 NATIONAL TREASURY & BANKING
- CRESTFIELD BANK 💰
- 🏙️ ASABA LIFESTYLE
- 🏥NATIONAL SPECIALIST HOSPITAL
- 🚓POLICE FORCE HEADQUARTERS
- ⚡ NATIONAL PUBLIC UTILITIES
- ⚖️ THE SUPREME COURT
- ASABA HOUSING DEVELOPMENT🏠
- 🇩🇨 ASABA HOUSING & HOSPITALITY
- 🌾MINISTRY OF AGRICULTURE & RESOURCES
- 🎓CAMBRIDGE UNIVERSITY
- 🏰 PRESIDENCY
- 🏛️ FEDERAL COUNCIL
- 🚦 NATIONAL TRANSPORT AUTHORITY
- 💼 MINISTRY OF TRADE & COMMERCE
- 🏺NATIONAL CULTURE & HERITAGE BUREAU
- 📊NATIONAL BUREAU OF STATISTICS
- 🌍 FOREIGN AFFAIRS
- 🌊WARRI
- WARRI STATE GOVERNMENT
- EASTWAY BANK💰
- 🌊 WARRI LIFESTYLE
- WARRI STATE HOSPITAL⚕️
- WARRI PUBLIC UTILITIES ⚡
- WARRI POLICE COMMAND👮
- 🧑‍⚖️ WARRI STATE HIGH COURT
- WARRI HOUSING DEVELOPMENT🏠
- 🇩🇨 WARRI HOUSING & HOSPITALITY
- STATE MINISTRY OF TRANSPORT WARRI
- NATURAL RESOURCES OFFICE🌳
- WARRI STATE UNIVERSITY🏫
- 🌴OZORO
- OZORO STATE GOVERNMENT
- TRUSTMARK BANK💰
- 🌴 OZORO LIFESTYLE
- OZORO STATE HOSPITAL⚕️
- OZORO PUBLIC UTILITIES⚡
- OZORO POLICE COMMAND👮
- 🧑‍⚖️ OZORO STATE HIGH COURT
- OZORO HOUSING DEVELOPMENT🏠
- 🇩🇨 OZORO HOUSING & HOSPITALITY
- STATE MINISTRY OF TRANSPORT OZORO
- FOOD PRODUCTION & REGULATION🚜
- OZORO STATE UNIVERSITY🏫
- 🏘️AGBOR
- AGBOR STATE GOVERNMENT
- GRANDVIEW BANK💰
- 🏘️ AGBOR LIFESTYLE
- AGBOR STATE HOSPITAL⚕️
- AGBOR PUBLIC UTILITIES⚡
- AGBOR POLICE COMMAND👮
- 🧑‍⚖️ AGBOR STATE HIGH COURT
- AGBOR HOUSING DEVELOPMENT🏠
- 🇩🇨 AGBOR HOUSING & HOSPITALITY
- STATE MINISTRY OF TRANSPORT AGBOR
- AGRICULTURAL SERVICES AUTHORITY🚜
- AGBOR STATE UNIVERSITY🏫
- ROLES THE RULES MENTION THAT DO NOT EXIST (skipped)
- CHANNELS WITH NO RULE (left exactly as they are)
- RULES WAITING FOR A CHANNEL THAT DOES NOT EXIST YET
- CATEGORIES NOT MANAGED (left exactly as they are)

## The full structure

```
======================================================================
ADMINISTRATION
======================================================================
#admin-only
    View + send: Chief Administrator
#safety-info
    View + send: Chief Administrator

======================================================================
📰 NATIONAL MEDIA
======================================================================
#announcements
    View + send: President | Vice President | Chief of Staff | Minister of Information, Culture & Heritage
    Read-only: Deltans
#national-news
    View + send: President | Vice President | Chief of Staff | Minister of Information, Culture & Heritage
    Read-only: Deltans

======================================================================
🛬 ARRIVALS & REGISTRATION
======================================================================
#city-regulations
    View + send: Chief Administrator
    Read-only: Deltans | Asylum
#delta-international-airport
    View + send: Chief Administrator
    Read-only: Deltans | Asylum
#arrival-station
    View + send: @everyone
#citizenship-application
    View + send: Comptroller-General | Deputy Comptroller-General | Citizenship Registrar (Federal) | Immigration Services Agent (Federal) | Asylum
#travel-services
    View + send: Comptroller-General | Deputy Comptroller-General | Immigration Services Agent (Federal) | State Comptroller

======================================================================
🛂 IMMIGRATION AUTHORITY
======================================================================
#immigration-log
    View + send: Comptroller-General | Deputy Comptroller-General | Immigration Services Agent (Federal) | Citizenship Registrar (Federal) | Border Protection Officer (Federal)
#citizens-database
    View + send: Comptroller-General | Deputy Comptroller-General | Immigration Services Agent (Federal) | Citizenship Registrar (Federal)
#birth-certificate
    View + send: Comptroller-General | Deputy Comptroller-General | Immigration Services Agent (Federal) | Citizenship Registrar (Federal)
    Read-only: Deltans
#passport-delivery
    View + send: Comptroller-General | Deputy Comptroller-General | Immigration Services Agent (Federal) | Citizenship Registrar (Federal)
    Read-only: Deltans
#deputy-comptroller-general-office
    View + send: Comptroller-General | Deputy Comptroller-General | Immigration Services Agent (Federal) | Citizenship Registrar (Federal) | Border Protection Officer (Federal)
    Send, no history: Immigration Visitor
#comptroller-general-office
    View + send: Comptroller-General | Deputy Comptroller-General
    Send, no history: Immigration Visitor

======================================================================
🏙️ASABA — CAPITAL
======================================================================
#asb-border-desk
    View + send: Citizen of Asaba | Visitor Asaba | Border Protection Officer | Immigration Services Agent | Citizenship Registrar | State Comptroller
#residence-permit
    View + send: Immigration Services Agent | Citizenship Registrar | State Comptroller
    Read-only: Citizen of Asaba
#entry-and-exit
    View + send: Immigration Services Agent | Citizenship Registrar | State Comptroller
#immigration-office
    View + send: Border Protection Officer | Immigration Services Agent | Citizenship Registrar | State Comptroller
    Send, no history: Immigration Visitor (citizen/visitor of Asaba)
#state-comptroller-office
    View + send: State Comptroller (citizen of Asaba)
    Send, no history: Immigration Visitor (citizen/visitor of Asaba)

======================================================================
ASABA STATE GOVERNMENT
======================================================================
#state-notice
    View + send: Governor (citizen of Asaba) | Secretary to the State Government (citizen of Asaba)
    Read-only: Citizen of Asaba | Visitor Asaba
#state-council
    View + send: Governor (citizen of Asaba) | Secretary to the State Government (citizen of Asaba) | State Comptroller (citizen of Asaba) | State Banking Director (citizen of Asaba) | Director of Housing & Urban Development (citizen of Asaba) | Director of Infrastructure (citizen of Asaba) | Medical Director (citizen of Asaba) | Director of Transport (citizen of Asaba) | Director of Agriculture & Natural Resources (citizen of Asaba) | Vice Chancellor (citizen of Asaba) | Chief Judge | Inspector-General of Police & Security
#ssg-office
    View + send: Governor (citizen of Asaba) | Secretary to the State Government (citizen of Asaba)
    Send, no history: Government Visitor
#governor-office
    View + send: Governor (citizen of Asaba) | Secretary to the State Government (citizen of Asaba)

======================================================================
🏦 NATIONAL TREASURY & BANKING
======================================================================
#banks-escalations
    View + send: Bank Governor | Minister of Finance | State Banking Director | Governor | Secretary to the State Government
#reserve-office
    View + send: Bank Governor | Minister of Finance
#delta-central-bank
    View + send: Bank Governor | Minister of Finance | Chief of Staff | Vice President | President

======================================================================
CRESTFIELD BANK 💰
======================================================================
#service-hall
    View + send: Citizen of Asaba | Visitor Asaba | Customer Service Officer | Account Officer | Audit Officer | Bank Manager | State Banking Director
#accounts
    View + send: Customer Service Officer | Account Officer | Audit Officer | Bank Manager | State Banking Director
#auditing-room
    View + send: Audit Officer | State Banking Director
#managers-office
    View + send: Customer Service Officer | Account Officer | Bank Manager | State Banking Director
    Send, no history: Bank Visitor
    Can see the channel: Audit Officer
#bank-directors-office
    View + send: Bank Manager | State Banking Director
    Send, no history: Bank Visitor
#deposit
    View + send: Customer Service Officer | Account Officer | Audit Officer | Bank Manager | State Banking Director
#atm-services💳
    View + send: Citizen of Asaba | Visitor Asaba | Customer Service Officer | Account Officer | Audit Officer | Bank Manager | State Banking Director

======================================================================
🏙️ ASABA LIFESTYLE
======================================================================
#as-lobby
    View + send: Citizen of Asaba | Visitor Asaba
#clubhouse
    View + send: Citizen of Asaba | Visitor Asaba
#Clubhouse
    View + send: Citizen of Asaba | Visitor Asaba
#Chapel
    View + send: Citizen of Asaba | Visitor Asaba

======================================================================
🏥NATIONAL SPECIALIST HOSPITAL
======================================================================
#hospital-lobby
    View + send: Citizen of Asaba | Visitor Asaba | Patient Services Staff | Dentist | Laboratory Scientist | Pharmacist | Nurse | Doctor | Surgeon | Medical Director | Minister of Health
#nurses-station
    View + send: Hospitalized (citizen/visitor of Asaba) | Outpatient | Patient Services Staff | Dentist | Laboratory Scientist | Pharmacist | Nurse | Doctor | Surgeon | Medical Director
#consultation
    View + send: Patient Services Staff | Dentist | Laboratory Scientist | Pharmacist | Nurse | Doctor | Surgeon | Medical Director
    Send, no history: Outpatient
#health-records
    View + send: Doctor | Nurse | Surgeon | Patient Services Staff | Medical Director
#male-ward
    View + send: Hospitalized (citizen/visitor of Asaba) | Patient Services Staff | Dentist | Laboratory Scientist | Pharmacist | Nurse | Doctor | Surgeon | Medical Director
#female-ward
    View + send: Hospitalized (citizen/visitor of Asaba) | Patient Services Staff | Dentist | Laboratory Scientist | Pharmacist | Nurse | Doctor | Surgeon | Medical Director
#private-ward
    View + send: Hospitalized (citizen/visitor of Asaba) | Patient Services Staff | Dentist | Laboratory Scientist | Pharmacist | Nurse | Doctor | Surgeon | Medical Director
#dental-room
    View + send: Dental Patient | Patient Services Staff | Dentist | Nurse | Doctor | Medical Director
#operating-theatre
    View + send: In-Surgery | Surgeon | Doctor | Nurse | Medical Director
#pharmacy
    View + send: Patient Services Staff | Pharmacist | Nurse | Doctor | Surgeon | Medical Director
#laboratory
    View + send: Laboratory Scientist | Nurse | Doctor | Surgeon | Medical Director
#medical-staff-office
    View + send: Patient Services Staff | Dentist | Laboratory Scientist | Pharmacist | Nurse | Doctor | Surgeon | Medical Director
#medical-directors-office
    View + send: Medical Director

======================================================================
🚓POLICE FORCE HEADQUARTERS
======================================================================
#complaints-office
    View + send: Citizen of Asaba | Visitor Asaba | Police Rookie | Swat | Sergeant | Security Analyst | Superintendent | Detective | Inspector-General of Police & Security
#investigation-and-records
    View + send: Cuffed | Swat | Sergeant | Security Analyst | Superintendent | Detective | Inspector-General of Police & Security
#evidence-room
    View + send + add/remove people: Superintendent | Detective | Inspector-General of Police & Security
    People added by hand are kept when this script runs
#jail
    View + send: Jail | Police Visitor | Sergeant | Superintendent | Detective | Inspector-General of Police & Security
#police-operations
    View + send: Police Rookie | Swat | Sergeant | Security Analyst | Superintendent | Detective | Inspector-General of Police & Security
    Send, no history: Police Visitor
#security-intelligence
    View + send: Security Analyst | Superintendent | Inspector-General of Police & Security
    Send, no history: Police Visitor
#igp-office
    View + send: Inspector-General of Police & Security
    Send, no history: Police Visitor

======================================================================
⚡ NATIONAL PUBLIC UTILITIES
======================================================================
#utilities-front-desk
    View + send: Citizen of Asaba | Director of Infrastructure | Electrical Officer | Utility Officer | Infrastructure Officer
#power-services
    View + send: Director of Infrastructure | Electrical Officer | Utility Officer | Infrastructure Officer
#water-services
    View + send: Director of Infrastructure | Electrical Officer | Utility Officer | Infrastructure Officer
#utilities-office
    View + send: Director of Infrastructure | Electrical Officer | Utility Officer | Infrastructure Officer | Electrician | Plumber | Utility Visitor
#directors-office
    View + send: Director of Infrastructure
    Send, no history: Utility Visitor
#utility-outage-report
    View + send: Director of Infrastructure | Electrical Officer | Utility Officer | Infrastructure Officer
    Read-only: Citizen of Asaba | Visitor Asaba
#power-generation
    View + send: Electrical Officer | Director of Infrastructure | Minister of Housing & Infrastructure
#water-connections
    View + send: Utility Officer | Director of Infrastructure | Minister of Housing & Infrastructure

======================================================================
⚖️ THE SUPREME COURT
======================================================================
#clerk-office
    View + send: Court Clerk | Chief Registrar | Chief Judge
#evidence
    View + send + add/remove people: Chief Judge
    People added by hand are kept when this script runs
#court-services
    View + send: Citizen of Asaba | Visitor Asaba | Court Clerk | Chief Registrar | Chief Judge
#chief-judge-office
    View + send: Chief Judge
#court-room
    Runs the voice room: Chief Judge | Attorney-General

======================================================================
ASABA HOUSING DEVELOPMENT🏠
======================================================================
#reminders
    View + send: Urban Development Officer | Land & Property Officer | Housing Administrator | Director of Housing & Urban Development
    Read-only: Citizen of Asaba | Visitor Asaba
#land-property-listing
    View + send: Director of Housing & Urban Development | Housing Administrator | Minister of Housing & Infrastructure
    Read-only: Citizen of Asaba
#deed-receipt
    View + send: Urban Development Officer | Land & Property Officer | Housing Administrator | Director of Housing & Urban Development
    Read-only: Citizen of Asaba
#rental-desk
    View + send: Citizen of Asaba | Visitor Asaba | Urban Development Officer | Land & Property Officer | Housing Administrator | Director of Housing & Urban Development
#housing-office
    View + send: Urban Development Officer | Land & Property Officer | Housing Administrator | Director of Housing & Urban Development
#director-housing-office
    View + send: Housing Administrator | Director of Housing & Urban Development

======================================================================
🇩🇨 ASABA HOUSING & HOSPITALITY
======================================================================
#gra
    View + send: GRA-Asb Resident
    Can see the channel: Director of Housing & Urban Development | Housing Administrator | Land & Property Officer | Urban Development Officer
#best-gra-hotel
    View + send: Best GRA Hotel
    Can see the channel: Director of Housing & Urban Development | Housing Administrator
#township
    View + send: Township-Asb Resident
    Can see the channel: Director of Housing & Urban Development | Housing Administrator | Land & Property Officer | Urban Development Officer
#asaba-guest-house
    View + send: Asaba Guest House
    Can see the channel: Director of Housing & Urban Development | Housing Administrator
#quarters
    View + send: Citizen of Asaba

======================================================================
🌾MINISTRY OF AGRICULTURE & RESOURCES
======================================================================
#general-services
    View + send: Citizen of Asaba | Visitor Asaba | Farmers | Drillers | Agriculture & Resource Officer | Drilling Inspector | Director of Agriculture & Natural Resources
#animal-and-food-production
    View + send: Farmers | Drillers | Agriculture & Resource Officer | Drilling Inspector | Director of Agriculture & Natural Resources
#oil-sale-and-distribution
    View + send: Drillers | Agriculture & Resource Officer | Drilling Inspector | Director of Agriculture & Natural Resources
#general-inspection
    View + send: Agriculture & Resource Officer | Drilling Inspector | Director of Agriculture & Natural Resources
#directors-office
    View + send: Director of Agriculture & Natural Resources
#farm-land
    View + send: Farmers | Agriculture & Resource Officer | Director of Agriculture & Natural Resources
#animal-pen
    View + send: Farmers | Agriculture & Resource Officer | Director of Agriculture & Natural Resources
#oil-rig
    View + send: Drillers | Drilling Inspector | Director of Agriculture & Natural Resources

======================================================================
🎓CAMBRIDGE UNIVERSITY
======================================================================
#lecture-halls
    View + send: Student | Lecturer | Professor | Dean of Students' Affairs | Vice Chancellor
#admission-and-information
    View + send: Citizen of Asaba | Visitor Asaba | Student | Lecturer | Professor | Dean of Students' Affairs | Vice Chancellor
#academic-office
    View + send: Student | Lecturer | Professor | Dean of Students' Affairs | Vice Chancellor
#examination-office
    View + send: Student | Lecturer | Professor | Dean of Students' Affairs | Vice Chancellor
#library
    View + send: Citizen of Asaba | Student | Lecturer | Professor | Dean of Students' Affairs | Vice Chancellor
#lecturers-office
    View + send: Lecturer | Professor | Dean of Students' Affairs | Vice Chancellor
#professor-office
    View + send: Professor | Dean of Students' Affairs | Vice Chancellor
#vice-chancellors-office
    View + send: Dean of Students' Affairs | Vice Chancellor | Secretary to the State Government (citizen of Asaba)

======================================================================
🏰 PRESIDENCY
======================================================================
#president-penthouse
    View + send: President | Vice President | President Villa Visitor
    May create private threads: President
#vice-president-penthouse
    View + send: President | Vice President | President Villa Visitor
    May create private threads: Vice President
#visitor-villa-1
    View + send: President | Vice President | President Villa Visitor
#visitor-villa-2
    View + send: President | Vice President | President Villa Visitor

======================================================================
🏛️ FEDERAL COUNCIL
======================================================================
#🏛️president-office
    View + send: President | Vice President
#🤝vice-president-office
    View + send: President | Vice President | Chief of Staff
#🗂️chief-of-staff
    View + send: President | Vice President | Chief of Staff | Federal Council
#💰ministry-of-finance
    View + send: Minister of Finance | Federal Council
#🏥minister-of-health
    View + send: Minister of Health | Federal Council
#⚖️attorney-general-office
    View + send: Attorney-General | Federal Council
#🏠⚡minister-of-housing-infrastructure
    View + send: Minister of Housing & Infrastructure | Federal Council
#🎓minister-of-education
    View + send: Minister of Education | Federal Council
#🌾minister-of-agriculture-and-resources
    View + send: Minister of Agriculture & Natural Resources | Federal Council
#🚦minister-of-transportation
    View + send: Minister of Transport | Federal Council
#🏺minister-of-information-culture-heritage
    View + send: Minister of Information, Culture & Heritage | Federal Council
#federal-chambers
    View + send: President | Vice President | Chief of Staff | Minister of Trade & Commerce | Minister of Foreign Affairs | Minister of Housing & Infrastructure | Minister of Finance | Minister of Health | Minister of Education | Minister of Transport | Minister of Agriculture & Natural Resources | Minister of Information, Culture & Heritage | Minister of National Statistics | Governor | Secretary to the State Government | Bank Governor | Comptroller-General | Deputy Comptroller-General | Inspector-General of Police & Security | Attorney-General

======================================================================
🚦 NATIONAL TRANSPORT AUTHORITY
======================================================================
#public-enquiries
    View + send: Citizen of Asaba | Visitor Asaba | Driver | Vehicle Licensing Officer | Transport & Safety Inspector | Director of Transport
#transport-services
    View + send: Vehicle Licensing Officer | Transport & Safety Inspector | Director of Transport
    Read-only: Citizen of Asaba | Visitor Asaba
#road-transport
    View + send: Driver | Vehicle Licensing Officer | Transport & Safety Inspector | Director of Transport
#transport-inspection
    View + send: Transport & Safety Inspector | Director of Transport | Minister of Transport
#licensing-office
    View + send: Vehicle Licensing Officer | Director of Transport
#staffs-office
    View + send: Driver | Vehicle Licensing Officer | Transport & Safety Inspector | Director of Transport
#directors-office
    View + send: Director of Transport
#engineering-services
    View + send: Minister of Transport | Transport & Safety Inspector | Director of Transport
#flight-track
    View + send: Minister of Transport

======================================================================
💼 MINISTRY OF TRADE & COMMERCE
======================================================================
#business-enquiries
    View + send: Deltans | Business Officer | Trade & Commerce Officer | Minister of Trade & Commerce
#trade-services
    View + send: Business Officer | Trade & Commerce Officer | Minister of Trade & Commerce
#import--export-office
    View + send: Business Officer | Trade & Commerce Officer | Minister of Trade & Commerce
#trade-directorate
    View + send: Trade & Commerce Officer | Minister of Trade & Commerce
#ministers-office
    View + send: Minister of Trade & Commerce

======================================================================
🏺NATIONAL CULTURE & HERITAGE BUREAU
======================================================================
#cultural-heritage-enquiry
    View + send: Deltans | Cultural Officer | Heritage Officer | Minister of Information, Culture & Heritage
#sites
    View + send: Cultural Officer | Heritage Officer | Minister of Information, Culture & Heritage
#permits
    View + send: Cultural Officer | Heritage Officer | Minister of Information, Culture & Heritage
#events-office
    View + send: Cultural Officer | Heritage Officer | Minister of Information, Culture & Heritage
#minister-of-culture-heritage-office
    View + send: Minister of Information, Culture & Heritage

======================================================================
📊NATIONAL BUREAU OF STATISTICS
======================================================================
#public-data-services
    View + send: Deltans | Survey Officer | Data Officer | Statistician | Minister of National Statistics
#statistical-services
    View + send: Statistician | Minister of National Statistics
#records-office
    View + send: Survey Officer | Data Officer | Statistician | Minister of National Statistics
#census-and-survey
    View + send: Survey Officer | Statistician | Minister of National Statistics
#data-analysis
    View + send: Data Officer | Statistician | Minister of National Statistics
#minister-of-national-statistics-office
    View + send: Minister of National Statistics

======================================================================
🌍 FOREIGN AFFAIRS
======================================================================
#foreign-affairs-office
    View + send: Citizen of Asaba | Visitor Asaba | Consular Officer | Diplomat | Foreign Affairs Officer | Minister of Foreign Affairs
#consular-services
    View + send: Consular Officer | Foreign Affairs Officer | Minister of Foreign Affairs
#diplomatic-services
    View + send: Diplomat | Foreign Affairs Officer | Minister of Foreign Affairs
#embassies-and-missions
    View + send: Foreign Affairs Officer | Minister of Foreign Affairs
#treaties-and-agreements
    View + send: Consular Officer | Diplomat | Foreign Affairs Officer | Minister of Foreign Affairs
#minister-of-foreign-affairs-office
    View + send: Minister of Foreign Affairs

======================================================================
🌊WARRI
======================================================================
#wri-border-desk
    View + send: Citizen of Warri | Visitor Warri | Border Protection Officer | Immigration Services Agent | Citizenship Registrar | State Comptroller
#residence-permit
    View + send: Immigration Services Agent | Citizenship Registrar | State Comptroller
    Read-only: Citizen of Warri
#warri-immigration-log
    View + send: Border Protection Officer | Immigration Services Agent | Citizenship Registrar | State Comptroller
#entry-and-exit
    View + send: Immigration Services Agent | Citizenship Registrar | State Comptroller
#immigration-office
    View + send: Border Protection Officer | Immigration Services Agent | Citizenship Registrar | State Comptroller
    Send, no history: Immigration Visitor (citizen/visitor of Warri)
#state-comptroller-office
    View + send: State Comptroller (citizen of Warri)
    Send, no history: Immigration Visitor (citizen/visitor of Warri)

======================================================================
WARRI STATE GOVERNMENT
======================================================================
#state-notice
    View + send: Governor (citizen of Warri) | Secretary to the State Government (citizen of Warri)
    Read-only: Citizen of Warri | Visitor Warri
#state-council
    View + send: Governor (citizen of Warri) | Secretary to the State Government (citizen of Warri) | State Comptroller (citizen of Warri) | State Banking Director (citizen of Warri) | Director of Housing & Urban Development (citizen of Warri) | Director of Infrastructure (citizen of Warri) | Medical Director (citizen of Warri) | Director of Transport (citizen of Warri) | Director of Agriculture & Natural Resources (citizen of Warri) | Vice Chancellor (citizen of Warri) | State Police & Security Commissioner (citizen of Warri) | High Court Judge (citizen of Warri)
#ssg-office
    View + send: Governor (citizen of Warri) | Secretary to the State Government (citizen of Warri)
    Send, no history: Government Visitor
#governor-office
    View + send: Governor (citizen of Warri) | Secretary to the State Government (citizen of Warri)

======================================================================
EASTWAY BANK💰
======================================================================
#service-hall
    View + send: Citizen of Warri | Visitor Warri | Customer Service Officer | Account Officer | Audit Officer | Bank Manager | State Banking Director
#accounts
    View + send: Customer Service Officer | Account Officer | Audit Officer | Bank Manager | State Banking Director
#auditing-room
    View + send: Audit Officer | State Banking Director
#managers-office
    View + send: Customer Service Officer | Account Officer | Bank Manager | State Banking Director
    Send, no history: Bank Visitor
    Can see the channel: Audit Officer
#bank-directors-office
    View + send: Bank Manager | State Banking Director
    Send, no history: Bank Visitor
#deposit
    View + send: Customer Service Officer | Account Officer | Audit Officer | Bank Manager | State Banking Director
#atm-services💳
    View + send: Citizen of Warri | Visitor Warri | Customer Service Officer | Account Officer | Audit Officer | Bank Manager | State Banking Director

======================================================================
🌊 WARRI LIFESTYLE
======================================================================
#wr-lobby
    View + send: Citizen of Warri | Visitor Warri
#clubhouse
    View + send: Citizen of Warri | Visitor Warri
#Clubhouse
    View + send: Citizen of Warri | Visitor Warri
#Chapel
    View + send: Citizen of Warri | Visitor Warri

======================================================================
WARRI STATE HOSPITAL⚕️
======================================================================
#lobby
    View + send: Citizen of Warri | Visitor Warri | Patient Services Staff | Dentist | Laboratory Scientist | Pharmacist | Nurse | Doctor | Surgeon | Medical Director | Minister of Health
#nurses-station
    View + send: Hospitalized (citizen/visitor of Warri) | Outpatient | Patient Services Staff | Dentist | Laboratory Scientist | Pharmacist | Nurse | Doctor | Surgeon | Medical Director
#consultation
    View + send: Patient Services Staff | Dentist | Laboratory Scientist | Pharmacist | Nurse | Doctor | Surgeon | Medical Director
    Send, no history: Outpatient
#health-records
    View + send: Doctor | Nurse | Surgeon | Patient Services Staff | Medical Director
#male-ward
    View + send: Hospitalized (citizen/visitor of Warri) | Patient Services Staff | Dentist | Laboratory Scientist | Pharmacist | Nurse | Doctor | Surgeon | Medical Director
#female-ward
    View + send: Hospitalized (citizen/visitor of Warri) | Patient Services Staff | Dentist | Laboratory Scientist | Pharmacist | Nurse | Doctor | Surgeon | Medical Director
#private-ward
    View + send: Hospitalized (citizen/visitor of Warri) | Patient Services Staff | Dentist | Laboratory Scientist | Pharmacist | Nurse | Doctor | Surgeon | Medical Director
#dental-room
    View + send: Dental Patient | Patient Services Staff | Dentist | Nurse | Doctor | Medical Director
#operating-theatre
    View + send: In-Surgery | Surgeon | Doctor | Nurse | Medical Director
#pharmacy
    View + send: Patient Services Staff | Pharmacist | Nurse | Doctor | Surgeon | Medical Director
#medical-staff-office
    View + send: Patient Services Staff | Dentist | Laboratory Scientist | Pharmacist | Nurse | Doctor | Surgeon | Medical Director
#medical-directors-office
    View + send: Medical Director

======================================================================
WARRI PUBLIC UTILITIES ⚡
======================================================================
#utilities-front-desk
    View + send: Citizen of Warri | Director of Infrastructure | Electrical Officer | Utility Officer | Infrastructure Officer
#water-services
    View + send: Director of Infrastructure | Electrical Officer | Utility Officer | Infrastructure Officer
#power-services
    View + send: Director of Infrastructure | Electrical Officer | Utility Officer | Infrastructure Officer
#utilities-office
    View + send: Director of Infrastructure | Electrical Officer | Utility Officer | Infrastructure Officer | Electrician | Plumber | Utility Visitor
#directors-office
    View + send: Director of Infrastructure
    Send, no history: Utility Visitor

======================================================================
WARRI POLICE COMMAND👮
======================================================================
#complaints-office
    View + send: Citizen of Warri | Visitor Warri | Police Rookie | Swat | Sergeant | Security Analyst | Superintendent | Detective | State Police & Security Commissioner
#investigation-and-records
    View + send: Cuffed | Swat | Sergeant | Security Analyst | Superintendent | Detective | State Police & Security Commissioner
#evidence-room
    View + send + add/remove people: Superintendent | Detective | State Police & Security Commissioner
    People added by hand are kept when this script runs
#jail
    View + send: Jail | Police Visitor | Sergeant | Superintendent | Detective | State Police & Security Commissioner
#police-operations
    View + send: Police Rookie | Swat | Sergeant | Security Analyst | Superintendent | Detective | State Police & Security Commissioner
    Send, no history: Police Visitor
#security-office
    View + send: Security Analyst | Superintendent | State Police & Security Commissioner
    Send, no history: Police Visitor
#commisioner-office
    View + send: Superintendent | State Police & Security Commissioner (citizen of Warri)
    Send, no history: Police Visitor

======================================================================
🧑‍⚖️ WARRI STATE HIGH COURT
======================================================================
#clerk-office
    View + send: Court Clerk | Chief Registrar | High Court Judge (citizen of Warri)
#evidence
    View + send + add/remove people: High Court Judge (citizen of Warri)
    People added by hand are kept when this script runs
#court-services
    View + send: Citizen of Warri | Visitor Warri | Court Clerk | Chief Registrar | High Court Judge (citizen of Warri)
#high-judge-office
    View + send: High Court Judge (citizen of Warri)
#court-room
    Runs the voice room: High Court Judge (citizen of Warri)

======================================================================
WARRI HOUSING DEVELOPMENT🏠
======================================================================
#reminders
    View + send: Urban Development Officer | Land & Property Officer | Housing Administrator | Director of Housing & Urban Development
    Read-only: Citizen of Warri | Visitor Warri
#land-property-listing
    View + send: Director of Housing & Urban Development | Housing Administrator
    Read-only: Citizen of Warri
#deed-receipt
    View + send: Urban Development Officer | Land & Property Officer | Housing Administrator | Director of Housing & Urban Development
    Read-only: Citizen of Warri
#rental-desk
    View + send: Citizen of Warri | Visitor Warri | Urban Development Officer | Land & Property Officer | Housing Administrator | Director of Housing & Urban Development
#housing-office
    View + send: Urban Development Officer | Land & Property Officer | Housing Administrator | Director of Housing & Urban Development
#director-housing-office
    View + send: Housing Administrator | Director of Housing & Urban Development

======================================================================
🇩🇨 WARRI HOUSING & HOSPITALITY
======================================================================
#gra
    View + send: GRA-Wri Resident
    Can see the channel: Director of Housing & Urban Development | Housing Administrator | Land & Property Officer | Urban Development Officer
#bon-hotel-hyatti
    View + send: Bon Hotel Hyatti
    Can see the channel: Director of Housing & Urban Development | Housing Administrator
#township
    View + send: Township-Wri Resident
    Can see the channel: Director of Housing & Urban Development | Housing Administrator | Land & Property Officer | Urban Development Officer
#legacy-suites
    View + send: Legacy Suites
    Can see the channel: Director of Housing & Urban Development | Housing Administrator
#barracks
    View + send: Citizen of Warri

======================================================================
STATE MINISTRY OF TRANSPORT WARRI
======================================================================
#public-enquiries
    View + send: Citizen of Warri | Visitor Warri | Driver | Vehicle Licensing Officer | Transport & Safety Inspector | Director of Transport
#transport-services
    View + send: Vehicle Licensing Officer | Transport & Safety Inspector | Director of Transport
    Read-only: Citizen of Warri | Visitor Warri
#road-transport
    View + send: Driver | Vehicle Licensing Officer | Transport & Safety Inspector | Director of Transport
#transport-inspection
    View + send: Transport & Safety Inspector | Director of Transport
#licensing-office
    View + send: Vehicle Licensing Officer | Director of Transport
#staff-office
    View + send: Driver | Vehicle Licensing Officer | Transport & Safety Inspector | Director of Transport
#directors-office
    View + send: Director of Transport

======================================================================
NATURAL RESOURCES OFFICE🌳
======================================================================
#general-services
    View + send: Citizen of Warri | Visitor Warri | Farmers | Drillers | Agriculture & Resource Officer | Drilling Inspector | Director of Agriculture & Natural Resources
#oil-sale-and-distribution
    View + send: Drillers | Agriculture & Resource Officer | Drilling Inspector | Director of Agriculture & Natural Resources
#crop-production
    View + send: Farmers | Drillers | Agriculture & Resource Officer | Drilling Inspector | Director of Agriculture & Natural Resources
#inspection
    View + send: Agriculture & Resource Officer | Drilling Inspector | Director of Agriculture & Natural Resources
#directors-office
    View + send: Director of Agriculture & Natural Resources
#farm-land
    View + send: Farmers | Agriculture & Resource Officer | Director of Agriculture & Natural Resources
#oil-rig
    View + send: Drillers | Drilling Inspector | Director of Agriculture & Natural Resources

======================================================================
WARRI STATE UNIVERSITY🏫
======================================================================
#lecture-halls
    View + send: Student | Lecturer | Professor | Dean of Students' Affairs | Vice Chancellor
#admission-and-information
    View + send: Citizen of Warri | Visitor Warri | Student | Lecturer | Professor | Dean of Students' Affairs | Vice Chancellor
#academic-office
    View + send: Student | Lecturer | Professor | Dean of Students' Affairs | Vice Chancellor
#examination-office
    View + send: Student | Lecturer | Professor | Dean of Students' Affairs | Vice Chancellor
#library
    View + send: Citizen of Warri | Student | Lecturer | Professor | Dean of Students' Affairs | Vice Chancellor
#lecturers-office
    View + send: Lecturer | Professor | Dean of Students' Affairs | Vice Chancellor
#vice-chancellors-office
    View + send: Dean of Students' Affairs | Vice Chancellor | Secretary to the State Government (citizen of Warri)

======================================================================
🌴OZORO
======================================================================
#ozr-border-desk
    View + send: Citizen of Ozoro | Visitor Ozoro | Border Protection Officer | Immigration Services Agent | Citizenship Registrar | State Comptroller
#residence-permit
    View + send: Immigration Services Agent | Citizenship Registrar | State Comptroller
    Read-only: Citizen of Ozoro
#entry-and-exit
    View + send: Immigration Services Agent | Citizenship Registrar | State Comptroller
#ozoro-immigration-log
    View + send: Border Protection Officer | Immigration Services Agent | Citizenship Registrar | State Comptroller
#immigration-office
    View + send: Border Protection Officer | Immigration Services Agent | Citizenship Registrar | State Comptroller
    Send, no history: Immigration Visitor (citizen/visitor of Ozoro)
#state-comptroller-office
    View + send: State Comptroller (citizen of Ozoro)
    Send, no history: Immigration Visitor (citizen/visitor of Ozoro)

======================================================================
OZORO STATE GOVERNMENT
======================================================================
#state-notice
    View + send: Governor (citizen of Ozoro) | Secretary to the State Government (citizen of Ozoro)
    Read-only: Citizen of Ozoro | Visitor Ozoro
#state-council
    View + send: Governor (citizen of Ozoro) | Secretary to the State Government (citizen of Ozoro) | State Comptroller (citizen of Ozoro) | State Banking Director (citizen of Ozoro) | Director of Housing & Urban Development (citizen of Ozoro) | Director of Infrastructure (citizen of Ozoro) | Medical Director (citizen of Ozoro) | Director of Transport (citizen of Ozoro) | Director of Agriculture & Natural Resources (citizen of Ozoro) | Vice Chancellor (citizen of Ozoro) | State Police & Security Commissioner (citizen of Ozoro) | High Court Judge (citizen of Ozoro)
#ssg-office
    View + send: Governor (citizen of Ozoro) | Secretary to the State Government (citizen of Ozoro)
    Send, no history: Government Visitor
#governor-office
    View + send: Governor (citizen of Ozoro) | Secretary to the State Government (citizen of Ozoro)

======================================================================
TRUSTMARK BANK💰
======================================================================
#service-hall
    View + send: Citizen of Ozoro | Visitor Ozoro | Customer Service Officer | Account Officer | Audit Officer | Bank Manager | State Banking Director
#accounts
    View + send: Customer Service Officer | Account Officer | Audit Officer | Bank Manager | State Banking Director
#auditing-room
    View + send: Audit Officer | State Banking Director
#managers-office
    View + send: Customer Service Officer | Account Officer | Bank Manager | State Banking Director
    Send, no history: Bank Visitor
    Can see the channel: Audit Officer
#bank-directors-office
    View + send: Bank Manager | State Banking Director
    Send, no history: Bank Visitor
#deposit
    View + send: Customer Service Officer | Account Officer | Audit Officer | Bank Manager | State Banking Director
#atm-services💳
    View + send: Citizen of Ozoro | Visitor Ozoro | Customer Service Officer | Account Officer | Audit Officer | Bank Manager | State Banking Director

======================================================================
🌴 OZORO LIFESTYLE
======================================================================
#oz-lobby
    View + send: Citizen of Ozoro | Visitor Ozoro
#clubhouse
    View + send: Citizen of Ozoro | Visitor Ozoro
#Clubhouse
    View + send: Citizen of Ozoro | Visitor Ozoro
#Chapel
    View + send: Citizen of Ozoro | Visitor Ozoro

======================================================================
OZORO STATE HOSPITAL⚕️
======================================================================
#lobby
    View + send: Citizen of Ozoro | Visitor Ozoro | Patient Services Staff | Dentist | Laboratory Scientist | Pharmacist | Nurse | Doctor | Surgeon | Medical Director | Minister of Health
#nurses-station
    View + send: Hospitalized (citizen/visitor of Ozoro) | Outpatient | Patient Services Staff | Dentist | Laboratory Scientist | Pharmacist | Nurse | Doctor | Surgeon | Medical Director
#consultation
    View + send: Patient Services Staff | Dentist | Laboratory Scientist | Pharmacist | Nurse | Doctor | Surgeon | Medical Director
    Send, no history: Outpatient
#health-records
    View + send: Doctor | Nurse | Surgeon | Patient Services Staff | Medical Director
#male-ward
    View + send: Hospitalized (citizen/visitor of Ozoro) | Patient Services Staff | Dentist | Laboratory Scientist | Pharmacist | Nurse | Doctor | Surgeon | Medical Director
#female-ward
    View + send: Hospitalized (citizen/visitor of Ozoro) | Patient Services Staff | Dentist | Laboratory Scientist | Pharmacist | Nurse | Doctor | Surgeon | Medical Director
#private-ward
    View + send: Hospitalized (citizen/visitor of Ozoro) | Patient Services Staff | Dentist | Laboratory Scientist | Pharmacist | Nurse | Doctor | Surgeon | Medical Director
#dental-room
    View + send: Dental Patient | Patient Services Staff | Dentist | Nurse | Doctor | Medical Director
#operating-theatre
    View + send: In-Surgery | Surgeon | Doctor | Nurse | Medical Director
#pharmacy
    View + send: Patient Services Staff | Pharmacist | Nurse | Doctor | Surgeon | Medical Director
#medical-staff-office
    View + send: Patient Services Staff | Dentist | Laboratory Scientist | Pharmacist | Nurse | Doctor | Surgeon | Medical Director
#medical-directors-office
    View + send: Medical Director

======================================================================
OZORO PUBLIC UTILITIES⚡
======================================================================
#utilities-front-desk
    View + send: Citizen of Ozoro | Director of Infrastructure | Electrical Officer | Utility Officer | Infrastructure Officer
#water-services
    View + send: Director of Infrastructure | Electrical Officer | Utility Officer | Infrastructure Officer
#power-services
    View + send: Director of Infrastructure | Electrical Officer | Utility Officer | Infrastructure Officer
#utilities-office
    View + send: Director of Infrastructure | Electrical Officer | Utility Officer | Infrastructure Officer | Electrician | Plumber | Utility Visitor
#directors-office
    View + send: Director of Infrastructure
    Send, no history: Utility Visitor

======================================================================
OZORO POLICE COMMAND👮
======================================================================
#complaints-office
    View + send: Citizen of Ozoro | Visitor Ozoro | Police Rookie | Swat | Sergeant | Security Analyst | Superintendent | Detective | State Police & Security Commissioner
#investigation-and-records
    View + send: Cuffed | Swat | Sergeant | Security Analyst | Superintendent | Detective | State Police & Security Commissioner
#evidence-room
    View + send + add/remove people: Superintendent | Detective | State Police & Security Commissioner
    People added by hand are kept when this script runs
#jail
    View + send: Jail | Police Visitor | Sergeant | Superintendent | Detective | State Police & Security Commissioner
#police-operations
    View + send: Police Rookie | Swat | Sergeant | Security Analyst | Superintendent | Detective | State Police & Security Commissioner
    Send, no history: Police Visitor
#security-office
    View + send: Security Analyst | Superintendent | State Police & Security Commissioner
    Send, no history: Police Visitor
#commisioner-office
    View + send: Superintendent | State Police & Security Commissioner (citizen of Ozoro)
    Send, no history: Police Visitor

======================================================================
🧑‍⚖️ OZORO STATE HIGH COURT
======================================================================
#clerk-office
    View + send: Court Clerk | Chief Registrar | High Court Judge (citizen of Ozoro)
#evidence
    View + send + add/remove people: High Court Judge (citizen of Ozoro)
    People added by hand are kept when this script runs
#court-services
    View + send: Citizen of Ozoro | Visitor Ozoro | Court Clerk | Chief Registrar | High Court Judge (citizen of Ozoro)
#high-judge-office
    View + send: High Court Judge (citizen of Ozoro)
#court-room
    Runs the voice room: High Court Judge (citizen of Ozoro)

======================================================================
OZORO HOUSING DEVELOPMENT🏠
======================================================================
#reminders
    View + send: Urban Development Officer | Land & Property Officer | Housing Administrator | Director of Housing & Urban Development
    Read-only: Citizen of Ozoro | Visitor Ozoro
#land-property-listing
    View + send: Director of Housing & Urban Development | Housing Administrator
    Read-only: Citizen of Ozoro
#deed-receipt
    View + send: Urban Development Officer | Land & Property Officer | Housing Administrator | Director of Housing & Urban Development
    Read-only: Citizen of Ozoro
#rental-desk
    View + send: Citizen of Ozoro | Visitor Ozoro | Urban Development Officer | Land & Property Officer | Housing Administrator | Director of Housing & Urban Development
#housing-office
    View + send: Urban Development Officer | Land & Property Officer | Housing Administrator | Director of Housing & Urban Development
#director-housing-office
    View + send: Housing Administrator | Director of Housing & Urban Development

======================================================================
🇩🇨 OZORO HOUSING & HOSPITALITY
======================================================================
#estate
    View + send: Estate-Ozr Resident
    Can see the channel: Director of Housing & Urban Development | Housing Administrator | Land & Property Officer | Urban Development Officer
#ozoro-presidential-hotel
    View + send: Ozoro Presidential Hotel
    Can see the channel: Director of Housing & Urban Development | Housing Administrator
#township
    View + send: Township-Ozr Resident
    Can see the channel: Director of Housing & Urban Development | Housing Administrator | Land & Property Officer | Urban Development Officer
#okay-hotels
    View + send: okay-hotels
    Can see the channel: Director of Housing & Urban Development | Housing Administrator
#old-quarters
    View + send: Citizen of Ozoro

======================================================================
STATE MINISTRY OF TRANSPORT OZORO
======================================================================
#public-enquiries
    View + send: Citizen of Ozoro | Visitor Ozoro | Driver | Vehicle Licensing Officer | Transport & Safety Inspector | Director of Transport
#transport-services
    View + send: Vehicle Licensing Officer | Transport & Safety Inspector | Director of Transport
    Read-only: Citizen of Ozoro | Visitor Ozoro
#road-transport
    View + send: Driver | Vehicle Licensing Officer | Transport & Safety Inspector | Director of Transport
#transport-inspection
    View + send: Transport & Safety Inspector | Director of Transport
#licensing-office
    View + send: Vehicle Licensing Officer | Director of Transport
#staff-office
    View + send: Driver | Vehicle Licensing Officer | Transport & Safety Inspector | Director of Transport
#directors-office
    View + send: Director of Transport

======================================================================
FOOD PRODUCTION & REGULATION🚜
======================================================================
#general-services
    View + send: Citizen of Ozoro | Visitor Ozoro | Farmers | Drillers | Agriculture & Resource Officer | Drilling Inspector | Director of Agriculture & Natural Resources
#crop-and-animal-production
    View + send: Farmers | Drillers | Agriculture & Resource Officer | Drilling Inspector | Director of Agriculture & Natural Resources
#inspection
    View + send: Agriculture & Resource Officer | Drilling Inspector | Director of Agriculture & Natural Resources
#directors-office
    View + send: Director of Agriculture & Natural Resources
#farm-land
    View + send: Farmers | Agriculture & Resource Officer | Director of Agriculture & Natural Resources
#animal-pen
    View + send: Farmers | Agriculture & Resource Officer | Director of Agriculture & Natural Resources

======================================================================
OZORO STATE UNIVERSITY🏫
======================================================================
#lecture-halls
    View + send: Student | Lecturer | Professor | Dean of Students' Affairs | Vice Chancellor
#admission-and-information
    View + send: Citizen of Ozoro | Visitor Ozoro | Student | Lecturer | Professor | Dean of Students' Affairs | Vice Chancellor
#academic-office
    View + send: Student | Lecturer | Professor | Dean of Students' Affairs | Vice Chancellor
#examination-office
    View + send: Student | Lecturer | Professor | Dean of Students' Affairs | Vice Chancellor
#library
    View + send: Citizen of Ozoro | Student | Lecturer | Professor | Dean of Students' Affairs | Vice Chancellor
#lecturers-office
    View + send: Lecturer | Professor | Dean of Students' Affairs | Vice Chancellor
#vice-chancellors-office
    View + send: Dean of Students' Affairs | Vice Chancellor | Secretary to the State Government (citizen of Ozoro)

======================================================================
🏘️AGBOR
======================================================================
#agb-border-desk
    View + send: Citizen of Agbor | Visitor Agbor | Border Protection Officer | Immigration Services Agent | Citizenship Registrar | State Comptroller
#residence-permit
    View + send: Immigration Services Agent | Citizenship Registrar | State Comptroller
    Read-only: Citizen of Agbor
#entry-and-exit
    View + send: Immigration Services Agent | Citizenship Registrar | State Comptroller
#agbor-immigration-log
    View + send: Border Protection Officer | Immigration Services Agent | Citizenship Registrar | State Comptroller
#immigration-office
    View + send: Border Protection Officer | Immigration Services Agent | Citizenship Registrar | State Comptroller
    Send, no history: Immigration Visitor (citizen/visitor of Agbor)
#state-comptroller-office
    View + send: State Comptroller (citizen of Agbor)
    Send, no history: Immigration Visitor (citizen/visitor of Agbor)

======================================================================
AGBOR STATE GOVERNMENT
======================================================================
#state-notice
    View + send: Governor (citizen of Agbor) | Secretary to the State Government (citizen of Agbor)
    Read-only: Citizen of Agbor | Visitor Agbor
#state-council
    View + send: Governor (citizen of Agbor) | Secretary to the State Government (citizen of Agbor) | State Comptroller (citizen of Agbor) | State Banking Director (citizen of Agbor) | Director of Housing & Urban Development (citizen of Agbor) | Director of Infrastructure (citizen of Agbor) | Medical Director (citizen of Agbor) | Director of Transport (citizen of Agbor) | Director of Agriculture & Natural Resources (citizen of Agbor) | Vice Chancellor (citizen of Agbor) | State Police & Security Commissioner (citizen of Agbor) | High Court Judge (citizen of Agbor)
#ssg-office
    View + send: Governor (citizen of Agbor) | Secretary to the State Government (citizen of Agbor)
    Send, no history: Government Visitor
#governor-office
    View + send: Governor (citizen of Agbor) | Secretary to the State Government (citizen of Agbor)

======================================================================
GRANDVIEW BANK💰
======================================================================
#service-hall
    View + send: Citizen of Agbor | Visitor Agbor | Customer Service Officer | Account Officer | Audit Officer | Bank Manager | State Banking Director
#accounts
    View + send: Customer Service Officer | Account Officer | Audit Officer | Bank Manager | State Banking Director
#auditing-room
    View + send: Audit Officer | State Banking Director
#managers-office
    View + send: Customer Service Officer | Account Officer | Bank Manager | State Banking Director
    Send, no history: Bank Visitor
    Can see the channel: Audit Officer
#bank-directors-office
    View + send: Bank Manager | State Banking Director
    Send, no history: Bank Visitor
#deposit
    View + send: Customer Service Officer | Account Officer | Audit Officer | Bank Manager | State Banking Director
#atm-services💳
    View + send: Citizen of Agbor | Visitor Agbor | Customer Service Officer | Account Officer | Audit Officer | Bank Manager | State Banking Director

======================================================================
🏘️ AGBOR LIFESTYLE
======================================================================
#ag-lobby
    View + send: Citizen of Agbor | Visitor Agbor
#clubhouse
    View + send: Citizen of Agbor | Visitor Agbor
#Clubhouse
    View + send: Citizen of Agbor | Visitor Agbor
#Chapel
    View + send: Citizen of Agbor | Visitor Agbor

======================================================================
AGBOR STATE HOSPITAL⚕️
======================================================================
#lobby
    View + send: Citizen of Agbor | Visitor Agbor | Patient Services Staff | Dentist | Laboratory Scientist | Pharmacist | Nurse | Doctor | Surgeon | Medical Director | Minister of Health
#nurses-station
    View + send: Hospitalized (citizen/visitor of Agbor) | Outpatient | Patient Services Staff | Dentist | Laboratory Scientist | Pharmacist | Nurse | Doctor | Surgeon | Medical Director
#consultation
    View + send: Patient Services Staff | Dentist | Laboratory Scientist | Pharmacist | Nurse | Doctor | Surgeon | Medical Director
    Send, no history: Outpatient
#health-records
    View + send: Doctor | Nurse | Surgeon | Patient Services Staff | Medical Director
#male-ward
    View + send: Hospitalized (citizen/visitor of Agbor) | Patient Services Staff | Dentist | Laboratory Scientist | Pharmacist | Nurse | Doctor | Surgeon | Medical Director
#female-ward
    View + send: Hospitalized (citizen/visitor of Agbor) | Patient Services Staff | Dentist | Laboratory Scientist | Pharmacist | Nurse | Doctor | Surgeon | Medical Director
#private-ward
    View + send: Hospitalized (citizen/visitor of Agbor) | Patient Services Staff | Dentist | Laboratory Scientist | Pharmacist | Nurse | Doctor | Surgeon | Medical Director
#dental-room
    View + send: Dental Patient | Patient Services Staff | Dentist | Nurse | Doctor | Medical Director
#operating-theatre
    View + send: In-Surgery | Surgeon | Doctor | Nurse | Medical Director
#pharmacy
    View + send: Patient Services Staff | Pharmacist | Nurse | Doctor | Surgeon | Medical Director
#medical-staff-office
    View + send: Patient Services Staff | Dentist | Laboratory Scientist | Pharmacist | Nurse | Doctor | Surgeon | Medical Director
#medical-directors-office
    View + send: Medical Director

======================================================================
AGBOR PUBLIC UTILITIES⚡
======================================================================
#utilities-front-desk
    View + send: Citizen of Agbor | Director of Infrastructure | Electrical Officer | Utility Officer | Infrastructure Officer
#water-services
    View + send: Director of Infrastructure | Electrical Officer | Utility Officer | Infrastructure Officer
#power-services
    View + send: Director of Infrastructure | Electrical Officer | Utility Officer | Infrastructure Officer
#utilities-office
    View + send: Director of Infrastructure | Electrical Officer | Utility Officer | Infrastructure Officer | Electrician | Plumber | Utility Visitor
#directors-office
    View + send: Director of Infrastructure
    Send, no history: Utility Visitor

======================================================================
AGBOR POLICE COMMAND👮
======================================================================
#complaints-office
    View + send: Citizen of Agbor | Visitor Agbor | Police Rookie | Swat | Sergeant | Security Analyst | Superintendent | Detective | State Police & Security Commissioner
#investigation-and-records
    View + send: Cuffed | Swat | Sergeant | Security Analyst | Superintendent | Detective | State Police & Security Commissioner
#evidence-room
    View + send + add/remove people: Superintendent | Detective | State Police & Security Commissioner
    People added by hand are kept when this script runs
#jail
    View + send: Jail | Police Visitor | Sergeant | Superintendent | Detective | State Police & Security Commissioner
#police-operations
    View + send: Police Rookie | Swat | Sergeant | Security Analyst | Superintendent | Detective | State Police & Security Commissioner
    Send, no history: Police Visitor
#security-office
    View + send: Security Analyst | Superintendent | State Police & Security Commissioner
    Send, no history: Police Visitor
#commisioner-office
    View + send: Superintendent | State Police & Security Commissioner (citizen of Agbor)
    Send, no history: Police Visitor

======================================================================
🧑‍⚖️ AGBOR STATE HIGH COURT
======================================================================
#clerk-office
    View + send: Court Clerk | Chief Registrar | High Court Judge (citizen of Agbor)
#evidence
    View + send + add/remove people: High Court Judge (citizen of Agbor)
    People added by hand are kept when this script runs
#court-services
    View + send: Citizen of Agbor | Visitor Agbor | Court Clerk | Chief Registrar | High Court Judge (citizen of Agbor)
#high-judge-office
    View + send: High Court Judge (citizen of Agbor)
#court-room
    Runs the voice room: High Court Judge (citizen of Agbor)

======================================================================
AGBOR HOUSING DEVELOPMENT🏠
======================================================================
#reminders
    View + send: Urban Development Officer | Land & Property Officer | Housing Administrator | Director of Housing & Urban Development
    Read-only: Citizen of Agbor | Visitor Agbor
#land-property-listing
    View + send: Director of Housing & Urban Development | Housing Administrator
    Read-only: Citizen of Agbor
#deed-receipt
    View + send: Urban Development Officer | Land & Property Officer | Housing Administrator | Director of Housing & Urban Development
    Read-only: Citizen of Agbor
#rental-desk
    View + send: Citizen of Agbor | Visitor Agbor | Urban Development Officer | Land & Property Officer | Housing Administrator | Director of Housing & Urban Development
#housing-office
    View + send: Urban Development Officer | Land & Property Officer | Housing Administrator | Director of Housing & Urban Development
#director-housing-office
    View + send: Housing Administrator | Director of Housing & Urban Development

======================================================================
🇩🇨 AGBOR HOUSING & HOSPITALITY
======================================================================
#gra
    View + send: GRA-Agb Resident
    Can see the channel: Director of Housing & Urban Development | Housing Administrator | Land & Property Officer | Urban Development Officer
#agbor-palace-hotel
    View + send: Agbor Palace Hotel
    Can see the channel: Director of Housing & Urban Development | Housing Administrator
#township
    View + send: Township-Agb Resident
    Can see the channel: Director of Housing & Urban Development | Housing Administrator | Land & Property Officer | Urban Development Officer
#royal-suites
    View + send: Royal Suites Hotel
    Can see the channel: Director of Housing & Urban Development | Housing Administrator
#boji-quarters
    View + send: Citizen of Agbor

======================================================================
STATE MINISTRY OF TRANSPORT AGBOR
======================================================================
#public-enquiries
    View + send: Citizen of Agbor | Visitor Agbor | Driver | Vehicle Licensing Officer | Transport & Safety Inspector | Director of Transport
#transport-services
    View + send: Vehicle Licensing Officer | Transport & Safety Inspector | Director of Transport
    Read-only: Citizen of Agbor | Visitor Agbor
#road-transport
    View + send: Driver | Vehicle Licensing Officer | Transport & Safety Inspector | Director of Transport
#transport-inspection
    View + send: Transport & Safety Inspector | Director of Transport
#licensing-office
    View + send: Vehicle Licensing Officer | Director of Transport
#staff-office
    View + send: Driver | Vehicle Licensing Officer | Transport & Safety Inspector | Director of Transport
#directors-office
    View + send: Director of Transport

======================================================================
AGRICULTURAL SERVICES AUTHORITY🚜
======================================================================
#general-services
    View + send: Citizen of Agbor | Visitor Agbor | Farmers | Drillers | Agriculture & Resource Officer | Drilling Inspector | Director of Agriculture & Natural Resources
#crop-and-animal-production
    View + send: Farmers | Drillers | Agriculture & Resource Officer | Drilling Inspector | Director of Agriculture & Natural Resources
#inspection
    View + send: Agriculture & Resource Officer | Drilling Inspector | Director of Agriculture & Natural Resources
#directors-office
    View + send: Director of Agriculture & Natural Resources
#farm-land
    View + send: Farmers | Agriculture & Resource Officer | Director of Agriculture & Natural Resources
#animal-pen
    View + send: Farmers | Agriculture & Resource Officer | Director of Agriculture & Natural Resources

======================================================================
AGBOR STATE UNIVERSITY🏫
======================================================================
#lecture-halls
    View + send: Student | Lecturer | Professor | Dean of Students' Affairs | Vice Chancellor
#admission-and-information
    View + send: Citizen of Agbor | Visitor Agbor | Student | Lecturer | Professor | Dean of Students' Affairs | Vice Chancellor
#academic-office
    View + send: Student | Lecturer | Professor | Dean of Students' Affairs | Vice Chancellor
#examination-office
    View + send: Student | Lecturer | Professor | Dean of Students' Affairs | Vice Chancellor
#lecturers-office
    View + send: Lecturer | Professor | Dean of Students' Affairs | Vice Chancellor
#library
    View + send: Citizen of Agbor | Student | Lecturer | Professor | Dean of Students' Affairs | Vice Chancellor
#vice-chancellors-office
    View + send: Dean of Students' Affairs | Vice Chancellor | Secretary to the State Government (citizen of Agbor)

======================================================================
ROLES THE RULES MENTION THAT DO NOT EXIST (skipped)
======================================================================

======================================================================
CHANNELS WITH NO RULE (left exactly as they are)
======================================================================
    ADMINISTRATION / #database
    ADMINISTRATION / #database

======================================================================
RULES WAITING FOR A CHANNEL THAT DOES NOT EXIST YET
======================================================================
    🏙️ASABA — CAPITAL / #*immigration-log
    NATURAL RESOURCES OFFICE🌳 / #animal-pen

======================================================================
CATEGORIES NOT MANAGED (left exactly as they are)
======================================================================
```
