try:
    from procedure import LTEProcedurePatterns, NSAProcedurePatterns
except ImportError:
    from .procedure import LTEProcedurePatterns, NSAProcedurePatterns

try:
    from pattern import LTEPattern, NSAPattern
except ImportError:
    from .pattern import LTEPattern, NSAPattern


class LTEProcedureStore:

    def __init__(self, _max_items=3, _threshold_fresh=5, _debug=True):
        self.max_items = _max_items  # including Procedure item
        self.threshold_fresh = _threshold_fresh
        self.debug = _debug
        self.current_phase = 0
        self.procedure_dict = {procedure: LTEProcedurePatterns(procedure) for procedure
                               in LTEPattern.PROCEDURE_ITEMS}

    def __str__(self):
        procedure_patterns = [procedure.__str__() for procedure in self.procedure_dict.values()]
        return f"\n\n \t\t\t Procedure Store State\n {procedure_patterns}"

    def increment_phase(self):
        self.current_phase += 1

    def initialize_store(self, pattern_object_list: list):
        for pattern_object in pattern_object_list:
            if pattern_object[0][-1] not in LTEPattern.PROCEDURE_ITEMS:  # make sure procedure is of valid type
                raise Exception('Invalid procedure type encountered!')
            ## make sure item_list is not greater than max_items
            if pattern_object[0].__len__() > self.max_items:
                pattern_object[0] = pattern_object[0][-1 * self.max_items:]
            self.procedure_dict[pattern_object[0][-1]].add_pattern_from_list(pattern_object[0], pattern_object[1])

    def predict_ho(self, item_list: list):
        ## make sure item_list is not greater than max_items
        if item_list.__len__() > self.max_items - 1:  # since HO type has been removed
            item_list = item_list[-1 * self.max_items - 1:]
        for procedure_name, procedure_object in self.procedure_dict.items():
            for pattern in procedure_object.lte_pattern_list:
                if pattern.is_improper_supersequence(item_list + [procedure_object.procedure_type]):
                    return procedure_object.procedure_type
        return "no"

    def update_phase(self, item_list: list):
        if item_list[-1] not in LTEPattern.PROCEDURE_ITEMS:  # make sure procedure is of valid type
            raise Exception('Invalid procedure type encountered!')
        ## make sure item_list is not greater than max_items
        if item_list.__len__() > self.max_items:
            item_list = item_list[-1 * self.max_items:]
        ## update phase for respective procedure type
        if not self.procedure_dict[item_list[-1]].update_phase(item_list):
            print(f"( phase: {self.current_phase}; new sequence: {item_list} ==> no action taken")
        ## evict patterns if any
        self.procedure_dict[item_list[-1]].evict_pattern(self.threshold_fresh)
        ## increment phase
        self.increment_phase()
        ## print database if debugging enabled
        if self.debug:
            print(f"( phase: {self.current_phase}; new sequence: {item_list}")
            print(self)


class NSAProcedureStore:

    def __init__(self, _max_items=3, _threshold_fresh=3, _debug=True):
        self.max_items = _max_items  # including Procedure item
        self.threshold_fresh = _threshold_fresh
        self.debug = _debug
        self.current_phase = 0
        self.procedure_dict = {procedure: NSAProcedurePatterns(procedure) for procedure
                               in NSAPattern.PROCEDURE_ITEMS}  # Dict[str, NSAProcedurePatterns]

    def __str__(self):
        procedure_patterns = [procedure.__str__() for procedure in self.procedure_dict.values()]
        return f"\n\n \t\t\t Procedure Store State\n {procedure_patterns}"

    def increment_phase(self):
        self.current_phase += 1

    def initialize_store(self, pattern_object_list: list):
        for pattern_object in pattern_object_list:
            if pattern_object[0][-1] not in NSAPattern.PROCEDURE_ITEMS:  # make sure procedure is of valid type
                raise Exception('Invalid procedure type encountered!')
            ## make sure item_list is not greater than max_items
            if pattern_object[0].__len__() > self.max_items:
                pattern_object[0] = pattern_object[0][-1 * self.max_items:]
            self.procedure_dict[pattern_object[0][-1]].add_pattern_from_list(pattern_object[0], pattern_object[1])

    def predict_ho(self, item_list: list):
        ## make sure item_list is not greater than max_items
        if item_list.__len__() > self.max_items - 1:  # since HO type has been removed
            item_list = item_list[-1 * self.max_items - 1:]
        for procedure_name, procedure_object in self.procedure_dict.items():
            for pattern in procedure_object.nsa_pattern_list:
                if pattern.is_improper_supersequence(item_list + [procedure_object.procedure_type]):
                    return procedure_object.procedure_type
        return "no"

    def update_phase(self, item_list: list):
        ## make sure procedure is of valid type
        if item_list[-1] not in NSAPattern.PROCEDURE_ITEMS:
            raise Exception('Invalid procedure type encountered!')
        ## make sure item_list is not greater than max_items
        if item_list.__len__() > self.max_items:
            item_list = item_list[-1 * self.max_items:]
        ## update phase for respective procedure type
        if not self.procedure_dict[item_list[-1]].update_phase(item_list):
            print(f"( phase: {self.current_phase}; new sequence: {item_list} ==> no action taken")
        ## evict patterns if any
        self.procedure_dict[item_list[-1]].evict_pattern(self.threshold_fresh)
        ## increment phase
        self.increment_phase()
        ## print database if debugging enabled
        if self.debug:
            print(f"( phase: {self.current_phase}; new sequence: {item_list}")
            print(self)
