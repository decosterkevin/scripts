#!/usr/bin/python

import sys, getopt
import yaml
import csv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from itertools import islice
import smtplib
import html2text

def main(argv):
    file = ''
    configFile = ''
    textFile = ''
    try:

        opts, args = getopt.getopt(argv, "hf:c:t:")
        print(argv)
    except getopt.GetoptError:
        print('main.py -f <csv file> -c <config file .yaml> -t <text file .yaml>')
        sys.exit(2)
    for opt, arg in opts:

        if opt == '-h':
            print('main.py -f <csv file> -c <config file .yaml> -t <text file>')
            sys.exit()
        elif opt in ("-f", "--file"):
            file = arg
        elif opt in ("-c", "--config"):
            configFile = arg
        elif opt in ("-t", "--text"):
            textFile = arg

    config = yaml.safe_load(open(configFile))
    option = yaml.safe_load(open(textFile))

    emailPW = config.get('password')
    emailUN=config.get('username')
    emailSMTP =config.get('smtp')
    emailPort = config.get('port')
    if None in (emailPort, emailPW, emailSMTP, emailUN ):
        print('error in config file')
        sys.exit()

    startRow = option.get('row')
    emailCol = option.get('email_col')
    nameCol = option.get('name_col')
    optionCol = option.get('option_col')
    if None in (startRow, emailCol, nameCol, optionCol):
        print('error in option file')
        sys.exit()

    server = smtplib.SMTP(emailSMTP, emailPort)
    server.starttls()
    server.login(emailUN, emailPW)

    option1 = option.get("option_1")
    option2 = option.get("option_2")
    optionDefault = option.get("option_default")

    if None in (option1, option2, optionDefault):
        print('cannot extract option')
        sys.exit()

    with open(file, newline='') as csvfile:
        filereader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in islice(filereader,  startRow, None):

            toAddress = row[emailCol]
            toName = row[nameCol]
            toOption= row[optionCol]

            text=''
            if toOption is None:
                print("cannot extract option")
            else:
                if(toOption == option1.get("value")):
                    text = option1.get("text").format(toName)
                if(toOption == option2.get("value")):
                    text = option2.get("text").format(toName)
                else:
                    tmp = option2.get("text")
                    if tmp is not None:
                        text = optionDefault.get("text").format(toName)

            msg = MIMEMultipart('alternative')

            #
            msg['From'] = emailUN
            msg['To'] = toAddress
            msg['Subject'] = "Anniversaire M&K"

            part1 = MIMEText(html2text.html2text(text).encode("UTF-8"), 'plain', "UTF-8")
            part2 = MIMEText(text.encode("UTF-8"), 'html', "UTF-8")

            msg.attach(part1)
            msg.attach(part2)

            server.sendmail(msg['From'] ,  msg['To'], msg.as_string())
            print("email sent to " + toAddress)
    server.quit()

if __name__ == "__main__":
    main(sys.argv[1:])