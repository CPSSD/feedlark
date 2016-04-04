import gearman
import sys

def get_username_from_input(argv):
    return ' '.join(argv[1:])

def main():
    gearman_client = gearman.GearmanClient(['localhost:4730'])
    if len(sys.argv) < 2:
        print('Please specify a user to get the error of. See README.md')
        return
    username = get_username_from_input(sys.argv)
    print username

if __name__ == '__main__':
    main()
