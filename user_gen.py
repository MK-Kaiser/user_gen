#! /usr/bin/python3

from libs.firstname import FirstNames, CURRENT_YEAR
from libs.surnames import SurNames
from libs.formatter import Formatter

import argparse
import os
import fileinput
from time import sleep


class Action:
    def __init__(self):
        self.exit = False
    
    def inform_user(self, text, end='\n'):
        if not self.usernames_only:
            print(text, end=end)
        return
    
    def store_to_file(self, usernames, location):
        with open(location, 'w') as output:
            output.writelines('\n'.join(usernames))
    
    def prompt_for_filename(self):
        return input('Would you prefer to save these as a file? [Y/n]: ').lower()
    
    def set_output_file(self):
        default = "names_generated_{}.txt".format(self.formatting)
        output = input('What would you like the filename to be (default: {}): '.format(default))
        output = output.strip()
        if not output:
            output = default
        return output


    def verify_stdout(self, total):
        print('\nThe result of this are over 2000 possibilities ({:,} total)'.format(total))
        choice = self.prompt_for_filename()
        if not choice or choice[0].lower() == 'y':
            self.output = self.set_output_file()
            return
        print('Ok, printing to stdout then. Hope you have time and your line buffer is set correctly...')
        sleep(1)
        return
        
    def __check_max_count__(self):
        # checks
        if self.top_firstnames > 1000:
            self.inform_user('A max of 1000 records is allowed')
            self.top_firstnames = 1000
    
    def __check_max_years__(self):
        if self.years > (CURRENT_YEAR - 1980):
            self.years = (CURRENT_YEAR - 1980)
            self.inform_user("A max of {} years is allowed as SSA didn't digitize records before 1980.".format(self.years))
    

    def __get_firstnames__(self):
        self.firstnames = FirstNames()
        if not self.formatting in ['flast', 'f.last']:
            # TODO make these inherit from this class
            self.firstnames.usernames_only = self.usernames_only
            self.firstnames.top_firstnames = self.top_firstnames
            self.firstnames.years = self.years
            self.firstnames.debug = self.debug
            self.firstnames.usernames_only = self.usernames_only
            self.firstnames.verbose = self.verbose
            # start calls
            self.firstnames.request()
            self.firstnames.dedupe_names()
        return
    

    def __get_surnames__(self):
        self.surnames = SurNames()
        # TODO make these inherit from this class
        self.surnames.usernames_only = self.usernames_only
        self.surnames.top_surnames = self.top_surnames
        self.surnames.debug = self.debug
        self.surnames.usernames_only = self.usernames_only
        self.surnames.verbose = self.verbose
        # start calls
        self.surnames.request()
        self.surnames.dedupe_surnames()
        return
    
    def __set_username_count__(self):
        if self.username_count == 0:
            self.username_count = self.formatter.count()
    
    def __check_for_continue(self):
        if self.formatter.count() == 0:
            self.exit = True
    

    def run(self):
        
        self.__check_max_count__()
        self.__check_max_years__()
        self.__get_firstnames__()        
        self.__get_surnames__()
        
        if args.type == 'male':
            self.formatter = Formatter(self.firstnames.males, self.surnames.surnames)
        elif args.type == 'female':
            self.formatter = Formatter(self.firstnames.females, self.surnames.surnames)
        elif args.type:
            self.formatter = Formatter(self.firstnames.combined, self.surnames.surnames)
        
        if self.formatting == 'first.last':
            self.formatter.first_dot_last()
        elif self.formatting == 'f.last':
            self.formatter.first_initial_dot_last()
        elif self.formatting == 'first.l':
            self.formatter.first_dot_last_initial()
        elif self.formatting == 'flast':
            self.formatter.first_initial_last()
        elif self.formatting == 'firstl':
            self.formatter.first_last_initial()
        elif self.formatting == 'firstlast':
            self.formatter.first_last()
        elif self.formatting == 'first':
            self.formatter.first_only()
        elif self.formatting == 'last':
            self.formatter.last_only()

        
        self.__check_for_continue()

        if self.exit:
            self.inform_user('Ther are 0 results based on your arguments. Increase the years or counts.')
            exit()

        # reduce count
        self.__set_username_count__()
        usernames = self.formatter.usernames[:self.username_count]

        if self.sort:
            usernames = sorted(usernames)

        if self.output == None and len(usernames) > 2000 and not self.usernames_only:
            self.verify_stdout(len(usernames))        
        
        if self.output:
            location = os.path.join('/tmp/', self.output)
            self.store_to_file(usernames, location)
            print('\nfile created: {}'.format(location))
            return

        # print to stdout
        self.inform_user('################################')
        for username in usernames:
            print(username)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generates a list of usernames from SSA and Namecensus respositories.')
    parser.add_argument('-f', '--format', metavar='str', help='This sets the format for username output. Choices are: first.last, f.last, first.l, flast, firstl, firstlast, first, last.', choices=['first.last','f.last','first.l','flast','firstl','firstlast','first','last'], default='flast', action='store', required=False)
    parser.add_argument('-tf', '--top-firstnames', metavar='n', help='This is the top number of firstnames to return from the SSA query for each year specified. The min selection is 1 and the max is 1000. Any value less then 1 will result in a value of 10 being returned. This is not the total amount of useranmes returned, as they will be combined with surnames. This feature is meant to be used in conjunction with the -f first only specification. Additonally, this number is doubled if "combined" is selected from the type. Default: 1000', default=1000, type=int, action='store', required=False)
    parser.add_argument('-ts', '--top-surnames', metavar='n', help='This is the top number of surnames to return from the name census query. The min selection is 1. This is not the total amount of useranmes returned. Default: 1000', default=1000, type=int, action='store', required=False)
    parser.add_argument('-c', '--count', metavar='n', help='This returns only n number of usernames. Default: 0 (all)', default=0, type=int, action='store', required=False)
    parser.add_argument('-y', '--years', metavar='n', help='This is the number of previous years to search starting from the current year. This will increase your firstname results. Default: 2', default=2, type=int, action='store', required=False)
    parser.add_argument('-t', '--type', metavar='type', help='This is the type of firstnames to return. Choices are: male, female, combined. Default: combined', choices=['male', 'female', 'combined'], default='combined', action='store', required=False)
    parser.add_argument('-s', '--sort', help='This sorts the final list of usernames alphabetically. Default: False', action='store_true', required=False)
    parser.add_argument('-d', '--debug', help='This prints the output from the web requets. Default: False', action='store_true', required=False)
    parser.add_argument('-v', '--verbosity', help='This does nolthing at the moment. Default: False', action='store_true', required=False)
    
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-uo', '--usernames-only', help='This only outputs the usernames and none of the filler text. This can be used when piping this into another command. This will disable verbosity if enabled. Default: False', action='store_true', required=False)
    group.add_argument('-o', '--output', metavar='filename', help='This is the filename of the output file. The file will be created in the /tmp/ directory and not print to stdout. Cannot be used in conjunction with the -uo flag. Default: stdout.', action='store', required=False)
    
    args = parser.parse_args()
    
    action = Action()
    
    # formatting
    action.formatting = args.format
    action.verbose = args.verbosity if not args.usernames_only else False
    
    # results
    action.top_firstnames = args.top_firstnames
    action.top_surnames = args.top_surnames
    action.years = args.years
    
    # output
    action.debug = args.debug
    action.sort = args.sort
    action.usernames_only = args.usernames_only
    action.output = args.output
    action.username_count = args.count
    
    try:
        action.run()
    except KeyboardInterrupt:
        exit('\nStopping the thing...')
