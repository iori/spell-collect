# coding=utf8
import MeCab, collections, pprint

def words(text):
    mecab = MeCab.Tagger("mecabrc")
    node = mecab.parseToNode(text)
    words = []
    while node:
        if (node.posid >= 36) and (node.posid <= 67): # 名詞のみ
            words.append(node.surface.lower())
        node = node.next
    return words

def train(features):
    model = collections.defaultdict(lambda: 1) # スムージング.未知の語を1とする
    for f in features:
        model[f] += 1 # count
    return model

def debug_print(j_list): # 日本語を含むリストを文字化けせずに表示させる
    print "\n".join("%s: %s" % i for i in j_list.items())

NWORDS = train(words(file('big_j.txt').read())) # 単語と出現数
debug_print(NWORDS)

alphabet = 'abcdefghijklmnopqrstuvwxyz'

# 与えられた語 w に対して可能な修正語 c を列挙する
def edits1(word):
    n = len(word)
    return set([word[0:i]+word[i+1:] for i in range(n)] +                  # deletion      削除:文字を取り除く
            [word[0:i]+word[i+1]+word[i]+word[i+2:] for i in range(n-1)] + # transposition 転位:隣あう文字を入れ替える
            [word[0:i]+c+word[i+1:] for i in range(n) for c in alphabet] + # alteration    置換:一つの文字を別の文字に置き換える
            [word[0:i]+c+word[i:] for i in range(n+1) for c in alphabet])  # insertion     挿入:文字の追加

# 編集距離2
def known_edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)

def known(words): return set(w for w in words if w in NWORDS)

def correct(word):
    candidates = known([word]) or known(edits1(word)) or known_edits2(word) or [word]
    return max(candidates, key=lambda w: NWORDS[w])
