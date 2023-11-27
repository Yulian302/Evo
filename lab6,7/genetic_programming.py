import random
from collections import deque
from genetic_operators import *
import numpy as np


class GeneticExpressionTree:
    def __init__(self,
                 functions: dict[str, Operator],
                 terminals: list[str],
                 head_len: int,
                 max_arity: int,
                 num_genes: int,
                 linker: TreeLinker,
                 mutation_prob: float,
                 move_max_len: int,
                 move_is_elements_prob: float,
                 move_ris_elements_prob: float):
        # class assign
        self.functions = functions
        self.terminals = set(terminals)
        self.head_len = head_len
        self.tail_len = head_len * (max_arity - 1) + 1
        self.gene_len = self.head_len + self.tail_len
        self.num_genes = num_genes
        self.linker = linker
        self.mutation_prob = mutation_prob
        self.move_max_len = move_max_len
        self.move_is_elements_prob = move_is_elements_prob
        self.move_ris_elements_prob = move_ris_elements_prob
        self._functions = list(functions.keys())
        self._terminals = terminals
        self._functions_terminals = self._functions + self._terminals
        self._validation_terminal_values = {self._terminals[i]: 0 for i in range(0, len(self._terminals))}

    def _eval_k_expression(self, k_expression: str, terminal_values: dict[str, float]) -> float:
        try:
            k_expression_valid = self.eval_cycle(k_expression)
            queue = deque()
            for primitive in list(k_expression_valid):
                if primitive in self.terminals:
                    queue.append(terminal_values[primitive])
                if primitive in self.functions.keys():
                    num_args = self.functions[primitive].get_args_num
                    operands = []
                    for _ in range(0, num_args):
                        operands.append(queue.popleft())
                    operands.reverse()
                    queue.append(self.functions[primitive].eval(operands))
            return queue.pop()
        except:
            return 0

    def evaluate_expression(self, gen_expr, terminals):
        if self.linker == TreeLinker.SUM:
            return sum([self._eval_k_expression(k_expr, terminals) for k_expr in gen_expr])
        if self.linker == TreeLinker.MAX:
            return max([self._eval_k_expression(k_expr, terminals) for k_expr in gen_expr])
        if self.linker == TreeLinker.MIN:
            return max([self._eval_k_expression(k_expr, terminals) for k_expr in gen_expr])

    def _rnd_gen_expr(self):
        return [random.choice(list(self._functions))
                + ''.join(random.choice(self._functions_terminals) for _ in range(1, self.head_len))
                + ''.join(random.choice(self._terminals) for _ in range(0, self.tail_len))
                for _ in range(0, self.num_genes)]

    def generate_genetic_expression(self):
        while True:
            ge = self._rnd_gen_expr()
            try:
                self.evaluate_expression(ge, self._validation_terminal_values)
                return ge
            except:
                continue

    def eval_fitness(self, genetic_expression: list[str], value_pairs):
        fitness_score = 0
        for value_pair in value_pairs:
            terminal_values = {self._terminals[i]: value_pair[0][i] for i in range(0, len(value_pair[0]))}
            fitness_score += abs(self.evaluate_expression(genetic_expression, terminal_values) - value_pair[1])
        return 1 / fitness_score if fitness_score != 0 else 0

    def eval_fitness_scores(self,
                            genetic_expressions: list[list[str]],
                            value_pairs):
        return [self.eval_fitness(ge, value_pairs)
                for ge in genetic_expressions]

    def eval_cycle(self, k_expression):
        k_expression_valid = deque()
        i, num_args = 0, 0
        while i < len(k_expression):
            primitive = k_expression[i]
            if primitive in self.functions.keys():
                num_args += self.functions[primitive].get_args_num
            k_expression_valid.appendleft(primitive)
            if num_args == 0:
                break
            else:
                num_args -= 1
            i += 1
        return k_expression_valid

    def _mutation(self,
                  genetic_expression: list[str]):
        for i in range(0, self.num_genes):
            gene = genetic_expression[i]
            index = random.randint(0, self.gene_len - 1)
            if index == 0:
                genetic_expression[i] = random.choice(self._functions) + gene[index + 1:]
            elif index < self.head_len:
                genetic_expression[i] = gene[:index] + random.choice(self._functions_terminals) + gene[index + 1:]
            else:
                genetic_expression[i] = gene[:index] + random.choice(self._terminals) + gene[index + 1:]

    def _move_is_elements(self,
                          genetic_expression: list[str]):
        f_gene_index = random.randint(0, self.num_genes - 1)
        s_gene_index = random.randint(0, self.num_genes - 1)
        while f_gene_index == s_gene_index:
            s_gene_index = random.randint(0, self.num_genes - 1)
        f_gene = genetic_expression[f_gene_index]
        s_gene = genetic_expression[s_gene_index]
        sequence_len = random.randint(1, self.move_max_len)
        move_from = random.randint(1, self.gene_len - 1 - sequence_len)
        move_to = random.randint(1, self.head_len - 1 - sequence_len)
        s_gene = s_gene[:move_to] + f_gene[move_from:move_from + sequence_len] + s_gene[move_to + sequence_len:]
        genetic_expression[s_gene_index] = s_gene

    @staticmethod
    def _select(
            genetic_expressions: list[list[str]],
            fitness_scores: list[float],
            n_ges):
        print(np.divide(fitness_scores, sum(fitness_scores)))
        return [random.choices(genetic_expressions, np.divide(fitness_scores, sum(fitness_scores)))[0]
                for _ in range(0, n_ges)]

    def _move_ris_elements(self,
                           genetic_expression: list[str]):
        f_gene_index = random.randint(0, self.num_genes - 1)
        s_gene_index = random.randint(0, self.num_genes - 1)
        while f_gene_index == s_gene_index:
            s_gene_index = random.randint(0, len(genetic_expression) - 1)
        f_gene = genetic_expression[f_gene_index]
        s_gene = genetic_expression[s_gene_index]
        sequence_len = random.randint(1, self.move_max_len)
        move_from = random.randint(1, self.head_len - 1 - sequence_len)
        while f_gene[move_from] not in self.functions:
            move_from = random.randint(1, self.head_len - 1 - sequence_len)
        s_k_expr = f_gene[move_from:move_from + sequence_len] + s_gene[sequence_len:]
        genetic_expression[s_gene_index] = s_k_expr

    def _one_point_recombination(self,
                                 f_ge: list[str],
                                 s_ge: list[str]):
        _r_f_ge, _r_s_ge = [], []
        f_ge_str = ''.join(f_ge)
        s_ge_str = ''.join(s_ge)
        index = random.randint(0, self.num_genes * self.gene_len - 1)
        r_f_ge_str = f_ge_str[:index] + s_ge_str[index:]
        r_s_ge_str = s_ge_str[:index] + f_ge_str[index:]
        i = self.gene_len
        while i < self.num_genes * self.gene_len + 1:
            _r_f_ge.append(r_f_ge_str[i - self.gene_len:i])
            _r_s_ge.append(r_s_ge_str[i - self.gene_len:i])
            i += self.gene_len
        return [_r_f_ge, _r_s_ge]

    def _two_points_recombination(self,
                                  f_ge: list[str],
                                  s_ge: list[str]):
        r_f_ge, r_s_ge = [], []
        f_ge_str = ''.join(f_ge)
        s_ge_str = ''.join(s_ge)
        f_index = random.randint(0, self.num_genes * self.gene_len - 2)
        s_index = random.randint(f_index + 1, self.num_genes * self.gene_len - 1)
        r_f_ge_str = f_ge_str[:f_index] + s_ge_str[f_index:s_index] + f_ge_str[s_index:]
        r_s_ge_str = s_ge_str[:f_index] + f_ge_str[f_index:s_index] + s_ge_str[s_index:]
        i = self.gene_len
        while i < self.num_genes * self.gene_len + 1:
            r_f_ge.append(r_f_ge_str[i - self.gene_len:i])
            r_s_ge.append(r_s_ge_str[i - self.gene_len:i])
            i += self.gene_len
        return [r_f_ge, r_s_ge]

    def _recombination(self,
                       f_ge: list[str],
                       s_ge: list[str]):
        # full recombination
        gene_index = random.randint(0, self.num_genes - 1)
        r_f_ge = f_ge.copy()
        r_s_ge = s_ge.copy()
        r_f_ge[gene_index] = s_ge[gene_index]
        r_s_ge[gene_index] = f_ge[gene_index]
        return [r_f_ge, r_s_ge]

    def train(self, a_F, n_gen_expr, epochs):
        genetic_expressions = [self.generate_genetic_expression() for _ in range(0, n_gen_expr)]
        fitness_scores = self.eval_fitness_scores(genetic_expressions, a_F)
        best_ge = genetic_expressions[np.argmax(fitness_scores)]
        for _ in range(0, epochs):
            if random.random() < self.move_ris_elements_prob:
                self._move_ris_elements(random.choice(genetic_expressions))
            if random.random() < self.mutation_prob:
                self._mutation(random.choice(genetic_expressions))
            if random.random() < self.move_is_elements_prob:
                self._move_is_elements(random.choice(genetic_expressions))
            parents = random.sample(genetic_expressions, 2)
            offsprings = self._one_point_recombination(parents[0], parents[1])
            genetic_expressions.extend(offsprings)
            parents = random.sample(genetic_expressions, 2)
            offsprings = self._recombination(parents[0], parents[1])
            genetic_expressions.extend(offsprings)
            parents = random.sample(genetic_expressions, 2)
            offsprings = self._two_points_recombination(parents[0], parents[1])
            genetic_expressions.extend(offsprings)
            fitness_scores = self.eval_fitness_scores(genetic_expressions, a_F)
            genetic_expressions = GeneticExpressionTree._select(genetic_expressions, fitness_scores, n_gen_expr)
            best_result = max(genetic_expressions, key=lambda ge: self.eval_fitness(ge, a_F))
            if self.eval_fitness(best_result, a_F) > self.eval_fitness(best_ge, a_F):
                best_ge = best_result
                mae_ = 0
                for vp in a_F:
                    prediction = self.evaluate_expression(best_ge, {'a': vp[0][0]})
                    mae_ += abs(vp[1] - prediction)
                print(f'MAE: {mae_ / len(a_F)}')
        return best_ge

    def restore_expr(self,
                     genetic_expression: list[str]):
        restored_expression = []
        for k_expression in genetic_expression:
            k_expression_valid = self.eval_cycle(k_expression)
            restored_expression.append(''.join(list(reversed([*k_expression_valid]))))
        return {'expression': restored_expression, 'linker': self.linker}
