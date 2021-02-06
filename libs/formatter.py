from string import ascii_lowercase

class Formatter:

    def __init__(self, names, surnames):
        self.first = names
        self.surnames = surnames
        self.usernames = []
    
    def first_dot_last(self):
        results = []
        for name in self.first:
            for surname in self.surnames:
                results.append('{}.{}'.format(name, surname))
        
        results = list(set(results))
        self.usernames = results
    
    def first_initial_dot_last(self):
        results = []
        self.first = [i for i in ascii_lowercase]
        for name in self.first:
            for surname in self.surnames:
                results.append('{}.{}'.format(name, surname))
        
        results = list(set(results))
        self.usernames = results
    
    def first_dot_last_initial(self):
        results = []
        for name in self.first:
            for surname in self.surnames:
                results.append('{}.{}'.format(name, surname[0]))
        
        results = list(set(results))
        self.usernames = results
    
    def first_initial_last(self):
        results = []
        self.first = [i for i in ascii_lowercase]
        for name in self.first:
            for surname in self.surnames:
                results.append('{}{}'.format(name, surname))
        
        results = list(set(results))
        self.usernames = results
    
    def first_last_initial(self):
        results = []
        for name in self.first:
            for surname in self.surnames:
                results.append('{}.{}'.format(name, surname[0]))
        
        results = list(set(results))
        self.usernames = results
    
    def first_last(self):
        results = []
        for name in self.first:
            for surname in self.surnames:
                results.append('{}{}'.format(name, surname))
        
        results = list(set(results))
        self.usernames = results
    
    def first_only(self):
        results = []
        results = self.first
        results = list(set(results))
        self.usernames = results
    
    def last_only(self):
        results = []
        results = self.surnames
        results = list(set(results))
        self.usernames = results
    
    def count(self):
        return len(self.usernames)
    
    def sorted(self):
        return sorted(self.usernames)
