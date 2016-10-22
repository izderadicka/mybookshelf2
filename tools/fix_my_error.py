import argparse
import mysql.connector as mysql
import shutil
import os.path

def main():
    p=argparse.ArgumentParser()
    p.add_argument('-H', '--host', default='localhost', help='MySQL host')
    p.add_argument('-p', '--port', type=int, default=3306, help='MySQL port')
    p.add_argument('--user', default='ebooks', help='db user')
    p.add_argument('--pwd', default='', help='db user password')
    p.add_argument('--db', default='ebooks', help='db name')
    p.add_argument('--dir', required=True, help='ebooks dir')
    p.add_argument('--backup-dir', required=True, help="backup directory")
    p.add_argument('-v', '--verbose', action='store_true', help='verbose output')
    p.add_argument('--dry', action='store_true', help='dry run')
    
    args = p.parse_args()
    
    conn = mysql.connect(host=args.host, port=args.port, user=args.user, password=args.pwd,
                         database=args.db, charset='utf8')
    c = conn.cursor()
    c.execute('select location, size from ebook_source')
    recovered = 0
    for i,src in enumerate(c):
        src_file=os.path.join(args.dir, src[0])
        if not os.path.exists(src_file):
            if args.verbose: print('Missing file %s'%src[0])
            back_file = os.path.join(args.backup_dir, src[0])
            if os.path.exists(back_file):
                if not args.dry: shutil.copy(back_file, src_file)
                if args.verbose: print('Recovering file %s'%src[0])
                recovered+=1
            else:
                print('%d Cannot Recover File %s'% (i,src[0]))
    print('recovered %d files'%recovered)
            
            
if __name__ == '__main__':
    main()
    print('##### DONE #####')
    