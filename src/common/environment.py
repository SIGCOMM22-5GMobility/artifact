import pandas as pd
from sklearn.metrics import f1_score, recall_score, precision_score, accuracy_score

try:
    from procedure_store import LTEProcedureStore, NSAProcedureStore
except ImportError:
    from .procedure_store import LTEProcedureStore, NSAProcedureStore


class Environment:
    def __init__(self, lte_initial_pattern_list=None, nsa_initial_pattern_list=None,
                 debug=True, log_path=None):
        self.lte_procedure_store = LTEProcedureStore(_max_items=4, _threshold_fresh=2, _debug=debug)
        self.nsa_procedure_store = NSAProcedureStore(_max_items=4, _threshold_fresh=2, _debug=debug)
        self.lte_prediction_results = []
        self.nsa_prediction_results = []
        self.lte_stats_df = None
        self.nsa_stats_df = None
        self.log_path = log_path
        if lte_initial_pattern_list is not None:
            self.lte_procedure_store.initialize_store(lte_initial_pattern_list)
        if nsa_initial_pattern_list is not None:
            self.nsa_procedure_store.initialize_store(nsa_initial_pattern_list)

    @staticmethod
    def generate_mr_subsequences(sequence_list: list):
        if sequence_list.__len__() < 2:
            raise Exception('Learning sequence of invalid length encountered!')
        subsequences = []
        for i in range(len(sequence_list) - 1):
            if i == len(sequence_list) - 2:
                mr_ho_pair = (list(sequence_list[:i + 1]), sequence_list[-1])
            else:
                mr_ho_pair = (list(sequence_list[:i + 1]), "no")
            subsequences.append(mr_ho_pair)
        return subsequences

    def analyse_results(self):
        self.lte_stats_df = pd.DataFrame(self.lte_prediction_results,
                                         columns=['result', 'prediction', 'sequence', 'truth_value'])
        self.nsa_stats_df = pd.DataFrame(self.nsa_prediction_results,
                                         columns=['result', 'prediction', 'sequence', 'truth_value'])

    def print_results_lte(self):
        f1 = f1_score(self.lte_stats_df['truth_value'], self.lte_stats_df['prediction'], average='weighted')
        recall = recall_score(self.lte_stats_df['truth_value'], self.lte_stats_df['prediction'], average='weighted')
        precision = precision_score(self.lte_stats_df['truth_value'], self.lte_stats_df['prediction'],
                                    average='weighted')
        accuracy = accuracy_score(self.lte_stats_df['truth_value'], self.lte_stats_df['prediction'])
        print(f"[Results] -> F1-score: {f1:.3f} Recall: {recall:.3f}  "
              f"Precision: {precision:.3f}  Accuracy: {accuracy:.3f}")
        self.lte_stats_df.to_csv(f'{self.log_path}_lte.csv', header=True, index=False)
        
    def print_results_nsa(self):
        f1 = f1_score(self.nsa_stats_df['truth_value'], self.nsa_stats_df['prediction'], average='weighted')
        recall = recall_score(self.nsa_stats_df['truth_value'], self.nsa_stats_df['prediction'], average='weighted')
        precision = precision_score(self.nsa_stats_df['truth_value'], self.nsa_stats_df['prediction'],
                                    average='weighted')
        accuracy = accuracy_score(self.nsa_stats_df['truth_value'], self.nsa_stats_df['prediction'])
        print(f"[Results] -> F1-score: {f1:.3f} Recall: {recall:.3f}  "
              f"Precision: {precision:.3f}  Accuracy: {accuracy:.3f}")
        self.nsa_stats_df.to_csv(f'{self.log_path}_nsa.csv', header=True, index=False)

    def run_lte(self, lte_sequence_list: list):
        for sequence in lte_sequence_list:
            #  for mr-subsequence in sequence, predict HO
            subsequences_ho = Environment.generate_mr_subsequences(sequence)
            for subsequence in subsequences_ho:
                prediction = self.lte_procedure_store.predict_ho(subsequence[0])
                self.lte_prediction_results.append([prediction == subsequence[1], prediction,
                                                    subsequence[0], subsequence[1]])
            self.lte_procedure_store.update_phase(sequence)
        self.analyse_results()
        self.print_results_lte()

    def run_nsa(self, nsa_sequence_list: list):
        for sequence in nsa_sequence_list:
            #  for mr-subsequence in sequence, predict HO
            subsequences_ho = Environment.generate_mr_subsequences(sequence)
            for subsequence in subsequences_ho:
                prediction = self.nsa_procedure_store.predict_ho(subsequence[0])
                self.nsa_prediction_results.append([prediction == subsequence[1], prediction,
                                                    subsequence[0], subsequence[1]])
            self.nsa_procedure_store.update_phase(sequence)
        self.analyse_results()
        self.print_results_nsa()
