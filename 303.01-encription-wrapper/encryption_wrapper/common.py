import subprocess
import sys


def error_and_exit(message):
  print('encryption_wrapper wrapper ERROR: {}'.format(message))
  sys.exit(1)


def run_command(cmd, description):

  try:
    p = subprocess.Popen(cmd,
                         shell=True,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    while True:
      line = p.stdout.readline()
      if not line:
        break
      else:
        print(str(line.strip(), 'utf-8'))
  except subprocess.SubprocessError as command_exception:
    error_and_exit('{} failed: {}'.format(description,
                                          str(command_exception)))

  p.communicate()
  return p.returncode
