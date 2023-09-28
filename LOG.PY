import logging

logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

def some_function():
    try:
        # Some operation
        pass
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)

some_function()
