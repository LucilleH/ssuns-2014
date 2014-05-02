DELEGATION_FEE = 90

MAX_NUM_DELEGATES = 100

MIN_NUM_DELEGATES = 0

COUNTRIESFULL = (('AF', u'Afghanistan'), ('AX', u'\xc5land Islands'), ('AL', u'Albania'), ('DZ', u'Algeria'), ('AS', u'American Samoa'), ('AD', u'Andorra'), ('AO', u'Angola'), ('AI', u'Anguilla'), ('AQ', u'Antarctica'), ('AG', u'Antigua and Barbuda'), ('AR', u'Argentina'), ('AM', u'Armenia'), ('AW', u'Aruba'), ('SH', u'Ascension and Tristan Da Cunha Saint Helena'), ('AU', u'Australia'), ('AT', u'Austria'), ('AZ', u'Azerbaijan'), ('BS', u'Bahamas'), ('BH', u'Bahrain'), ('BD', u'Bangladesh'), ('BB', u'Barbados'), ('BY', u'Belarus'), ('BE', u'Belgium'), ('BZ', u'Belize'), ('BJ', u'Benin'), ('BM', u'Bermuda'), ('BT', u'Bhutan'), ('VE', u'Bolivarian Republic of Venezuela'), ('BO', u'Bolivia, Plurinational State of'), ('BQ', u'Bonaire, Sint Eustatius and Saba'), ('BA', u'Bosnia and Herzegovina'), ('BW', u'Botswana'), ('BV', u'Bouvet Island'), ('BR', u'Brazil'), ('IO', u'British Indian Ocean Territory'), ('VG', u'British Virgin Islands'), ('BN', u'Brunei Darussalam'), ('BG', u'Bulgaria'), ('BF', u'Burkina Faso'), ('BI', u'Burundi'), ('KH', u'Cambodia'), ('CM', u'Cameroon'), ('CA', u'Canada'), ('CV', u'Cape Verde'), ('KY', u'Cayman Islands'), ('CF', u'Central African Republic'), ('TD', u'Chad'), ('CL', u'Chile'), ('CN', u'China'), ('CX', u'Christmas Island'), ('CC', u'Cocos (Keeling) Islands'), ('CO', u'Colombia'), ('KM', u'Comoros'), ('CG', u'Congo'), ('CD', u'Congo, The Democratic Republic of the'), ('CK', u'Cook Islands'), ('CR', u'Costa Rica'), ('CI', u"C\xf4te D'ivoire"), ('HR', u'Croatia'), ('CU', u'Cuba'), ('CW', u'Cura\xe7ao'), ('CY', u'Cyprus'), ('CZ', u'Czech Republic'), ('KP', u"Democratic People's Republic of Korea"), ('DK', u'Denmark'), ('DJ', u'Djibouti'), ('DM', u'Dominica'), ('DO', u'Dominican Republic'), ('EC', u'Ecuador'), ('EG', u'Egypt'), ('SV', u'El Salvador'), ('GQ', u'Equatorial Guinea'), ('ER', u'Eritrea'), ('EE', u'Estonia'), ('ET', u'Ethiopia'), ('FK', u'Falkland Islands (Malvinas)'), ('FO', u'Faroe Islands'), ('FM', u'Federated States of Micronesia'), ('FJ', u'Fiji'), ('FI', u'Finland'), ('FR', u'France'), ('GF', u'French Guiana'), ('PF', u'French Polynesia'), ('TF', u'French Southern Territories'), ('GA', u'Gabon'), ('GM', u'Gambia'), ('GE', u'Georgia'), ('DE', u'Germany'), ('GH', u'Ghana'), ('GI', u'Gibraltar'), ('GR', u'Greece'), ('GL', u'Greenland'), ('GD', u'Grenada'), ('GP', u'Guadeloupe'), ('GU', u'Guam'), ('GT', u'Guatemala'), ('GG', u'Guernsey'), ('GN', u'Guinea'), ('GW', u'Guinea-bissau'), ('GY', u'Guyana'), ('HT', u'Haiti'), ('HM', u'Heard Island and McDonald Islands'), ('VA', u'Holy See (Vatican City State)'), ('HN', u'Honduras'), ('HK', u'Hong Kong'), ('HU', u'Hungary'), ('IS', u'Iceland'), ('IN', u'India'), ('ID', u'Indonesia'), ('IR', u'Iran, Islamic Republic of'), ('IQ', u'Iraq'), ('IE', u'Ireland'), ('IR', u'Islamic Republic of Iran'), ('IM', u'Isle of Man'), ('IL', u'Israel'), ('IT', u'Italy'), ('JM', u'Jamaica'), ('JP', u'Japan'), ('JE', u'Jersey'), ('JO', u'Jordan'), ('KZ', u'Kazakhstan'), ('KE', u'Kenya'), ('KI', u'Kiribati'), ('KP', u"Korea, Democratic People's Republic of"), ('KR', u'Korea, Republic of'), ('KW', u'Kuwait'), ('KG', u'Kyrgyzstan'), ('LA', u"Lao People's Democratic Republic"), ('LV', u'Latvia'), ('LB', u'Lebanon'), ('LS', u'Lesotho'), ('LR', u'Liberia'), ('LY', u'Libya'), ('LI', u'Liechtenstein'), ('LT', u'Lithuania'), ('LU', u'Luxembourg'), ('MO', u'Macao'), ('MK', u'Macedonia, The Former Yugoslav Republic of'), ('MG', u'Madagascar'), ('MW', u'Malawi'), ('MY', u'Malaysia'), ('MV', u'Maldives'), ('ML', u'Mali'), ('MT', u'Malta'), ('MH', u'Marshall Islands'), ('MQ', u'Martinique'), ('MR', u'Mauritania'), ('MU', u'Mauritius'), ('YT', u'Mayotte'), ('MX', u'Mexico'), ('FM', u'Micronesia, Federated States of'), ('MD', u'Moldova, Republic of'), ('MC', u'Monaco'), ('MN', u'Mongolia'), ('ME', u'Montenegro'), ('MS', u'Montserrat'), ('MA', u'Morocco'), ('MZ', u'Mozambique'), ('MM', u'Myanmar'), ('NA', u'Namibia'), ('NR', u'Nauru'), ('NP', u'Nepal'), ('NL', u'Netherlands'), ('NC', u'New Caledonia'), ('NZ', u'New Zealand'), ('NI', u'Nicaragua'), ('NE', u'Niger'), ('NG', u'Nigeria'), ('NU', u'Niue'), ('NF', u'Norfolk Island'), ('MP', u'Northern Mariana Islands'), ('NO', u'Norway'), ('PS', u'Occupied Palestinian Territory'), ('OM', u'Oman'), ('PK', u'Pakistan'), ('PW', u'Palau'), ('PS', u'Palestinian Territory, Occupied'), ('PA', u'Panama'), ('PG', u'Papua New Guinea'), ('PY', u'Paraguay'), ('PE', u'Peru'), ('PH', u'Philippines'), ('PN', u'Pitcairn'), ('BO', u'Plurinational State of Bolivia'), ('PL', u'Poland'), ('PT', u'Portugal'), ('TW', u'Province of China Taiwan'), ('PR', u'Puerto Rico'), ('QA', u'Qatar'), ('KR', u'Republic of Korea'), ('MD', u'Republic of Moldova'), ('RE', u'R\xe9union'), ('RO', u'Romania'), ('RU', u'Russian Federation'), ('RW', u'Rwanda'), ('BL', u'Saint Barth\xe9lemy'), ('SH', u'Saint Helena, Ascension and Tristan Da Cunha'), ('KN', u'Saint Kitts and Nevis'), ('LC', u'Saint Lucia'), ('MF', u'Saint Martin (French Part)'), ('PM', u'Saint Pierre and Miquelon'), ('VC', u'Saint Vincent and the Grenadines'), ('WS', u'Samoa'), ('SM', u'San Marino'), ('ST', u'Sao Tome and Principe'), ('SA', u'Saudi Arabia'), ('SN', u'Senegal'), ('RS', u'Serbia'), ('SC', u'Seychelles'), ('SL', u'Sierra Leone'), ('SG', u'Singapore'), ('BQ', u'Sint Eustatius and Saba Bonaire'), ('SX', u'Sint Maarten (Dutch Part)'), ('SK', u'Slovakia'), ('SI', u'Slovenia'), ('SB', u'Solomon Islands'), ('SO', u'Somalia'), ('ZA', u'South Africa'), ('GS', u'South Georgia and the South Sandwich Islands'), ('SS', u'South Sudan'), ('ES', u'Spain'), ('LK', u'Sri Lanka'), ('SD', u'Sudan'), ('SR', u'Suriname'), ('SJ', u'Svalbard and Jan Mayen'), ('SZ', u'Swaziland'), ('SE', u'Sweden'), ('CH', u'Switzerland'), ('SY', u'Syrian Arab Republic'), ('TW', u'Taiwan, Province of China'), ('TJ', u'Tajikistan'), ('TZ', u'Tanzania, United Republic of'), ('TH', u'Thailand'), ('CD', u'The Democratic Republic of the Congo'), ('MK', u'The Former Yugoslav Republic of Macedonia'), ('TL', u'Timor-leste'), ('TG', u'Togo'), ('TK', u'Tokelau'), ('TO', u'Tonga'), ('TT', u'Trinidad and Tobago'), ('TN', u'Tunisia'), ('TR', u'Turkey'), ('TM', u'Turkmenistan'), ('TC', u'Turks and Caicos Islands'), ('TV', u'Tuvalu'), ('VI', u'U.S. Virgin Islands'), ('UG', u'Uganda'), ('UA', u'Ukraine'), ('AE', u'United Arab Emirates'), ('GB', u'United Kingdom'), ('TZ', u'United Republic of Tanzania'), ('US', u'United States'), ('UM', u'United States Minor Outlying Islands'), ('UY', u'Uruguay'), ('UZ', u'Uzbekistan'), ('VU', u'Vanuatu'), ('VE', u'Venezuela, Bolivarian Republic of'), ('VN', u'Viet Nam'), ('VG', u'Virgin Islands, British'), ('VI', u'Virgin Islands, U.S.'), ('WF', u'Wallis and Futuna'), ('EH', u'Western Sahara'), ('YE', u'Yemen'), ('ZM', u'Zambia'), ('ZW', u'Zimbabwe'))

COUNTRIES = (
	('AF', u'Afghanistan'), ('AL', u'Albania'), ('AC', u'ALECSO'),('DZ', u'Algeria'), 
	('AD', u'Andorra'), ('AO', u'Angola'), 
	('AG', u'Antigua and Barbuda'), ('AR', u'Argentina'), ('AM', u'Armenia'), 
	('AU', u'Australia'), 
	('AT', u'Austria'), ('AZ', u'Azerbaijan'), ('BS', u'Bahamas'), 
	('BH', u'Bahrain'), ('BD', u'Bangladesh'), ('BB', u'Barbados'), 
	('BY', u'Belarus'), ('BE', u'Belgium'), ('BZ', u'Belize'), 
	('BJ', u'Benin'), ('BT', u'Bhutan'), 
	('BO', u'Bolivia, Plurinational State of'), 
	('BA', u'Bosnia and Herzegovina'), ('BW', u'Botswana'), 
	('BR', u'Brazil'), ('BN', u'Brunei Darussalam'), ('BG', u'Bulgaria'), 
	('BF', u'Burkina Faso'), ('BI', u'Burundi'), ('KH', u'Cambodia'), 
	('CM', u'Cameroon'), ('CA', u'Canada'), ('CV', u'Cape Verde'), 
	('TD', u'Chad'), 
	('CL', u'Chile'), ('CN', u'China'), ('CO', u'Colombia'), ('KM', u'Comoros'), 
	('CG', u'Congo'), ('CR', u'Costa Rica'), ('CI', u"C\xf4te D'ivoire"), ('HR', u'Croatia'), 
	('CU', u'Cuba'), ('CY', u'Cyprus'), 
	('CZ', u'Czech Republic'), ('KP', u"Democratic People's Republic of Korea"),
	('RC', u'Democratic Republic of Congo'), ('DK', u'Denmark'), 
	('DJ', u'Djibouti'), ('DO', u'Dominican Republic'), 
	('EC', u'Ecuador'), ('EG', u'Egypt'), ('SV', u'El Salvador'), 
	('GQ', u'Equatorial Guinea'), ('ER', u'Eritrea'),
	('ET', u'Ethiopia'), ('FJ', u'Fiji'), ('FI', u'Finland'), 
	('FR', u'France'), ('GA', u'Gabon'), ('GM', u'Gambia'), 
	('GE', u'Georgia'), ('DE', u'Germany'), ('GH', u'Ghana'), 
	('GR', u'Greece'), ('GD', u'Grenada'), ('GT', u'Guatemala'), 
	('GN', u'Guinea'), ('GY', u'Guyana'), ('HT', u'Haiti'), 
	('HN', u'Honduras'), ('HU', u'Hungary'), 
	('IS', u'Iceland'), ('IN', u'India'), ('ID', u'Indonesia'),
	('IM', u'International Organization for Migration'),
	('IR', u'Iran, Islamic Republic of'), ('IQ', u'Iraq'), ('IE', u'Ireland'), 
	('IL', u'Israel'), ('IT', u'Italy'), ('JM', u'Jamaica'), ('JP', u'Japan'), 
	('JO', u'Jordan'), ('KZ', u'Kazakhstan'), ('KE', u'Kenya'), 
	('KW', u'Kuwait'), ('KG', u'Kyrgyzstan'), 
	('LA', u"Lao People's Democratic Republic"), ('LB', u'Lebanon'), 
	('LS', u'Lesotho'), ('LR', u'Liberia'), ('LY', u'Libya'), 
	('LT', u'Lithuania'), ('LU', u'Luxembourg'), 
	('MG', u'Madagascar'), 
	('MW', u'Malawi'), ('MY', u'Malaysia'), ('MV', u'Maldives'), 
	('ML', u'Mali'), ('MT', u'Malta'), ('MR', u'Mauritania'), 
	('MU', u'Mauritius'), ('MX', u'Mexico'), ('MC', u'Monaco'), 
	('MN', u'Mongolia'), ('MA', u'Morocco'), ('MZ', u'Mozambique'), 
	('MM', u'Myanmar'), ('NA', u'Namibia'),
	('NP', u'Nepal'), ('NL', u'Netherlands'),
	('NZ', u'New Zealand'), ('NI', u'Nicaragua'), ('NE', u'Niger'), 
	('NG', u'Nigeria'), ('NO', u'Norway'), 
	('OM', u'Oman'), ('IC', u'Organization of the Islamic Cooperation'), ('PK', u'Pakistan'), 
	('PS', u'Palestine'), ('PA', u'Panama'), 
	('PG', u'Papua New Guinea'), ('PY', u'Paraguay'), ('PE', u'Peru'), ('PH', u'Philippines'), 
	('PL', u'Poland'), ('PT', u'Portugal'), ('QA', u'Qatar'), 
	('KR', u'Republic of Korea'), ('MD', u'Republic of Macedonia'), 
	('RO', u'Romania'), ('RU', u'Russian Federation'), 
	('RW', u'Rwanda'), ('SR', u'Sahrawi Republic'), 
	('KN', u'Saint Kitts and Nevis'), ('LC', u'Saint Lucia'), 
	('VC', u'Saint Vincent and the Grenadines'), ('ST', u'Sao Tome and Principe'), 
	('SA', u'Saudi Arabia'), ('SN', u'Senegal'), 
	('RS', u'Serbia'), ('SC', u'Seychelles'), ('SL', u'Sierra Leone'), 
	('SG', u'Singapore'), ('SK', u'Slovakia'), ('SO', u'Somalia'), ('ZA', u'South Africa'), 
	('SS', u'South Sudan'), 
	('ES', u'Spain'), ('LK', u'Sri Lanka'), ('SD', u'Sudan'), ('SR', u'Suriname'), 
	('SZ', u'Swaziland'), ('SE', u'Sweden'), 
	('CH', u'Switzerland'), ('SY', u'Syrian Arab Republic'), ('TH', u'Thailand'), 
	('TL', u'Timor-leste'), ('TG', u'Togo'), 
	('TT', u'Trinidad and Tobago'), 
	('TN', u'Tunisia'), ('TR', u'Turkey'), ('TM', u'Turkmenistan'), 
	('UG', u'Uganda'), ('UA', u'Ukraine'), ('UN', u'UNHCR'), ('AE', u'United Arab Emirates'), 
	('GB', u'United Kingdom'), ('TZ', u'United Republic of Tanzania'), 
	('US', u'United States of America'), ('UY', u'Uruguay'), ('UZ', u'Uzbekistan'), 
	('VU', u'Vanuatu'), 
	('VE', u'Venezuela, Bolivarian Republic of'), ('VN', u'Viet Nam'), 
	('YE', u'Yemen'), 
	('ZM', u'Zambia'), ('ZW', u'Zimbabwe'))

YESNO = (( True, 'Yes'), (False, 'No'))

HOWYOUHEAR = (('brochure', 'Brochure'), ('letter', 'Letter'), ('website', 'Website'), ('another_school', 'Other School'), ('other', 'Other'))


TRUEFALSE = (( True, 'True'), (False, 'False'))


