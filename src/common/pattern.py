class Pattern:
    MR_ITEMS = []
    PROCEDURE_ITEMS = []

    def __init__(self, items: list, init_support=0):
        self.item_list = list(items)  # add HOs to the end
        self.support_count = init_support  # we assume that this pattern has been observed once
        self.confidence_count = 0  # TODO: not using right now
        self.freshness = 0  # set freshness to zero if pattern encountered in this phase
        self.stale_threshold = 1000  # in milliseconds

    def __eq__(self, other):
        if isinstance(other, LTEPattern):
            if self.item_list == other.item_list:
                return True
        return False

    def __hash__(self):
        return ' '.join(self.item_list)

    def __str__(self):
        return f"[ Pattern: {self.item_list}; Support Count: {self.support_count}; " \
               f"Freshness: {self.freshness} ]"

    def get_pattern_len(self):
        return self.item_list.__len__()

    def get_score(self):
        return self.get_support_count() * self.get_pattern_len()

    def get_support_count(self):
        return self.support_count

    def get_confidence_count(self):
        return self.confidence_count

    def get_freshness(self):
        return self.freshness

    def increment_support_count(self):
        self.support_count += 1

    def set_support_count(self, support: int):
        self.support_count = support

    def increment_confidence_count(self):
        self.confidence_count += 1

    def increment_freshness(self):
        self.freshness += 1

    def reset_freshness(self):
        self.freshness = 0

    @classmethod
    def validate_items(cls, items: list):
        if items[-1] in cls.PROCEDURE_ITEMS:  # check if last item is of type procedure
            if all(item in cls.MR_ITEMS + cls.PROCEDURE_ITEMS
                   for item in items):  # check if all items are valid
                return True
        return False

    def is_fresh(self, total_patterns: int, thresh: int):
        if self.get_freshness() < total_patterns * thresh:
            return True
        return False

    def is_proper_supersequence(self, sequence: list):
        # new sequence is a subsequence of this pattern
        if self.item_list.__len__() > sequence.__len__() and self.item_list[-1 * sequence.__len__():] == list(sequence):
            return True
        return False

    def is_improper_supersequence(self, sequence: list):
        # new sequence is same as this pattern
        if self.item_list.__len__() == sequence.__len__() and self.item_list == list(sequence):
            return True
        return False

    def is_proper_subsequence(self, sequence: list):
        # new sequence is a supersequence of this pattern
        if self.item_list.__len__() < sequence.__len__() and \
                list(sequence[-1 * self.item_list.__len__():]) == self.item_list:
            return True
        return False


class LTEPattern(Pattern):
    MR_ITEMS = [
        'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'RS', 'CGI',  # LTE events
        'NRB1', 'NRB2',  # inter-RAT events
        ]
    PROCEDURE_ITEMS = [
        'pcell_intra', 'pcell_inter',  # LTE PCell mobility procedures
        'scga',  # NSA SCG mobility procedures
        ]

    def __init__(self, items: list, init_support=0):
        super().__init__(items, init_support)


class NSAPattern(Pattern):
    MR_ITEMS = ['NRA1', 'NRA2', 'NRA3']
    PROCEDURE_ITEMS = ['scgm', 'scgr']

    def __init__(self, items: list, init_support=0):
        super().__init__(items, init_support)


class SAPattern(Pattern):
    MR_ITEMS = ['NRA1', 'NRA2', 'NRA3']
    PROCEDURE_ITEMS = ['mcg_intra', 'mcg_inter']

    def __init__(self, items: list, init_support=0):
        super().__init__(items, init_support)
