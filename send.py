import smtplib
import argparse
import os


def load_template(filename):
    content = ''
    if os.path.exists(filename):
        fp = open(filename, "r", encoding="utf8")
        content = fp.read()
        fp.close()
    return content


def send_mail(to,subject):
    server = smtplib.SMTP('', port)
    # login
    server.login('yourmail@ff.com', 'password');
    template = load_template('./mail/mail.html')
    server.sendmail('from', 'to', template);


if __name__ == '__main__':
    # check_regex()
    ap = argparse.ArgumentParser()
    ap.add_argument('-to', help='query', required=True)
    ap.add_argument('-s', help='report file [html, csv, json]', default=None)
    # ap.add_argument('-r', help='report file [html, csv, json]', default=None)

    args = ap.parse_args()
    if ap.args.q:
        send_mail(args.to, args.s)