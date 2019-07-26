import argparse
from config import Task, Config
import os.path as path


def main():
  """
  Parse input arguments
  """
  parser = argparse.ArgumentParser(description='Using mailTip pipeline!')
  parser.add_argument('-t', dest='to_addr',
                      help='the address you will send to',
                      type=str)
  parser.add_argument('-e', dest='from_addr',
                    help='email message you using',
                    type=str)

  parser.add_argument('-c', action='store_true',
                      default=False,
                     help='create a task pipeline')

  parser.add_argument('-s',
                      default=False,
                    help='task pipeline name to send')

  parser.add_argument('-m',default='None',
                      help='manuly',
                      type=str)

  parser.add_argument('--file', 
                      help='file path', 
                      type=str)
  args = parser.parse_args()
  
  


  config = Config()
  if args.c:
    config.add_task()
  
  
  elif args.s:
    if not path.exists(args.file):
      print('File needed! Using --file to add file path!')
      exit(0)
    t = Task(args.s, args.file)
    t.send()

  else:
    print('Arguments wrong! try -h to get help :)')



if __name__ == "__main__":
    main()