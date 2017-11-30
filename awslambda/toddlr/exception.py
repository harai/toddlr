import logging

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class RetriableError(Exception):
  pass


class UnretriableError(Exception):
  pass


def handle_error(fn):

  def wrapper(*args, **kwargs):
    try:
      return fn(*args, **kwargs)
    except RetriableError as e1:
      log.info('Retriable error occurred: {}'.format(e1))
      raise e1
    except UnretriableError as e2:
      log.error('Unretriable error occurred: {}'.format(e2))
      log.exception(e2)

  return wrapper
