import argparse
from config import Mail

def main():
  """
  Parse input arguments
  """
  parser = argparse.ArgumentParser(description='Using mailTip pipeline!')
  parser.add_argument('-t', dest='comment',
                      help='Task name',
                      type=str)
  parser.add_argument('-f', dest='file_path',
                    help='Path to the Markdown file',
                    type=str)

  args = parser.parse_args()
  
  Mail(args.comment, args.file_path).send()


if __name__ == "__main__":
    main()