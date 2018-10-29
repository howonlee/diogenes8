Use pyfakefs to mock filesystem
Lots of http request mocks, but I don't think needed. Use the settings functionality to create mock settings, which will call out to localhost instead of mailgun api

Overall goal is to create pip installable dealio, which presupposes ripping out the mailgun and making it work
