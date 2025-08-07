import logging


def main_run():
    data = 'enough'

    logging.basicConfig(
        level = logging.DEBUG,

        filename = 'infor.log',
        filemode = 'w',
        format = '%(asctime)s-%(name)s-%(levelname)s-%(message)s',
        datefmt= '%Y-%m-%d %H:%M:%S'
    )
    if data == 'enough' : 

        logging.info('Conlusion is drawn from data.')
    else:
        logging.info('Data is crunxed')

if __name__ == "__main__":
    main_run()

