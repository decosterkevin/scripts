#!/usr/bin/python

import sys, getopt
import yaml
import csv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from itertools import islice
import smtplib
import time
import html2text

class Mailer:

    def __init__(self,emailPort, emailPW, emailSMTP, emailUN):
        self.emailPort= emailPort
        self.emailPW=emailPW
        self.emailUN= emailUN
        self.emailSMTP= emailSMTP
        self.server = smtplib.SMTP(emailSMTP, emailPort)
        self.server.starttls()
        self.server.login(emailUN, emailPW)


    def sendMail(self, toAddress, subject, text, cc=None, option=None):
        print("trying to sent email: " + toAddress)
        msg = MIMEMultipart('alternative')

        if(option):
            text = text.format(option)

        msg['From'] = self.emailUN
        msg['To'] = toAddress
        msg['Subject'] = subject

        if cc is not None:
            msg['CC'] = cc

        part1 = MIMEText(html2text.html2text(text).encode("UTF-8"), 'plain', "UTF-8")
        part2 = MIMEText(text.encode("UTF-8"), 'html', "UTF-8")

        msg.attach(part1)
        msg.attach(part2)

        self.server.sendmail(msg['From'], msg['To'], msg.as_string())
        print("email sent to " + toAddress)
        time.sleep(1.0)

    def close(self):
        self.server.quit()


    def sendMailsFromCSV(self,file,subject,option,cc=None):
        startRow = option.get('row')
        emailCol = option.get('email_col')
        nameCol = option.get('name_col')
        optionCol = option.get('option_col')
        if None in (startRow, emailCol, nameCol, optionCol):
            print('error in option file')
            sys.exit()

        option1 = option.get("option_1")
        option2 = option.get("option_2")
        optionDefault = option.get("option_default")
        if None in (option1, option2, optionDefault):
            print('cannot extract option')
            sys.exit()

        with open(file, newline='') as csvfile:
            filereader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in islice(filereader, startRow, None):

                toAddress = row[emailCol]
                toName = row[nameCol]
                toOption = row[optionCol]
                print("trying to sent email: " + toAddress + "with option " + toOption)
                text = ''
                if toOption is None:
                    print("cannot extract option")
                else:
                    if (toOption == option1.get("value")):
                        text = option1.get("text")
                    elif (toOption == option2.get("value")):
                        text = option2.get("text")
                    else:
                        toOption = None
                if toOption is not None:
                    self.sendMail(toAddress,subject, text, cc, toName)


    def sendMailsFromList(self, listEmails, text,subject,cc=None, listOptions=None):
            for i in range(0, len(listEmails)):
                if listOptions and len(listOptions) == len(listEmails):
                    self.sendMail(listEmails[i],subject,text,cc, listOptions[i])
                else:
                    self.sendMail(listEmails[i], subject, text, cc)
# def main(argv):
#     file = ''
#     configFile = ''
#     textFile = ''
#     cc=''
#     try:
#
#         opts, args = getopt.getopt(argv, "hf:c:t:")
#         print(argv)
#     except getopt.GetoptError:
#         print('main.py -f <csv file> -c <config file .yaml> -t <text file .yaml>')
#         sys.exit(2)
#     for opt, arg in opts:
#
#         if opt == '-h':
#             print('main.py -f <csv file> -c <config file .yaml> -t <text file>')
#             sys.exit()
#         elif opt in ("-f", "--file"):
#             file = arg
#         elif opt in ("-c", "--config"):
#             configFile = arg
#         elif opt in ("-t", "--text"):
#             textFile = arg
#
#     config = yaml.safe_load(open(configFile))
#     option = yaml.safe_load(open(textFile))
#
#     emailPW = config.get('password')
#     emailUN=config.get('username')
#     emailSMTP =config.get('smtp')
#     emailPort = config.get('port')
#
#     cc = config.get('cc')
#     subject = "Anniversaire M&K"
#
#     if None in (emailPort, emailPW, emailSMTP, emailUN ):
#         print('error in config file')
#         sys.exit()
#
#     mailer = Mailer(emailPort, emailPW, emailSMTP, emailUN)
#
#     if args=="fromCSV":
#         mailer.sendMailsFromCSV(file,subject,option)
#     else:
#
#         mailer.sendMailsFromList(listEmails, text, subject,cc,listOptions)
#
#
#     mailer.close()


def mainBis(argv):
    configFile = ''
    paramFile = ''
    try:
        opts, args = getopt.getopt(argv, "hc:p:")
        print(argv)
    except getopt.GetoptError:
        print('main.py -c <config file .yaml> -p <param file>')
        sys.exit(2)
    for opt, arg in opts:

        if opt == '-h':
            print('main.py -c <config file .yaml> -p <param file>')
            sys.exit()
        elif opt in ("-c", "--configFile"):
            configFile = arg
        elif opt in ("-p", "--paramFile"):
            paramFile = arg

    config = yaml.safe_load(open(configFile))
    option = yaml.safe_load(open(paramFile))

    emailPW = config.get('password')
    emailUN = config.get('username')
    emailSMTP = config.get('smtp')
    emailPort = config.get('port')

    if None in (emailPort, emailPW, emailSMTP, emailUN):
        print('error in config file')
        sys.exit()

    subject = option.get("subject")
    cc = option.get("cc", None)
    emailsFile = option.get("emailsFile")
    namesFile = option.get("namesFile", None)
    text = option.get("text")

    if None in (text,subject, emailsFile):
        print("error params file")
        sys.exit()

    listEmails = open(emailsFile, "r").read().splitlines()
    listNames= None
    if namesFile:
        listNames = open(namesFile, "r").read().splitlines()


    mailer = Mailer(emailPort, emailPW, emailSMTP, emailUN)
    mailer.sendMailsFromList(listEmails, text, subject, cc, listNames)
    mailer.close()

if __name__ == "__main__":
    mainBis(sys.argv[1:])