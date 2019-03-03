import logging
###
FORMAT = '[%(asctime)s.%(msecs)3d::%(levelname)-5s::%(module)s]\t%(message)s'
logging.basicConfig(
    level=logging.DEBUG,
    format = FORMAT,
    datefmt = '%M:%S',
)
log = logging.getLogger('trio_test')
###

