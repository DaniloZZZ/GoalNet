import logging

import logging
import logging.config

logging.config.fileConfig('logging.conf')

# create logger
db= logging.getLogger('db')
bot= logging.getLogger('bot')
main= logging.getLogger('main')

if __name__=='__main__':
    # 'application' code
    bot.debug('debug message')
    bot.info('info message')
    bot.warn('warn message')
    bot.error('error message')
    bot.critical('critical message')
    db.debug('debug message')
    db.info('info message')
    db.warn('warn message')
    db.error('error message')
    db.critical('critical message')
    main.info('info message')
    main.warn('warn message')
    main.error('error message')
    main.critical('critical message')
