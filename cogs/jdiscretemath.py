from discord.ext import commands
import random
import math
import json
import requests

class DiscreteMath(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.predicate_eng = [
            "The political canvasser posed a threat if and only if they arrived after the house cleaner, and if the house cleaner posed a threat, then the political canvasser also posed a threat and the house cleaner arrived before the political canvasser.",
            "If both the political canvasser and the house cleaner posed a threat, then the house cleaner arrived before the political canvasser.",
            "Either the canvasser or the house cleaner posed a threat, or the house cleaner arrived before the canvasser, and it was not the case that the house cleaner arrived before the canvasser and that the canvasser and the house cleaner both posed threats.",
            "Every visitor who was not driven away by Duncan did not arrive after the house cleaner.",
            "There was a visitor that was driven away by Duncan, and every visitor arrived before the house cleaner if and only if they were that visitor. Alternatively: There was exactly one visitor who arrived before the house cleaner, and they were driven away by Duncan.",
            "Every visitor who posed a threat was driven away by Duncan.",
            "Given any dog, Cardie joined the walk before it if and only if Duncan joined the walk before it.",
            "If Bingley joined the walk before Whistle, then Cardie joined before Guinness and Guinness joined before Bingley.",
            "Guinness joined the walk before Bingley, and either Bingley joined before Whistle, or Cardie joined before Guinness, but not both.",
            "Whistle joined the walk before at least two distinct other dogs.",
            "Every dog, except for Bingley himself, joined the walk before Bingley.",
            "It is not the case that for every dog, it joined the walk before Whistle or Bingley joined the walk before it. or There exists a dog who did not join the walk before Whistle and did not join the walk after Bingley",
            "It is not the case that if Duncan is no larger than Rio, then either Maya is no larger than Nina or Guinness is no larger than Cardie.",
            "It is not the case that either Maya is no larger than Nina or that it is not the case that Guinness is not no larger than Cardie and Duncan is no larger than Rio",
            "The relation NL is a total order. (This should be the AND of four quantified statements, one for each defining property of a total order.",
            "'There is a mastiff such that all dogs are no larger than it,' or 'The largest of the dogs is a mastiff.'",
            "Duncan is the one and only dog who is both no larger than Rio and no smaller than Nina.",
            "'For any dog, there is a different dog of the same breed if and only if the first dog is Maya or Nina,' or 'Maya and Nina each share a breed with a different dog, and no other dogs do,' or even 'Maya and Mina are the same breed, and all the other dogs are the only ones of their breed'.",
            "Every dog is no smaller than some poodle, and every dog is neither Cardie nor Guinness if and only if it is no larger than some poodle."
        ]
        self.predicate_symbols = [
            "(PT(pc) ↔ AB(hc, pc)) ∧ (PT(hc) → (PT(pc) ∧ AB(hc, pc)))",
            "(PT(pc) ∧ PT(hc)) → AB(hc, pc)",
            "(PT(pc) \lor PT(hc) \lor AB(hc, pc)) ∧ ¬(AB(hc, pc) ∧ PT(hc) ∧ PT(pc))",
            "∀ x:(¬DA(x)) → (¬AB(hc, x))",
            "∃ y:∀ z:DA(y)∧ (AB(z, hc) ↔ (y=z))",
            "∀ x:PT(x) → DA(x)",
            "∀ x: JB(c, x) ↔ JB(d, x)",
            "JB(b, c) →  (JB(c, g) ∧  JB(g, b))",
            "JB(g, b) ∧  (JB(b, w) ⊕ JB(c, g))",
            "∃ x:∃ y: JB(w, x) ∧  JB(w, y) ∧  (x ≠ y)",
            "∀ x: (x ≠ b) →  JB(x, b)",
            "¬(∀ y: JB(y, w) ∨ JB(b, y))",
            "¬(NL(d, r) →  (NL(m, n) ∨ NL(g, c)))",
            "¬(NL(m, n) ∨ ¬(¬NL(g, c) ∧  NL(d, r)))",
            "∀ x:∀ y:∀ z:NL(x, x) ∧  ((NL(x, y) ∧  NL(y, x)) →  (x = y)) ∧  ((NL(x, y) ∧  NL(y, z)) →  NL(x, z)) ∧  (NL(x, y) ∨ NL(y, x).",
            "∃ x: (f(x) = M) ∧  ∀ y: NL(y, x)",
            "∀ x: (NL(x, r) ∧  NL(n, x)) ↔ (x = d).",
            "∀ x: (∃ y: (f(x) = f(y)) ∧  (x ≠ y)) ↔ ((x = m) ∨ (x = n))",
            "∀ x: ∃ y:(f(y) = P) ∧  (NL(y, x)) ∧  (((x ≠ c) ∧  (x ≠ g)) ↔ ∃ z: NL(x, z) ∧  (f(z) = p))"
        ]
        self.predicate_context = [
            "One day there were exactly five visitors, arriving at five distinct times. In alphabetical order, they were an Amazon driver (ad), the house cleaner (hc), the mail person (mp). a political canvasser (pc), and a UPS driver (ud). \n Let PT and DA be two unary relations on V, such that PT(x) means 'visitor x posed a threat' and DA(x) means 'visitor x was driven away by Duncan'. Let AB be a binary relation on V, such that AB(x, y) means 'visitor x arrived before visitor y', or equivalently 'visitor y arrived after visitor x'.",
            "One day Cardie and Duncan were joined on their morning walk by several other dogs. The set S of dogs on this group walk included Bingley (b), Cardie (c), Duncan (d), Guinness (g), Whistle (w), and perhaps others. \n Let the binary predicate JB on S be defined so that JB(x, y) means 'dog x joined the walk before dog y'. Assume that the relation corresponding to JB is antireflexive, antisymmetric, and transitive.",
            "Let S be a finite set of dogs consisting of exactly the six distinct dogs Cardie (c), Duncan (d), Guinness (g), Maya (m), Nina (n), and Rio (c). \n Let B be a finite set of breeds consisting of exactly the six breeds Collie (C), Mastiff (M), Poodle (P), Retriever (R), Terrier (T), and Weimeraner (W). \n Let NL be the binary relation on S defined so that NL(x, y) means 'dog x is no larger than dog y'. We will also sometimes translate NL(x, y) as 'dog y is no smaller than dog x'. Although I didn't say this on the actual test, I should have encouraged you to translate ¬NL(x, y) as 'dog x is larger than dog y' or 'dog y is smaller than dog x'. \n Let f be the function from S to B defined so that 'f(x) = b' means 'the breed of dog x is b'."
        ]
        self.tf_question_2 = [
            "Any undirected graph with no cycles is a tree.",
            "Depth-first search is the same as uniform-cost search with costs of 1 on every edge.",
            "Let g(s) and h(s) be two admissible heuristic functions for an A* search of the same graph with the same target node. Then the average of the two, (1/2)(g(s) + h(s)), is also an admissible heuristic for that graph with that target node.",
            "The path relation on a directed graph may fail to be transitive.",
            "If a rooted tree has exactly one node, then its depth is 1.",
            "There exists a rooted binary tree T, with a positive even number of nodes, such that every internal node of T has exactly two children.",
            "Let G be a weighted directed graph with nodes s and t. Let C be a positive constant. It is possible that if we add C to the cost of evere edge in G, then we will change the path from s to t found by a uniform-cost search.",
            "Let P(n) be a predicate on naturals. If P(0) and P(1) are both true, and ∀n: P(n) → (P(2n) ∧ P(2n+1)) is true, then ∀n: P(n) must be true.",
            "Let Q(w) be a predicate on binary strings. It is possible that Q(λ) and ∀w: Q(w) → (Q(w0) ∧ Q(w1)) are both true, but that there exists a string v such that Q(v) is false.",
            "Let G be a directed graph and let s and t be nodes of G. If we do both a depth-first search and an A* of G with start node s and goal node t, then the A* search is guaranteed to expand no more nodes than the DFS.",
            "Let G be a strongly connected directed graph, and suppose we conduct a DFS of G from start node s. If we remove all the back edges from the resulting DFS tree, the remaining edges form an acyclic graph.",
            "Let (u, v) be a non-tree edge of the BFS tree of a strongly connected directed graph. If u is at level 5 of the tree, then it is possible that v is at level 2 or at level 6, but not possible that v is at level 7.",
            "The set of integers {0,1,2,3,4,5,6}, with successor, addition, and multiplication all defined modulo 7, does not model the Peano axioms.",
            "The following is not a valid recursive definition: Define f(0) = 0, and for n > 0, f(n) = 1 + f(n/2) if n is even, and f(n) = 3n + 1 if n is odd.",
            "Define g(x, 0) = 1 and g(x, 2k) = (g(x, k))2 for k > 0, g(x, 2k + 1) = x(g(x, 2k))2 for k ≥ 0. Then for all naturals k, g(x, n) = xn.",
            "If P(0) is true, and for all n ≥ 1, (P(n) → P(n+1)) ∧ (P(n-1) → P(n-1)), then ∀n: P(n) must be true.",
            "Define the relation G on naturals such that ∀x: G(S(x), 0) and ∀x: G(x, y) → G(S(x), S(y)), where S is the successor function. Then ∀x:∀y:∀z: G(x, y) → G(x+z, y+z).",
            "Let P be a property of strings over the alphabet {a, b, c}. If P(λ) is true, and P(w) → P(wx) is true for any string w and any letter x, then it is possible that P(w) is false for some w ∈ S.",
            "The set S of strings over the alphabet {a, b, c} is defined as follows: \n (1) λ is in S \n(2) if w is an even-length string in S and x is a letter, then wx is in S \n (3) if w is an odd-length string in S, x is a letter, and x ≠ last(w), then wx is in S \n (4) nothing else is in S \n \n If u and v are both strings of odd length in S, then the strings uv and vu are both in S.",
            "The set S of strings over the alphabet {a, b, c} is defined as follows: \n (1) λ is in S \n(2) if w is an even-length string in S and x is a letter, then wx is in S \n (3) if w is an odd-length string in S, x is a letter, and x ≠ last(w), then wx is in S \n (4) nothing else is in S \n \n If u and v are both strings of even length in S, then the strings uv and vu are also both in S.",
            "For any n > 1, there exists an undirected graph with n nodes and at least 2(n!) different simple cycles.",
            "An undirected graph with 6 nodes, 8 edges, and no isolated nodes must be connected.",
            "Consider a directed graph with five nodes, no self-loops, and an antisymmetric edge relation. It is possible for such a graph to contain two different strongly connected components, each with more than one node.",
            "There is exactly one way to add a + operator to the string '2 + 3 * 4 5' to make it a valid prefix expression string.",
            "For all n > 1, there exists an undirected graph G and a node v in G such that the BFS tree from v has depth 1 and the DFS tree from v has depth n - 1.",
            "In the BFS tree of a directed graph, there can be an edge from a node at level t to a node at level t + 2.",
            "If ∀n:P(n) can be proved by strong induction, then there exists a statement Q(n) such that ∀n:Q(n) can be proved by ordinary induction, and the statement ∀n:Q(n) → P(n) is true.",
            "Define the function f from binary strings to binary strings by the rules f(λ) = 0, f(w0) = f(w), and f(w1) = f(w)1. Then f(10010) = 011.",
            "The statement ∀x:S(0) + x = S(x), where S is the successor function, is not part of the definition of addition but can be proved from that definition using induction.",
            "If f(0) = 4 and f(n+1) = f(n) + n - 3 for every natural n, then f(n) = (n2 - 5n + 8)/2 for every natural n.",
            "The set {0, 1, 2, 3, 4, 5, 6}, with the successor function S(i) = (i+1)%7, does not satisfy the fifth Peano axiom for naturals.",
            "The operation of exponentiation on naturals, with E(x, y) = x^y, is neither commutative nor associative.",
            "If a binary string has odd length and has a first letter and a last letter that are different, it must contain either 00 or 11 as a substring.",
            "Let Σ be a nonempty finite alphabet with k letters. Then the number of strings in Σn that never have the same letter twice in a row is (k-1)kn-1.",
            "A rooted binary tree has a number of leaves equal to its number of internal nodes.",
            "A generic search may fail to terminate even if the search space is finite.",
            "The call tree of our recursive factorial method has n-1 leaves for any input n with n > 1.",
            "There exists a boolean expression (as in Discussion #7) with more operators than primitive expressions."
        ]
        self.tf_solution_2 = [
            "FALSE. It might not be connected.",
            "FALSE. BFS is the same as UCS with unit edge weights.",
            "TRUE. If both g(s) and h(s) are in the range from 0 to d(s, g), then so is their average.",
            "FALSE. We proved that it is transitive.",
            "FALSE. The depth is the length of the longest path from the root to a leaf, which in this case is 0.",
            "FALSE. The single node tree has an odd number of nodes, and adding exactly two children to any leaf keeps the number odd, so the number is always odd.",
            "TRUE. A simple example has three nodes and edges (s, x, 1), (s, t, 3), and (x, t, 1). The optimal path is two steps, but if we add 10 to every edge cost the one-edge path becomes optimal.",
            "TRUE. We have enough to prove ∀n:P(n) by strong induction.",
            "FALSE. These premises are enough to prove ∀w:Q(w).",
            "FALSE. The DFS could happen upon the shortest path immediately, while if the heuristic is zero and we have unit weights, A* becomes BFS, which will examine all paths from the start that are shorter than the shortest one to the goal.",
            "TRUE. Tree and forward edges only go from ancestors to descendants. And no sequence of cross edges can get from a descendant to an ancestor.",
            "TRUE. The edge can go to the following level, the same level, or any previous level, but if v were not yet discovered it would be at the next level after u’s.",
            "TRUE. Zero is the successor of a number (6), which the Peano Axioms forbid.",
            "FALSE. The value of f for every odd number is defined directly, and for any even number the recursion will continue until an odd number is reached. For example, f(12) = 1 + f(6) = 2 + f(3) = 2 + 10 = 12. This is somewhat similar to the definition of the Collatz sequence, the subject of a famous unsolved problem which you may look up on your own if you are interested.",
            "TRUE. This is the repeated squaring algorithm for computing powers -- we could prove the claim by induction on n, letting x be arbitrary.",
            "FALSE. P(1) does not follow from the given statements. We could let P(n) be 'n ≠ 1' and the premises would all be true, but the conclusion false.",
            "TRUE. These rules define G to be the 'greater than' predicate. We could prove the claim by induction on z, letting x and y be arbitrary and using only the second statement of the definition.",
            "FALSE. These premises are enough to prove P(w) for all strings w, not just those in S.",
            "FALSE. If u and v are both 'a', they are both in S but 'aa' isn't.",
            "TRUE. A string is in S if and only if it not of the form uaav, ubbv, or uccv where u is a string of even length. IF we concatenate two strings x and y each of even length, a double letter in in a bad position in x or y if and only if it is in a bad position in xy.",
            "TRUE. Let G be the complete graph. Any of the n! orderings of the n nodes leads to two distinct simple paths that are not cycles, one with n-1 edges and one of n-2 edges. For example, with n = 4 we can assign the ordering a-b-c-d to the path a-b-c-d and the path a-b-c (leaving out d). Neither of these are cycles because they do not begin and end at the same point. We should be a bit careful of the n = 2 case: there the four (2(2!)) paths are a-b, b-a, a, and b. The latter two are simple paths (since they don't reuse a vertex) and are not cycles because a cycle in an undirected graph must have at least three edges.",
            "TRUE. If it were not connected and had no isolated nodes, the connected components could be size 2 and 4, or size 3 and 3. (A graph with more than two connected components has fewer edges than one with two components, and we'll show these have too few edges.) A graph with 2 and 4 nodes in its components could have at most seven edges, and one with 3 and 3 could have at most six.",
            "FALSE. If x is a node in a directed graph with an asymmetric edge relation, and its component has more than one node, it must have an edge to another node y. Since y cannot have an edge back to x, there must be a least one other node in the component. So a graph with two such components must have at least six nodes.",
            "TRUE. A prefix expression string must begin with an operator, so the only place to put the + is at the beginning.",
            "TRUE. For n = 2, let the graph have one edge -- both trees have depth 1 which is fine because n = 1 = 1. For n = 3, let the graph be a triangle, so the DFS has depth 2 and the BFS has depth 1. For n > 3, let the graph be a cycle of n - 1 nodes together with a node v that shares an edge with every node of the cycle. (This is called a wheel graph and has 2n - 2 edges.) The BFS tree of the wheel clearly has depth 1 because every other node is distance 1 from v and thus goes on the first level. The DFS will have depth n - 1 because each node we encounter will have an unseen neighbor, until we have seen them all. (The DFS tree consists of a single path.)",
            "FALSE. If this happened, there would be a directed path of length t + 1 from the start node to the second node (using the path to the first node and the alleged edge from the first to the second), but this node would be on level t + 2. The level in a BFS tree is the length of the shortest path from the start node.",
            "TRUE. Q(n) can be taken to be the statement ∀i: (i ≤ n) → P(i). The inductive step of an ordinary induction proof of ∀n:Q(n) is just the strong inductive step for the strong induction proof of ∀n:P(n). And clearly Q(n) implies P(n) for any n, since we can specify the universal quantifier in Q(n) to i = n to get '(n ≤ n) → P(n)', which clearly implies P(n).",
            "TRUE. This function deletes all the zeroes in w, and places a single 0 at the start. This creates 011 from 10010.",
            "TRUE. The similar statement in the definition of addition is ∀x:∀y:x + S(y) = S(x + y).",
            "FALSE. I had intended this to be true, but got the numbers wrong. If the formula were true, f(0) would be 4 but f(1) would be (1 - 5 + 8)/2 = 2, while the recursive definiton gives f(1) = f(0) + 0 - 3 = 1. The correct closed form of this recurrence is (n2 - 7n + 8)/2.",
            "FALSE. The fifth axiom says that if you start at 0 and keep taking successors, you will reach all the numbers, and that is true in this system.",
            "TRUE. E(2, 3) ≠ E(3, 2), and E(2, E(3, 2)) ≠ E(E(2, 3), 2). I see that I asked this same question in Spring 2017.",
            "TRUE. If a string does not have either of those two substrings, it must alternate 0's and 1's, and so if it has odd length its first and last letter will be the same.",
            "FALSE. The correct number is k(k-1)n-1, because we may choose any of the k letters to start and then have k-1 choices for each subsequent letter. Actually I neglected to specify that n should be positive, so the statement is also false because it gives (k-1)/k instead of 1 for n = 0.",
            "FALSE. It has one more leaf than its number of internal nodes.",
            "TRUE. The generic search does not recognize previously seen nodes unless we say it does, so it could get caught in an infinite loop.",
            "FALSE. It has one leaf, because this method only calls itself at most once per iteration So the call tree has a single branch and a single leaf.",
            "TRUE. This would be false if there were only binary operators, but the expression 'NOT NOT 0', for example, has two operators and only one primitive expression."
        ]

    def exp_latex(self, dat):
        sent = {
            'auth': { 
                'user': "guest", 
                'password': "guest" 
            },
            'latex': dat,
            'resolution': 600,
            'color': "D53131",
	    }
        json.dumps(sent)
        req = requests.post('http://www.latex2png.com/api/convert', json=sent).json()
        try:
            return f'http://www.latex2png.com{req["url"]}'
        except KeyError:
            return f"Error: {req['result-message']})"

    def modinv(self, a, m):
        def egcd(a, b):
            if a == 0:
                return (b, 0, 1)
            g, y, x = egcd(b % a, a)
            return (g, x - (b // a) * y, y)

        g, x, y = egcd(a, m)
        if g != 1:
            raise ValueError(f'{a} has no inverse modulo {m}')
        return [x % m, g]

    def build_predicate_problem(self, to_symbols=True):
        idx = random.randint(0, len(self.predicate_eng) - 1)
        return f'{self.predicate_context[idx // 6]} \n \n Translate the following into {"symbols" if to_symbols else "English"}: \n {self.predicate_eng[idx] if to_symbols else self.predicate_symbols[idx]} \n \n ||{self.predicate_symbols[idx] if to_symbols else self.predicate_eng[idx]}||'

    def build_tf_problem(self):
        if(len(self.tf_question_2) != len(self.tf_solution_2)):
            return "Error: Question and solution arrays have different length."
        idx = random.randint(0, len(self.tf_question_2) - 1)
        return f"True or False: \n {self.tf_question_2[idx]} \n \n Solution: \n ||{self.tf_solution_2[idx]}||"

    @commands.command()
    async def modular_inverse(self, ctx, a, m):
        await ctx.send(self.modinv(a, m))

    @commands.command()
    async def ets(self, ctx):
        await ctx.send(self.build_predicate_problem())

    @commands.command()
    async def ste(self, ctx):
        await ctx.send(self.build_predicate_problem(to_symbols=False))

    @commands.command()
    async def tf(self, ctx):
        await ctx.send(self.build_tf_problem())

    @commands.command()
    async def crt(self, ctx, a1, m1, a2, m2, a3, m3):
        t = self.exp_latex(self.generate_problem(ctx, a1, m1, a2, m2, a3, m3))
        await ctx.send(t)
        
    def generate_problem(self, ctx, a1, m1, a2, m2, a3, m3):
        a_1 = int(a1)
        m_1 = int(m1)
        a_2 = int(a2)
        m_2 = int(m2)
        a_3 = int(a3)
        m_3 = int(m3)
        M = m_1 * m_2 * m_3
        M_m_1 = int(M / m_1)
        M_m_2 = int(M / m_2)
        M_m_3 = int(M / m_3)
        n_1  = 0
        n_2 = 0
        n_3 = 0
        try: 
            n_1 = self.modinv(M_m_1, m_1)
            n_2 = self.modinv(M_m_2, m_2)
            n_3 = self.modinv(M_m_3, m_3)
        except ValueError:
            return "\\text{One of these modular inverses does not exist.}"
        c = a_1 * n_1 * M_m_1 + a_2 * n_2 * M_m_2 + a_3 * n_3 * M_m_3
        out = f'''
        \\textbf{{Using the CRT, find a single congruence equivalent to
        the following system of congruences}}: \\\\ x \equiv {a1} \pmod{{{m1}}},
        x \equiv {a2} \pmod{{{m2}}} \\text{{ and }} x \equiv {a3} \pmod{{{m3}}}. \\\\ \\\\
        \\textbf{{Solution}} \\\\
        \\text{{Let }} a_1 = {a1} \\text{{ and }} m_1 = {m1}. \\text{{ Let }} a_2 = {a2} \\text{{ and }} m_2 = {m2}.
        \\text{{ Let }} a_3 = {a3} \\text{{ and }} m_3 = {m3}. \\\\ 
        \\text{{From this we can see that }} M = {m1} \cdot {m2} \cdot {m3} = {M}, \\text{{so }} \\frac{{M}}{{m_1}} =
        {M_m_1}, \\frac{{M}}{{m_2}} = {M_m_2}, \\text{{and }} \\frac{{M}}{{m_3}} = {M_m_3}. \\\\
        \\text{{We can now use the Euclidean Algorithm to determine that }} n_1 = {n_1},
        n_2 = {n_2}, \\text{{and }} n_3 = {n_3}. \\\\ \\text{{From this it follows that }}
        c = {a1} \cdot {n_1} \cdot {M_m_1} + {a2} \cdot {n_2}
        \cdot {M_m_2} + {a3} \cdot {n_3} \cdot {M_m_3} = {c}, \\text{{ so a
        solution is }} x \equiv {c} \pmod{{{M}}}.
        '''
        return out
 
def setup(bot):
    bot.add_cog(DiscreteMath(bot))
    
