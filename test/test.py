
import json
import os
import subprocess
import sys
import textwrap
import manage_test_words as manage_words

from jdicscrape import Result


def test_words_sanity():
    # TODO: This should be moved to the run_test.sh script.
    """Check sanity of words database (keep this test first)"""
    script_path = os.path.join(os.path.dirname(__file__),
            "support", "words", "manage_test_words.py")
    p = subprocess.Popen([script_path, "-s"])
    sts = os.waitpid(p.pid, 0)[1]
    assert sts == 0

def print_helper(object_a, object_b, object_a_desc, object_b_desc, member_string):
    value_a = object_a.__getattribute__(member_string)
    value_b = object_b.__getattribute__(member_string)

    if hasattr(object_a, 'dic'):
        dic_name_a = object_a.dic.short_name
    else:
        dic_name_a = object_a.result.dic.short_name

    if hasattr(object_b, 'dic'):
        dic_name_b = object_b.dic.short_name
    else:
        dic_name_b = object_b.result.dic.short_name

    # print if different
    if value_a != value_b:
        print(u'\n\t%s: "%s" attribute -- %s' %
                (object_a_desc, member_string, value_a))
        print(u'\t%s: "%s" attribute -- %s' %
                (object_b_desc, member_string, value_b))

def pretty_format(obj, tab_amount=0):
    indent = ""
    for i in range(tab_amount):
        indent += "\t"

    wrapper = textwrap.TextWrapper(initial_indent=indent, subsequent_indent=indent, width=35)
    return wrapper.fill(u'%s' % obj)

def print_differences_example_sentence(ex_sent_a, ex_sent_b, ex_sent_a_string, ex_sent_b_string):
    """
    Prints the differences to between two example sentences.
    """
    print_helper(ex_sent_a, ex_sent_b, ex_sent_a_string, ex_sent_b_string, "jap_sentence")
    print_helper(ex_sent_a, ex_sent_b, ex_sent_a_string, ex_sent_b_string, "eng_trans")

def print_differences_definition_part(part_a, part_b, part_a_string, part_b_string):
    """
    Prints the differences to between two definition parts.
    """
    print_helper(part_a, part_b, part_a_string, part_b_string, "part")

def print_differences_definition(def_a, def_b, def_a_string, def_b_string):
    """
    Prints the differences to between two definitions.
    """
    parts_a = def_a.parts
    parts_b = def_b.parts

    if len(parts_a) != len(parts_b):
        print(u'\n\tnumber of parts for definition is different')
        print(u'\n\tparts from %s:' % def_a_string)
        for p in parts_a:
            print(p)
        print(u'\n\tparts from %s:' % def_a_string)
        for p in parts_b:
            print(p)
    else:
        for part_a, part_b in zip(parts_a, parts_b):
            part_a_string = def_a_string + ".part"
            part_b_string = def_b_string + ".part"
            print_differences_definition_part(part_a, part_b, part_a_string, part_b_string)

    exs_a = def_a.example_sentences
    exs_b = def_b.example_sentences

    if len(exs_a) != len(exs_b):
        print(u'\n\tnumber of example sentences for definition is different')
        print(u'\n\tdefinition: %s' % def_a.definition)
        print(u'\n\texample sentences from %s:' % def_a_string)
        for e in exs_a:
            print(e)
        print(u'\n\texample sentences from %s:' % def_a_string)
        for e in exs_b:
            print(e)
    else:
        for ex_a, ex_b in zip(exs_a, exs_b):
            ex_a_string = def_a_string + ".example_sentence"
            ex_b_string = def_b_string + ".example_sentence"
            print_differences_example_sentence(ex_a, ex_b, ex_a_string, ex_b_string)

def print_differences_result(result_a, result_b, result_a_string, result_b_string):
    """
    Prints the differences to between two results.
    """
    print_helper(result_a, result_b, result_a_string, result_b_string, "original_kanji")
    print_helper(result_a, result_b, result_a_string, result_b_string, "original_kana")
    print_helper(result_a, result_b, result_a_string, result_b_string, "url")
    print_helper(result_a, result_b, result_a_string, result_b_string, "kanji")
    print_helper(result_a, result_b, result_a_string, result_b_string, "kana")
    print_helper(result_a, result_b, result_a_string, result_b_string, "accent")

    defs_a = result_a.defs
    defs_b = result_b.defs

    if len(defs_a) != len(defs_b):
        print(u'\n\tnumber of definitions is different')
        print(u'\tdefs from %s:' % result_a_string)
        for d in defs_a:
            print(pretty_format(d, tab_amount=2))
        print(u'\tdefs from %s:' % result_b_string)
        for d in defs_b:
            print(pretty_format(d, tab_amount=2))
    else:
        for def_a, def_b in zip(defs_a, defs_b):
            def_a_string = result_a_string + ".definition"
            def_b_string = result_b_string + ".definition"
            print_differences_definition(def_a, def_b, def_a_string, def_b_string)

def checkword(dictionary, kanji, kana):
    html = manage_words.get_html_for_word(dictionary, kana, kanji)
    json_object = manage_words.get_json_for_word(dictionary, kana, kanji)

    html_parse_result = dictionary.lookup(kanji, kana, html)
    json_result = Result.from_jsonable(dictionary, json_object)

    if (json_result != html_parse_result):
        # TODO: find out what doesn't match
        print_differences_result(json_result, html_parse_result, "JSON result", "HTML result")
        assert(json_result == html_parse_result)

def test_words():
    words = manage_words.get_words_from_wordsdb()
    for dic in manage_words.get_dics():
        for kana, kanji in words:
            checkword.description = u'check %s (%s) in %s' % (kana, kanji, dic.short_name)
            yield checkword, dic, kanji, kana

