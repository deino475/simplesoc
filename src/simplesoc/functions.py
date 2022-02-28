from simplesoc.data import JOB_TITLE_DICTIONARY


def find_soc_code(
    job_title, 
    year = 'US.2018', 
    n_socs = 10
):
    '''
    This function takes in a job title and returns the top n socs based
    on a levenshtein word/phrase distance.

    :param: job_title: A string representing a job title,
    :param: year: The year for the SOC codes you want to find. Default = 2018
    :param: n_socs: The top number of SOC codes you want to return. Default = 10
    '''
    similarity_dict = {}
    careers = list(JOB_TITLE_DICTIONARY[str(year)].keys())
    for career in careers:
        similarity_dict[career] = _levenshtein_sequence_distance(job_title.lower(), career.lower())

    sorted_careers = [{'name' : k, 'match': v} for k, v in sorted(
        similarity_dict.items(), 
        key=lambda item: item[1],
        reverse = True
    )]
    top_career_matches = sorted_careers[0:n_socs]
    for x in range(len(top_career_matches)):
        top_career_matches[x]['socs'] = JOB_TITLE_DICTIONARY[str(year)][top_career_matches[x]['name']]

    return top_career_matches

def _levenshtein_word_distance(str1, str2):
    '''
    Calculates the edit distance between two words.
    '''
    if type(str1) != str or type(str2) != str:
        raise TypeError(
            f'Parameters are supposed to be of type str and str, not {type(str1)} and {type(str2)}'
        )

    matrix = [[0 for x in range(len(str2) + 1)] for y in range(len(str1) + 1)]

    for x in range(len(str1) + 1):
        matrix[x][0] = x

    for x in range(len(str2) + 1):
        matrix[0][x] = x

    for i in range(1, len(str1) + 1):
        for j in range(1, len(str2) + 1):
            insertion = matrix[i-1][j] + 1
            deletion = matrix[i][j-1] + 1
            substitution = matrix[i-1][j-1] + (1 if str1[i-1] != str2[j-1] else 0)

            matrix[i][j] = min(insertion, deletion, substitution)

    return 1 - ((len(str1) + len(str2) - matrix[len(str1)][len(str2)]) / (len(str1) + len(str2)))


def _levenshtein_sequence_distance(
    text1, 
    text2, 
    sub_weight = 2, 
    trans_weight = 2
):
    '''
    Calculates the distance between two phrases.
    '''
    if type(text1) != str or type(text2) != str:
        raise TypeError(
            f'Parameters are supposed to be of type str and str, not {type(text1)} and {type(text2)}'
        )

    words1, words2 = text1.split(" "), text2.split(" ")
    matrix = [[0 for x in range(len(words2) + 1)] for y in range(len(words1) + 1)]

    word_distance_dictionary = {}

    #Calculate the distance of each word between each word in both sentences.
    for word1 in words1:
        if word1 not in word_distance_dictionary:
            word_distance_dictionary[word1] = {}
        for word2 in words2:
            word_distance_dictionary[word1][word2] = _levenshtein_word_distance(word1, word2)

    #Calculate the edit distance between each sequence of words
    for x in range(len(words1) + 1):
        matrix[x][0] = x

    for x in range(len(words2) + 1):
        matrix[0][x] = x

    for i in range(1, len(words1) + 1):
        for j in range(1, len(words2) + 1):
            insertion = matrix[i - 1][j] + 1
            deletion = matrix[i][j - 1] + 1
            substitution = matrix[i-1][j-1] +  min(sub_weight * word_distance_dictionary[words1[i - 1]][words2[j - 1]],1)
            transposition = matrix[i-1][j-1] + min(trans_weight * word_distance_dictionary[words1[i - 1]][words2[j - 2]],1)
            matrix[i][j] = min(insertion, deletion, substitution, transposition)

    #Calculate the similarity between the two phrases
    return (len(words1) + len(words2) - matrix[len(words1)][len(words2)]) / (len(words1) + len(words2))
