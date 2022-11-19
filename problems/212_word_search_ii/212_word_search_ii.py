"""
Given an m x n board of characters and a list of strings words, return all words on the board.

Each word must be constructed from letters of sequentially adjacent cells, where adjacent cells are horizontally or vertically neighboring. The same letter cell may not be used more than once in a word.
"""


class Trie:
    def __init__(self, words=None):
        self.root = {}
        for word in words:
            self.add(word)

    def add(self, word):
        node = self.root
        for w in word:
            if w not in node:
                node[w] = {}
            node = node[w]
        node['$'] = word


class Solution:
    def __init__(self):
        self.ans = []

    def search(self, r, c, board, nrows, ncols, parent):

        char = board[r][c]
        cur_node = parent[char]

        # remove word once we get to it
        word_match = cur_node.pop('$', False)

        if word_match:
            self.ans.append(word_match)

        board[r][c] = '#'
        # we have to delete the word element after we use it
        # can't return here because some words like oa and oaa could be in there

        for nr, nc in ((r, c+1), (r+1, c), (r, c-1), (r-1, c)):
            if not (0 <= nr < nrows and 0 <= nc < ncols):
                continue
            if not board[nr][nc] in cur_node:
                continue

            self.search(nr, nc, board, nrows, ncols, cur_node)

        board[r][c] = char

        if not cur_node:
            """
            After we found a word and removed the '$' symbol then we
            cur_node is empty. Remove the parent node

            this speeds up the case when the list of target words space is >> than the
            number of words on the board
            """
            parent.pop(char)

    def findWords(self, board: List[List[str]], words: List[str]) -> List[str]:
        nrows, ncols = len(board), len(board[0]) if board else 0

        trie = Trie(words)
        for r in range(nrows):
            for c in range(ncols):
                if board[r][c] in trie.root:
                    self.search(r, c, board, nrows, ncols, trie.root)

        return self.ans
