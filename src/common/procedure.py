from typing import List

try:
    from pattern import LTEPattern, NSAPattern
except ImportError:
    from .pattern import LTEPattern, NSAPattern


class LTEProcedurePatterns:
    def __init__(self, procedure_type: str):
        self.procedure_type = procedure_type
        self.total_patterns = 0
        self.lte_pattern_list: List[LTEPattern] = list()

    def __str__(self):
        patterns = [pat.__str__() for pat in self.lte_pattern_list]
        return f"====== {self.procedure_type} =======\n {patterns}\n"

    def add_pattern(self, pattern: LTEPattern):
        self.lte_pattern_list = self.lte_pattern_list.append(pattern)
        self.total_patterns += 1

    def add_pattern_from_list(self, items: list, init_support=0):
        # validate items and then add
        if self.validate_items(items):
            self.lte_pattern_list.append(LTEPattern(items, init_support))
            self.total_patterns += 1
        else:
            raise Exception('Cannot create LTEPattern object: list invalid!')

    def evict_pattern(self, threshold_fresh: int):
        self.lte_pattern_list = [pat for pat in self.lte_pattern_list
                                  if pat.is_fresh(self.total_patterns, threshold_fresh)]
        self.total_patterns = len(self.lte_pattern_list)

    def validate_items(self, items: list):
        if LTEPattern.validate_items(items) and self.procedure_type == items[-1]:
            return True
        return False

    def sort_pattern_list(self):
        self.lte_pattern_list.sort(key=lambda pat: pat.get_score(), reverse=True)

    def check_duplicate(self):
        pattern_list = self.get_pattern_list_from_object()
        seen_pattern = []
        for pattern in pattern_list:
            if pattern in seen_pattern:
                return True
            seen_pattern.append(pattern)
        return False

    def get_pattern_list_from_object(self):
        pat_list = [pat_obj.item_list for pat_obj in self.lte_pattern_list]
        return pat_list

    def update_improper_supersequence(self, sequence: list):
        for pat in self.lte_pattern_list:
            if pat.is_improper_supersequence(sequence):
                pat.increment_support_count()  # increment support count
                pat.reset_freshness()  # reset freshness
                return True
        return False

    def update_proper_supersequence(self, sequence: list):
        ## here we can sort the patterns according to length since we're not updating anything in existing patterns
        for pat in sorted(self.lte_pattern_list, key=lambda x: x.get_pattern_len()):
            if pat.is_proper_supersequence(sequence):
                if not self.validate_items(sequence):
                    raise Exception('Cannot create LTEPattern object: list invalid!')
                newPattern = LTEPattern(sequence)  # new pattern
                # since the existing pattern is a supersequence of new sequence, it should already have its support
                newPattern.set_support_count(pat.get_support_count())
                newPattern.increment_support_count()  # increment support count
                newPattern.reset_freshness()  # reset freshness
                return True
        return False

    def update_phase(self, sequence: list):
        if sequence.__len__() == 0:
            raise Exception('Candidate list of size zero encountered!')
        if sequence.__len__() == 1:  # nothing to do
            return False
        ## increment freshness for all patterns
        for pat in self.lte_pattern_list:
            pat.increment_freshness()
        ## case 1: if the new sequence is same as one of the existing patterns
        if self.update_improper_supersequence(sequence):
            self.sort_pattern_list()
            assert not self.check_duplicate()
            return True
        ## case 2: if the new sequence is a subsequence of one of the existing patterns
        elif self.update_proper_supersequence(sequence):
            self.sort_pattern_list()
            assert not self.check_duplicate()
            return True
        ## case 3: if the new sequence is bigger than any existing patterns
        else:
            newPattern = LTEPattern(sequence)  # new pattern
            newPattern.increment_support_count()  # increment support count to 1
            newPattern.reset_freshness()  # reset freshness
            self.lte_pattern_list.append(newPattern)
            self.total_patterns += 1
            ## check if the new sequence is a supersequence of any existing patterns
            for pat in self.lte_pattern_list:
                if pat.is_proper_subsequence(sequence):
                    pat.increment_support_count()
                    pat.reset_freshness()
            self.sort_pattern_list()
            assert not self.check_duplicate()
            return True


class NSAProcedurePatterns:
    def __init__(self, procedure_type: str):
        self.procedure_type = procedure_type
        self.total_patterns = 0
        self.nsa_pattern_list: List[NSAPattern] = list()

    def __str__(self):
        patterns = [pat.__str__() for pat in self.nsa_pattern_list]
        return f"====== {self.procedure_type} =======\n {patterns}\n"

    def add_pattern(self, pattern: NSAPattern):
        self.nsa_pattern_list = self.nsa_pattern_list.append(pattern)
        self.total_patterns += 1

    def add_pattern_from_list(self, items: list, init_support=0):
        # validate items and then add
        if self.validate_items(items):
            self.nsa_pattern_list.append(NSAPattern(items, init_support))
            self.total_patterns += 1
        else:
            raise Exception('Cannot create NSAPattern object: list invalid!')

    def evict_pattern(self, threshold_fresh: int):
        self.nsa_pattern_list = [pat for pat in self.nsa_pattern_list
                                  if pat.is_fresh(self.total_patterns, threshold_fresh)]
        self.total_patterns = len(self.nsa_pattern_list)

    def validate_items(self, items: list):
        if NSAPattern.validate_items(items) and self.procedure_type == items[-1]:
            return True
        return False

    def sort_pattern_list(self):
        self.nsa_pattern_list.sort(key=lambda pat: pat.get_score(), reverse=True)

    def check_duplicate(self):
        pattern_list = self.get_pattern_list_from_object()
        seen_pattern = []
        for pattern in pattern_list:
            if pattern in seen_pattern:
                return True
            seen_pattern.append(pattern)
        return False

    def get_pattern_list_from_object(self):
        pat_list = [pat_obj.item_list for pat_obj in self.nsa_pattern_list]
        return pat_list

    def update_improper_supersequence(self, sequence: list):
        for pat in self.nsa_pattern_list:
            if pat.is_improper_supersequence(sequence):
                pat.increment_support_count()  # increment support count
                pat.reset_freshness()  # reset freshness
                return True
        return False

    def update_proper_supersequence(self, sequence: list):
        ## here we can sort the patterns according to length since we're not updating anything in existing patterns
        for pat in sorted(self.nsa_pattern_list, key=lambda x: x.get_pattern_len()):
            if pat.is_proper_supersequence(sequence):
                if not self.validate_items(sequence):
                    raise Exception('Cannot create NSAPattern object: list invalid!')
                newPattern = NSAPattern(sequence)  # new pattern
                ## since the existing pattern is a supersequence of new sequence, it should already have its support
                newPattern.set_support_count(pat.get_support_count())
                newPattern.increment_support_count()  # increment support count
                newPattern.reset_freshness()  # reset freshness
                return True
        return False

    def update_phase(self, sequence: list):
        if sequence.__len__() == 0:
            raise Exception('Candidate list of size zero encountered!')
        if sequence.__len__() == 1:  # nothing to do
            return False
        ## increment freshness for all patterns
        for pat in self.nsa_pattern_list:
            pat.increment_freshness()
        ## case 1: if the new sequence is same as one of the existing patterns
        if self.update_improper_supersequence(sequence):
            self.sort_pattern_list()
            assert not self.check_duplicate()
            return True
        ## case 2: if the new sequence is a subsequence of one of the existing patterns
        elif self.update_proper_supersequence(sequence):
            self.sort_pattern_list()
            assert not self.check_duplicate()
            return True
        ## case 3: if the new sequence is bigger than any existing patterns
        else:
            newPattern = NSAPattern(sequence)  # new pattern
            newPattern.increment_support_count()  # increment support count to 1
            newPattern.reset_freshness()  # reset freshness
            self.nsa_pattern_list.append(newPattern)
            self.total_patterns += 1
            ## check if the new sequence is a supersequence of any existing patterns
            for pat in self.nsa_pattern_list:
                if pat.is_proper_subsequence(sequence):
                    pat.increment_support_count()
                    pat.reset_freshness()
            self.sort_pattern_list()
            assert not self.check_duplicate()
            return True
