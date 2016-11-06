from crontab import CronTab
cron = CronTab(user='joshbenner')
#date = month, day, hour, minute


job = cron.new(command='/Library/Frameworks/Python.framework/Versions/3.4/bin/python3 /Users/joshbenner/WebScrapingWorkshop/SpartyNomNom/SpartyNomNom.py',)
#job.hour.every(24)

job.minute.every(1)
#job.dow.on('SUN')

job.enable()
cron.write()

