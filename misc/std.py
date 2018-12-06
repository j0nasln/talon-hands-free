from talon.voice import Word, Context, Key, Rep, RepPhrase, Str, press
from talon import ctrl, clip
from talon_init import TALON_HOME, TALON_PLUGINS, TALON_USER
import string

from ..utils import parse_word, surround, text, sentence_text, word, parse_words
from .basic_keys import alpha_alt


def rot13(i, word, _):
    out = ""
    for c in word.lower():
        if c in string.ascii_lowercase:
            c = chr((((ord(c) - ord("a")) + 13) % 26) + ord("a"))
        out += c
    return out

formatters = {
    "allcaps": (False, lambda i, word, _: word.upper()),
    
    #PROGRAMMING---
    "dunder": (True, lambda i, word, _: "__%s__" % word if i == 0 else word),
    "camel": (True, lambda i, word, _: word if i == 0 else word.capitalize()),
    "snake": (True, lambda i, word, _: word if i == 0 else "_" + word),
    "smash": (True, lambda i, word, _: word),
    # spinal or kebab?
    "kebab": (True, lambda i, word, _: word if i == 0 else "-" + word),
    # 'sentence':  (False, lambda i, word, _: word.capitalize() if i == 0 else word),
    "title": (False, lambda i, word, _: word.capitalize()),
    "dubstring": (False, surround('"')),
    "string": (False, surround("'")),
    "padded": (False, surround(" ")),
    "rot-thirteen": (False, rot13),
}


def FormatText(m):
    fmt = []
    for w in m._words:
        if isinstance(w, Word) and w != "over":
            fmt.append(w.word)
    words = parse_words(m)
    if not words:
        with clip.capture() as s:
            press("cmd-c")
        words = s.get().split(" ")
        if not words:
            return

    tmp = []
    spaces = True
    for i, word in enumerate(words):
        word = parse_word(word).lower()
        for name in reversed(fmt):
            smash, func = formatters[name]
            word = func(i, word, i == len(words) - 1)
            spaces = spaces and not smash
        tmp.append(word)
    words = tmp

    sep = " "
    if not spaces:
        sep = ""
    Str(sep.join(words))(None)

ctx = Context("input")

ctx.keymap(
    {
        "phrase <dgndictation> [over]": text,
        "sentence <dgndictation> [over]": sentence_text,
        "comma <dgndictation> [over]": [", ", text],
        "period <dgndictation> [over]": [". ", sentence_text],
        # "more <dgndictation> [over]": [" ", text],
        "word <dgnwords>": word,
        "(%s)+ <dgndictation> [over]" % (" | ".join(formatters)): FormatText,
        
        "slap": [Key("cmd-right enter")],
        
        "(dubquote | double quote)": '"',
        "triple quote": "'''",
        
        #PROGRAMMING----
        "(dot dot | dotdot)": "..",
        "cd talon home": "cd {}".format(TALON_HOME),
        "cd talon user": "cd {}".format(TALON_USER),
        "cd talon plugins": "cd {}".format(TALON_PLUGINS),
        
        "run make (durr | dear)": "mkdir ",
        "run get": "git ",
        "run get (R M | remove)": "git rm ",
        "run get add": "git add ",
        "run get bisect": "git bisect ",
        "run get branch": "git branch ",
        "run get checkout": "git checkout ",
        "run get clone": "git clone ",
        "run get commit": "git commit ",
        "run get diff": "git diff ",
        "run get fetch": "git fetch ",
        "run get grep": "git grep ",
        "run get in it": "git init ",
        "run get log": "git log ",
        "run get merge": "git merge ",
        "run get move": "git mv ",
        "run get pull": "git pull ",
        "run get push": "git push ",
        "run get rebase": "git rebase ",
        "run get reset": "git reset ",
        "run get show": "git show ",
        "run get status": "git status ",
        "run get tag": "git tag ",
        "run (them | vim)": "vim ",
        "run L S": "ls\n",
        "dot pie": ".py",
        "run make": "make\n",
        "run jobs": "jobs\n",

        "const": "const ",
        "static": "static ",
        "tip pent": "int ",
        "tip char": "char ",
        "tip byte": "byte ",
        "tip pent 64": "int64_t ",
        "tip you went 64": "uint64_t ",
        "tip pent 32": "int32_t ",
        "tip you went 32": "uint32_t ",
        "tip pent 16": "int16_t ",
        "tip you went 16": "uint16_t ",
        "tip pent 8": "int8_t ",
        "tip you went 8": "uint8_t ",
        "tip size": "size_t",
        "tip float": "float ",
        "tip double": "double ",

        "args": ["()", Key("left")],
        "index": ["[]", Key("left")],
        "block": [" {}", Key("left enter enter up tab")],
        "empty array": "[]",
        "empty dict": "{}",

        "state (def | deaf | deft)": "def ",
        "state else if": "elif ",
        "state if": "if ",
        "state else if": [" else if ()", Key("left")],
        "state while": ["while ()", Key("left")],
        "state for": ["for ()", Key("left")],
        "state for": "for ",
        "state switch": ["switch ()", Key("left")],
        "state case": ["case \nbreak;", Key("up")],
        "state goto": "goto ",
        "state import": "import ",
        "state class": "class ",
        
        "state include": "#include ",
        "state include system": ["#include <>", Key("left")],
        "state include local": ['#include ""', Key("left")],
        "state type deaf": "typedef ",
        "state type deaf struct": ["typedef struct {\n\n};", Key("up"), "\t"],
        
        "comment see": "// ",
        "comment py": "# ",
        
        "word queue": "queue",
        "word eye": "eye",
        "word bson": "bson",
        "word iter": "iter",
        "word no": "NULL",
        "word cmd": "cmd",
        "word dup": "dup",
        "word streak": ["streq()", Key("left")],
        "word printf": "printf",
        "word (dickt | dictionary)": "dict",
        "word shell": "shell",
        
        "word talon": "talon",
        
        "dunder in it": "__init__",
        "self taught": "self.",
        "dickt in it": ["{}", Key("left")],
        "list in it": ["[]", Key("left")],
        "string utf8": "'utf8'",
        "state past": "pass",

        "arrow": "->",
        "call": "()",
        "indirect": "&",
        "dereference": "*",
        "(op equals | assign | equeft)": " = ",
        "(op (minus | subtract) | deminus)": " - ",
        "(op (plus | add) | deplush)": " + ",
        "(op (times | multiply) | duster)": " * ",
        "(op divide | divy)": " / ",
        "op mod": " % ",
        "[op] (minus | subtract) equals": " -= ",
        "[op] (plus | add) equals": " += ",
        "[op] (times | multiply) equals": " *= ",
        "[op] divide equals": " /= ",
        "[op] mod equals": " %= ",

        "(op | is) greater [than]": " > ",
        "(op | is) less [than]": " < ",
        "(op | is) equal": " == ",
        "(op | is) not equal": " != ",
        "(op | is) greater [than] or equal": " >= ",
        "(op | is) less [than] or equal": " <= ",
        "(op (power | exponent) | to the power [of])": " ** ",
        "op and": " && ",
        "op or": " || ",
        "[op] (logical | bitwise) and": " & ",
        "[op] (logical | bitwise) or": " | ",
        "(op | logical | bitwise) (ex | exclusive) or": " ^ ",
        "[(op | logical | bitwise)] (left shift | shift left)": " << ",
        "[(op | logical | bitwise)] (right shift | shift right)": " >> ",
        "(op | logical | bitwise) and equals": " &= ",
        "(op | logical | bitwise) or equals": " |= ",
        "(op | logical | bitwise) (ex | exclusive) or equals": " ^= ",
        "[(op | logical | bitwise)] (left shift | shift left) equals": " <<= ",
        "[(op | logical | bitwise)] (right shift | shift right) equals": " >>= ",
        
        "shebang bash": "#!/bin/bash -u\n",
        
        #MISCELLANEOUS---
        "prefies": Key("cmd-,"), #preferences
        "put computer to sleep": lambda m: os.system("pmset sleepnow"),
    }
)