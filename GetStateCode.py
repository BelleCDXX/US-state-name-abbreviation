# US state reference https://en.wikipedia.org/wiki/List_of_U.S._state_abbreviations

from mapping import us_state_abbrev_map, special_case

states_abbrev = set(us_state_abbrev_map.values())
states_full = set(us_state_abbrev_map.keys())

# import existing mapping
statesMapping = dict()
with open('statesMapping', 'r') as f:
    for line in f:
        input_name, output_name, count = line.split('\t')
        statesMapping[input_name] = [output_name, int(count)]



# find best match
import re

def order_match(states_full, input_name):
    best_match_score = float('inf')
    best_match = None
    initials_input_name = [word[0] for word in input_name.split()]

    for state in states_full:
        # check if the initial of input can full map to the initial of state, order matters
        
        initials_state = [word[0] for word in state.split()]
        i1, i2 = 0, 0
        while i1 < len(initials_state) and i2 < len(initials_input_name):
            if initials_state[i1] == initials_input_name[i2]:
                i2 += 1
            i1 += 1

        if i2 != len(initials_input_name):
            continue

        # check if input can full map to state, order matters
        # compute the weight of each full map, weight will be reset for each word, weight = cur - left
        # weight for second word is larger than first word, thus use left = cur - 1
        # choose the match with least weight

        left, cur, i = -1, 0, 0
        cur_match_score = 0
        while cur < len(state) and i < len(input_name):
            if state[cur] == ' ':
                left = cur - 1
            if state[cur] == input_name[i]:
                #print left, cur, cur_match_score, state
                cur_match_score += cur - left
                i += 1
            cur += 1
        if i == len(input_name) and cur_match_score < best_match_score:
            #print cur_match_score, state
            best_match = state
            best_match_score = cur_match_score
    return best_match



def edit_distance_match():
    pass


def get_state_code(statesMapping):
    with open('input_data', 'r') as f1:
        for input_name_origin in f1:
            #input_name_origin = raw_input("input the state name: ")
            input_name_origin = input_name_origin.strip()
            input_name = ' '.join([item.lower() for item in re.split(r'[^a-zA-z]+', input_name_origin) if item])

            if input_name_origin in statesMapping:
                statesMapping[input_name_origin][1] += 1
            elif input_name.upper() in states_abbrev:
                statesMapping[input_name_origin] = [input_name.upper(), 1]
            elif input_name in us_state_abbrev_map:
                statesMapping[input_name_origin] = [us_state_abbrev_map[input_name], 1]
            elif input_name in special_case:
                statesMapping[input_name_origin] = [special_case[input_name], 1]
            else:
                best_match = order_match(states_full, input_name)
                if best_match:
                    statesMapping[input_name_origin] = [us_state_abbrev_map[best_match], 1]
                else:
                    with open('unidentify', 'a') as f2:
                        f2.write(input_name_origin + '\n')
                    continue

            print input_name_origin, statesMapping[input_name_origin][0]

    with open('statesMapping', 'w') as f3:
        for input_name in sorted(statesMapping):
            f3.write('{}\t{}\t{}\n'.format(input_name, statesMapping[input_name][0], statesMapping[input_name][1]))


# *********** main func *************

get_state_code(statesMapping)



