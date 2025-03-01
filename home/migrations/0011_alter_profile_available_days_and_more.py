# Generated by Django 4.1.3 on 2023-04-08 08:51

from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_alter_profile_sub_time_period_alter_profile_sub_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='available_days',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')], default=None, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='available_time',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('8am-12pm', '8am-12pm'), ('12pm-4pm', '12pm-4pm'), ('4pm-8pm', '4pm-8pm'), ('8pm-10pm', '8pm-10pm')], default=None, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='country',
            field=models.CharField(choices=[('---', '---'), ('AF', 'Afghanistan'), ('AX', 'Åland Islands'), ('AL', 'Albania'), ('DZ', 'Algeria'), ('AS', 'American Samoa'), ('AD', 'Andorra'), ('AO', 'Angola'), ('AI', 'Anguilla'), ('AQ', 'Antarctica'), ('AG', 'Antigua and Barbuda'), ('AR', 'Argentina'), ('AM', 'Armenia'), ('AW', 'Aruba'), ('AU', 'Australia'), ('AT', 'Austria'), ('AZ', 'Azerbaijan'), ('BS', 'Bahamas'), ('BH', 'Bahrain'), ('BD', 'Bangladesh'), ('BB', 'Barbados'), ('BY', 'Belarus'), ('BE', 'Belgium'), ('BZ', 'Belize'), ('BJ', 'Benin'), ('BM', 'Bermuda'), ('BT', 'Bhutan'), ('BO', 'Bolivia (Plurinational State of)'), ('BQ', 'Bonaire, Sint Eustatius and Saba'), ('BA', 'Bosnia and Herzegovina'), ('BW', 'Botswana'), ('BV', 'Bouvet Island'), ('BR', 'Brazil'), ('IO', 'British Indian Ocean Territory'), ('BN', 'Brunei Darussalam'), ('BG', 'Bulgaria'), ('BF', 'Burkina Faso'), ('BI', 'Burundi'), ('CV', 'Cabo Verde'), ('KH', 'Cambodia'), ('CM', 'Cameroon'), ('CA', 'Canada'), ('KY', 'Cayman Islands'), ('CF', 'Central African Republic'), ('TD', 'Chad'), ('CL', 'Chile'), ('CN', 'China'), ('CX', 'Christmas Island'), ('CC', 'Cocos (Keeling) Islands'), ('CO', 'Colombia'), ('KM', 'Comoros'), ('CG', 'Congo'), ('CD', 'Congo, Democratic Republic of the'), ('CK', 'Cook Islands'), ('CR', 'Costa Rica'), ('CI', "Côte d'Ivoire"), ('HR', 'Croatia'), ('CU', 'Cuba'), ('CW', 'Curaçao'), ('CY', 'Cyprus'), ('CZ', 'Czechia'), ('DK', 'Denmark'), ('DJ', 'Djibouti'), ('DM', 'Dominica'), ('DO', 'Dominican Republic'), ('EC', 'Ecuador'), ('EG', 'Egypt'), ('SV', 'El Salvador'), ('GQ', 'Equatorial Guinea'), ('ER', 'Eritrea'), ('EE', 'Estonia'), ('SZ', 'Eswatini'), ('ET', 'Ethiopia'), ('FK', 'Falkland Islands (Malvinas)'), ('FO', 'Faroe Islands'), ('FJ', 'Fiji'), ('FI', 'Finland'), ('FR', 'France'), ('GF', 'French Guiana'), ('PF', 'French Polynesia'), ('TF', 'French Southern Territories'), ('GA', 'Gabon'), ('GM', 'Gambia'), ('GE', 'Georgia'), ('DE', 'Germany'), ('GH', 'Ghana'), ('GI', 'Gibraltar'), ('GR', 'Greece'), ('GL', 'Greenland'), ('GD', 'Grenada'), ('GP', 'Guadeloupe'), ('GU', 'Guam'), ('GT', 'Guatemala'), ('GG', 'Guernsey'), ('GN', 'Guinea'), ('GW', 'Guinea-Bissau'), ('GY', 'Guyana'), ('HT', 'Haiti'), ('HM', 'Heard Island and McDonald Islands'), ('VA', 'Holy See'), ('HN', 'Honduras'), ('HK', 'Hong Kong'), ('HU', 'Hungary'), ('IS', 'Iceland'), ('IN', 'India'), ('ID', 'Indonesia'), ('IR', 'Iran (Islamic Republic of)'), ('IQ', 'Iraq'), ('IE', 'Ireland'), ('IM', 'Isle of Man'), ('IL', 'Israel'), ('IT', 'Italy'), ('JM', 'Jamaica'), ('JP', 'Japan'), ('JE', 'Jersey'), ('JO', 'Jordan'), ('KZ', 'Kazakhstan'), ('KE', 'Kenya'), ('KI', 'Kiribati'), ('KP', "Korea (Democratic People's Republic of)"), ('KR', 'Korea, Republic of'), ('KW', 'Kuwait'), ('KG', 'Kyrgyzstan'), ('LA', "Lao People's Democratic Republic"), ('LV', 'Latvia'), ('LB', 'Lebanon'), ('LS', 'Lesotho'), ('LR', 'Liberia'), ('LY', 'Libya'), ('LI', 'Liechtenstein'), ('LT', 'Lithuania'), ('LU', 'Luxembourg'), ('MO', 'Macao'), ('MG', 'Madagascar'), ('MW', 'Malawi'), ('MY', 'Malaysia'), ('MV', 'Maldives'), ('ML', 'Mali'), ('MT', 'Malta'), ('MH', 'Marshall Islands'), ('MQ', 'Martinique'), ('MR', 'Mauritania'), ('MU', 'Mauritius'), ('YT', 'Mayotte'), ('MX', 'Mexico'), ('FM', 'Micronesia (Federated States of)'), ('MD', 'Moldova, Republic of'), ('MC', 'Monaco'), ('MN', 'Mongolia'), ('ME', 'Montenegro'), ('MS', 'Montserrat'), ('MA', 'Morocco'), ('MZ', 'Mozambique'), ('MM', 'Myanmar'), ('NA', 'Namibia'), ('NR', 'Nauru'), ('NP', 'Nepal'), ('NL', 'Netherlands'), ('NC', 'New Caledonia'), ('NZ', 'New Zealand'), ('NI', 'Nicaragua'), ('NE', 'Niger'), ('NG', 'Nigeria'), ('NU', 'Niue'), ('NF', 'Norfolk Island'), ('MK', 'North Macedonia'), ('MP', 'Northern Mariana Islands'), ('NO', 'Norway'), ('OM', 'Oman'), ('PK', 'Pakistan'), ('PW', 'Palau'), ('PS', 'Palestine, State of'), ('PA', 'Panama'), ('PG', 'Papua New Guinea'), ('PY', 'Paraguay'), ('PE', 'Peru'), ('PH', 'Philippines'), ('PN', 'Pitcairn'), ('PL', 'Poland'), ('PT', 'Portugal'), ('PR', 'Puerto Rico'), ('QA', 'Qatar'), ('RE', 'Réunion'), ('RO', 'Romania'), ('RU', 'Russian Federation'), ('RW', 'Rwanda'), ('BL', 'Saint Barthélemy'), ('SH', 'Saint Helena, Ascension and Tristan da Cunha'), ('KN', 'Saint Kitts and Nevis'), ('LC', 'Saint Lucia'), ('MF', 'Saint Martin (French part)'), ('PM', 'Saint Pierre and Miquelon'), ('VC', 'Saint Vincent and the Grenadines'), ('WS', 'Samoa'), ('SM', 'San Marino'), ('ST', 'Sao Tome and Principe'), ('SA', 'Saudi Arabia'), ('SN', 'Senegal'), ('RS', 'Serbia'), ('SC', 'Seychelles'), ('SL', 'Sierra Leone'), ('SG', 'Singapore'), ('SX', 'Sint Maarten (Dutch part)'), ('SK', 'Slovakia'), ('SI', 'Slovenia'), ('SB', 'Solomon Islands'), ('SO', 'Somalia'), ('ZA', 'South Africa'), ('GS', 'South Georgia and the South Sandwich Islands'), ('SS', 'South Sudan'), ('ES', 'Spain'), ('LK', 'Sri Lanka'), ('SD', 'Sudan'), ('SR', 'Suriname'), ('SJ', 'Svalbard and Jan Mayen'), ('SE', 'Sweden'), ('CH', 'Switzerland'), ('SY', 'Syrian Arab Republic'), ('TW', 'Taiwan, Province of China'), ('TJ', 'Tajikistan'), ('TZ', 'Tanzania, United Republic of'), ('TH', 'Thailand'), ('TL', 'Timor-Leste'), ('TG', 'Togo'), ('TK', 'Tokelau'), ('TO', 'Tonga'), ('TT', 'Trinidad and Tobago'), ('TN', 'Tunisia'), ('TR', 'Turkey'), ('TM', 'Turkmenistan'), ('TC', 'Turks and Caicos Islands'), ('TV', 'Tuvalu'), ('UG', 'Uganda'), ('UA', 'Ukraine'), ('AE', 'United Arab Emirates'), ('GB', 'United Kingdom of Great Britain and Northern Ireland'), ('US', 'United States of America'), ('UM', 'United States Minor Outlying Islands'), ('UY', 'Uruguay'), ('UZ', 'Uzbekistan'), ('VU', 'Vanuatu'), ('VE', 'Venezuela (Bolivarian Republic of)'), ('VN', 'Viet Nam'), ('VG', 'Virgin Islands (British)'), ('VI', 'Virgin Islands (U.S.)'), ('WF', 'Wallis and Futuna'), ('EH', 'Western Sahara'), ('YE', 'Yemen'), ('ZM', 'Zambia'), ('ZW', 'Zimbabwe')], default='---', max_length=3),
        ),
        migrations.AlterField(
            model_name='profile',
            name='timezoneutc',
            field=models.CharField(choices=[('UTC-11:00 (Midway Island, American Samoa)', 'UTC-11:00 (Midway Island, American Samoa)'), ('UTC-10:00 (Hawaii)', 'UTC-10:00 (Hawaii)'), ('UTC-08:00 (Alaska)', 'UTC-08:00 (Alaska)'), ('UTC-07:00 (Baja California)', 'UTC-07:00 (Baja California)'), ('UTC-07:00 (Pacific Time US and Canada)', 'UTC-07:00 (Pacific Time US and Canada)'), ('UTC-07:00 (Arizona)', 'UTC-07:00 (Arizona)'), ('UTC-06:00 (Chihuahua, La Paz, Mazatlan)', 'UTC-06:00 (Chihuahua, La Paz, Mazatlan)'), ('UTC-06:00 (Mountain Time US and Canada)', 'UTC-06:00 (Mountain Time US and Canada)'), ('UTC-06:00 (Central America)', 'UTC-06:00 (Central America)'), ('UTC-05:00 (Central Time US and Canada)', 'UTC-05:00 (Central Time US and Canada)'), ('UTC-05:00 (Guadalajara, Mexico City, Monterrey)', 'UTC-05:00 (Guadalajara, Mexico City, Monterrey)'), ('UTC-06:00 (Saskatchewan)', 'UTC-06:00 (Saskatchewan)'), ('UTC-05:00 (Bogota, Lima, Quito)', 'UTC-05:00 (Bogota, Lima, Quito)'), ('UTC-05:00 (Kingston, George Town)', 'UTC-05:00 (Kingston, George Town)'), ('UTC-04:00 (Eastern Time US and Canada)', 'UTC-04:00 (Eastern Time US and Canada)'), ('UTC-04:00 (Indiana East)', 'UTC-04:00 (Indiana East)'), ('UTC-04:30 (Caracas)', 'UTC-04:30 (Caracas)'), ('UTC-03:00 (Asuncion)', 'UTC-03:00 (Asuncion)'), ('UTC-03:00 (Atlantic Time Canada)', 'UTC-03:00 (Atlantic Time Canada)'), ('UTC-04:00 (Cuiaba)', 'UTC-04:00 (Cuiaba)'), ('UTC-04:00 (Georgetown, La Paz, Manaus, San Juan)', 'UTC-04:00 (Georgetown, La Paz, Manaus, San Juan)'), ('UTC-02:30 (Newfoundland and Labrador)', 'UTC-02:30 (Newfoundland and Labrador)'), ('UTC-03:00 (Brasilia)', 'UTC-03:00 (Brasilia)'), ('UTC-03:00 (Buenos Aires)', 'UTC-03:00 (Buenos Aires)'), ('UTC-03:00 (Cayenne, Fortaleza)', 'UTC-03:00 (Cayenne, Fortaleza)'), ('UTC-02:00 (Greenland)', 'UTC-02:00 (Greenland)'), ('UTC-03:00 (Montevideo)', 'UTC-03:00 (Montevideo)'), ('UTC-03:00 (Salvador)', 'UTC-03:00 (Salvador)'), ('UTC-03:00 (Santiago)', 'UTC-03:00 (Santiago)'), ('UTC-02:00 (Mid-Atlantic)', 'UTC-02:00 (Mid-Atlantic)'), ('UTC+00:00 (Azores)', 'UTC+00:00 (Azores)'), ('UTC-01:00 (Cape Verde Islands)', 'UTC-01:00 (Cape Verde Islands)'), ('UTC+01:00 (Dublin, Edinburgh, Lisbon, London)', 'UTC+01:00 (Dublin, Edinburgh, Lisbon, London)'), ('UTC+01:00 (Casablanca)', 'UTC+01:00 (Casablanca)'), ('UTC+00:00 (Monrovia, Reykjavik)', 'UTC+00:00 (Monrovia, Reykjavik)'), ('UTC+02:00 (Amsterdam, Berlin, Bern, Rome, Stockholm, Vienna)', 'UTC+02:00 (Amsterdam, Berlin, Bern, Rome, Stockholm, Vienna)'), ('UTC+02:00 (Belgrade, Bratislava, Budapest, Ljubljana, Prague)', 'UTC+02:00 (Belgrade, Bratislava, Budapest, Ljubljana, Prague)'), ('UTC+02:00 (Brussels, Copenhagen, Madrid, Paris)', 'UTC+02:00 (Brussels, Copenhagen, Madrid, Paris)'), ('UTC+02:00 (Sarajevo, Skopje, Warsaw, Zagreb)', 'UTC+02:00 (Sarajevo, Skopje, Warsaw, Zagreb)'), ('UTC+01:00 (West Central Africa)', 'UTC+01:00 (West Central Africa)'), ('UTC+02:00 (Windhoek)', 'UTC+02:00 (Windhoek)'), ('UTC+03:00 (Athens, Bucharest)', 'UTC+03:00 (Athens, Bucharest)'), ('UTC+03:00 (Beirut)', 'UTC+03:00 (Beirut)'), ('UTC+02:00 (Cairo)', 'UTC+02:00 (Cairo)'), ('UTC+03:00 (Damascus)', 'UTC+03:00 (Damascus)'), ('UTC+03:00 (Eastern Europe)', 'UTC+03:00 (Eastern Europe)'), ('UTC+02:00 (Harare, Pretoria)', 'UTC+02:00 (Harare, Pretoria)'), ('UTC+03:00 (Helsinki, Kiev, Riga, Sofia, Tallinn, Vilnius)', 'UTC+03:00 (Helsinki, Kiev, Riga, Sofia, Tallinn, Vilnius)'), ('UTC+03:00 (Istanbul)', 'UTC+03:00 (Istanbul)'), ('UTC+03:00 (Jerusalem)', 'UTC+03:00 (Jerusalem)'), ('UTC+02:00 (Kaliningrad)', 'UTC+02:00 (Kaliningrad)'), ('UTC+02:00 (Tripoli)', 'UTC+02:00 (Tripoli)'), ('UTC+03:00 (Amman)', 'UTC+03:00 (Amman)'), ('UTC+03:00 (Baghdad)', 'UTC+03:00 (Baghdad)'), ('UTC+03:00 (Kuwait, Riyadh)', 'UTC+03:00 (Kuwait, Riyadh)'), ('UTC+03:00 (Minsk)', 'UTC+03:00 (Minsk)'), ('UTC+03:00 (Moscow, St. Petersburg, Volgograd)', 'UTC+03:00 (Moscow, St. Petersburg, Volgograd)'), ('UTC+03:00 (Nairobi)', 'UTC+03:00 (Nairobi)'), ('UTC+03:30 (Tehran)', 'UTC+03:30 (Tehran)'), ('UTC+04:00 (Abu Dhabi, Muscat)', 'UTC+04:00 (Abu Dhabi, Muscat)'), ('UTC+05:00 (Baku)', 'UTC+05:00 (Baku)'), ('UTC+04:00 (Izhevsk, Samara)', 'UTC+04:00 (Izhevsk, Samara)'), ('UTC+04:00 (Port Louis)', 'UTC+04:00 (Port Louis)'), ('UTC+04:00 (Tbilisi)', 'UTC+04:00 (Tbilisi)'), ('UTC+04:00 (Yerevan)', 'UTC+04:00 (Yerevan)'), ('UTC+04:30 (Kabul)', 'UTC+04:30 (Kabul)'), ('UTC+05:00 (Tashkent, Ashgabat)', 'UTC+05:00 (Tashkent, Ashgabat)'), ('UTC+05:00 (Ekaterinburg)', 'UTC+05:00 (Ekaterinburg)'), ('UTC+05:00 (Islamabad, Karachi)', 'UTC+05:00 (Islamabad, Karachi)'), ('UTC+05:30 (Chennai, Kolkata, Mumbai, New Delhi)', 'UTC+05:30 (Chennai, Kolkata, Mumbai, New Delhi)'), ('UTC+05:30 (Sri Jayawardenepura)', 'UTC+05:30 (Sri Jayawardenepura)'), ('UTC+05:45 (Kathmandu)', 'UTC+05:45 (Kathmandu)'), ('UTC+06:00 (Astana)', 'UTC+06:00 (Astana)'), ('UTC+06:00 (Dhaka)', 'UTC+06:00 (Dhaka)'), ('UTC+06:00 (Novosibirsk)', 'UTC+06:00 (Novosibirsk)'), ('UTC+06:30 (Yangon Rangoon)', 'UTC+06:30 (Yangon Rangoon)'), ('UTC+07:00 (Bangkok, Hanoi, Jakarta)', 'UTC+07:00 (Bangkok, Hanoi, Jakarta)'), ('UTC+07:00 (Krasnoyarsk)', 'UTC+07:00 (Krasnoyarsk)'), ('UTC+08:00 (Beijing, Chongqing, Hong Kong SAR, Urumqi)', 'UTC+08:00 (Beijing, Chongqing, Hong Kong SAR, Urumqi)'), ('UTC+08:00 (Irkutsk)', 'UTC+08:00 (Irkutsk)'), ('UTC+08:00 (Kuala Lumpur, Singapore)', 'UTC+08:00 (Kuala Lumpur, Singapore)'), ('UTC+08:00 (Perth)', 'UTC+08:00 (Perth)'), ('UTC+08:00 (Taipei)', 'UTC+08:00 (Taipei)'), ('UTC+08:00 (Ulaanbaatar)', 'UTC+08:00 (Ulaanbaatar)'), ('UTC+09:00 (Osaka, Sapporo, Tokyo)', 'UTC+09:00 (Osaka, Sapporo, Tokyo)'), ('UTC+09:00 (Seoul)', 'UTC+09:00 (Seoul)'), ('UTC+09:00 (Yakutsk)', 'UTC+09:00 (Yakutsk)'), ('UTC+10:30 (Adelaide)', 'UTC+10:30 (Adelaide)'), ('UTC+09:30 (Darwin)', 'UTC+09:30 (Darwin)'), ('UTC+10:00 (Brisbane)', 'UTC+10:00 (Brisbane)'), ('UTC+11:00 (Canberra, Melbourne, Sydney)', 'UTC+11:00 (Canberra, Melbourne, Sydney)'), ('UTC+10:00 (Guam, Port Moresby)', 'UTC+10:00 (Guam, Port Moresby)'), ('UTC+11:00 (Hobart)', 'UTC+11:00 (Hobart)'), ('UTC+10:00 (Magadan)', 'UTC+10:00 (Magadan)'), ('UTC+10:00 (Vladivostok, Magadan)', 'UTC+10:00 (Vladivostok, Magadan)'), ('UTC+11:00 (Chokirdakh)', 'UTC+11:00 (Chokirdakh)'), ('UTC+11:00 (Solomon Islands, New Caledonia)', 'UTC+11:00 (Solomon Islands, New Caledonia)'), ('UTC+12:00 (Anadyr, Petropavlovsk-Kamchatsky)', 'UTC+12:00 (Anadyr, Petropavlovsk-Kamchatsky)'), ('UTC+13:00 (Auckland, Wellington)', 'UTC+13:00 (Auckland, Wellington)'), ('UTC+12:00 (Fiji Islands, Kamchatka, Marshall Islands)', 'UTC+12:00 (Fiji Islands, Kamchatka, Marshall Islands)'), ("UTC+13:00 (Nuku'alofa)", "UTC+13:00 (Nuku'alofa)"), ('UTC+14:00 (Samoa)', 'UTC+14:00 (Samoa)')], default='UTC+00:00 (Azores)', max_length=255),
        ),
    ]
