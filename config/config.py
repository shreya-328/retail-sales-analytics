from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')

DatabaseConnString = config['database']['connection_string']

smtpServer = config['email']['smtpServer']
smtpPort = config['email']['smtpPort']
smtpUser = config['email']['smtpUser']
smtpPassword = config['email']['smtpPassword']