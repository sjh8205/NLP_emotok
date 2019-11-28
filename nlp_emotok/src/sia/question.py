from . import neo4j_query
from random import randrange
#from neo4j_query import get_random_entity_relation
#from neo4j_query import get_node_from_id
#from neo4j_query import get_answer
#from neo4j_query import get_next_query

def random():
    _json = dict()

    question_type, node, relation, leaf_node, hint = neo4j_query.get_random_entity_relation()

    _json['question_type'] = question_type['name']
    _json['question_type_id'] = question_type.id
    _json['node_id'] = node.id
    _json['relation'] = relation
    if leaf_node == None:
        _json['leaf_node_id'] = None
    else:
        _json['leaf_node_id'] = leaf_node.id
    _json['hint'] = hint

    #Delete node?
    _json['history'] = {'question_type': [], 'node': [], 'popword': [], 'drama': [], 'movie': [], 'Season_Type': [], 'flower': [], 'GreatMan': [], 'oldsong': [], 'idol_era': [], 'illness': [], 'tour': [], 'FOOD': []}
    _json['yon'] = 0

    if question_type['entity'] in ['Season_Type']:
        _json['Season_Type'] = neo4j_query.get_today_season_type_id()
    
    if question_type['entity'] in ["popword", "drama", "oldsong", "idol_era", "Season"]:
        _json['add_q'] = question_type['name'] + "에 대해 알려드릴까요?"
    else:
        _json['add_q'] = node['name'] + "에 대해 알려드릴까요?"

    _json['actionName'] = 'sia'
    _json['serviceName'] = 'emotok'
    _json['init'] = 'random'
    
    return _json

def succesive(req):
    _json = dict()

    question_type_id = req['question_type_id']
    node_id = req['node_id']
    relation = req['relation']
    leaf_node_id = req['leaf_node_id']

    question_type = neo4j_query.get_node_from_id(question_type_id)
    node = neo4j_query.get_node_from_id(node_id)
    if leaf_node_id == None:
        leaf_node = None
    else:
        leaf_node = neo4j_query.get_node_from_id(leaf_node_id)

    hint = req['hint']
    history = req['history']
    yon = req['yon']

    init = req['init']
    
    #History update
    #First, question_type update
    entity = question_type['entity']
    if entity not in history['question_type']:
        history['question_type'].append(entity)

    #########
    # category update implement
    ####
    if node.id not in history[entity]:
        history[entity].append(node.id)

    """
    label = list(node.labels)[0]
    if label not in history['node']:
        history['node'].append(label)
    """
    
    # add node id!!!!
    if leaf_node == None:
        if str(node_id) in history:
            if hint not in history[str(node_id)]:
                history[str(node_id)].append(hint)
        else:
            history[str(node_id)] = [hint]
    else:
        if str(node_id) in history:
            if leaf_node_id not in history[str(node_id)]:
                history[str(node_id)].append(leaf_node_id)
        else:
            history[str(node_id)] = [leaf_node_id]

    if entity in ['illness', 'tour']:
        if str(leaf_node_id) in history:
            if hint not in history[str(leaf_node_id)]:
                history[str(leaf_node_id)].append(hint)
        else:
            history[str(leaf_node_id)] = [hint]

    if entity in ['Season_Type']:
        season_type_id = req['Season_Type']
        if season_type_id not in history['Season_Type']:
            history['Season_Type'].append(season_type_id)
    
    #Check if req variable is stored in _json.
    #_json = req

    #Get answer
    if yon == 0:
        _json['answer'] = neo4j_query.get_answer(node, relation, leaf_node, hint)

    try:
        next_question_type, next_node, next_relation, next_leaf_node, next_hint, is_end, change = neo4j_query.get_next_query(req, history, question_type, node, relation, leaf_node, yon, hint)
    except ValueError as ve:
        raise ValueError('yon over the limit in ', question_type['entitiy'])
    
    _json['question_type'] = next_question_type['name']
    _json['question_type_id'] = next_question_type.id
    _json['node_id'] = next_node.id
    _json['relation'] = next_relation
    if next_leaf_node == None:
        _json['leaf_node_id'] = None
    else:
        _json['leaf_node_id'] = next_leaf_node.id
    _json['hint'] = next_hint
    _json['history'] = history
    _json['yon'] = yon

    if next_question_type['entity'] == 'Season_Type':
        _json['Season_Type'] = neo4j_query.get_today_season_type_id()

    #NLG
    if is_end:
        pass
    #Node
    elif change == 0:
        if init != "random":
            more = "더 "
        else:
            more = ""
            
        if next_question_type['entity'] in ['tour']:
            if next_relation == 'has_tour_info':
                _json['add_q'] = next_node['name']  + "에 대해서 {}알려드릴까요?".format(more)
            else:
                _json['add_q'] = next_node['name'] + " 관련해서 " + next_leaf_node['name'] + " 정보 {}알려드릴까요?".format(more)
        elif next_question_type['entity'] in ['oldsong']:
            _json['add_q'] = next_node['type'] + "년대 " + next_node['name'] + "에 대해서 {}알려드릴까요?".format(more)
        elif next_question_type['entity'] in ['idol_era']:
            _json['add_q'] = next_node['type'] + "에 대해서 {}알려드릴까요?".format(more)
        elif next_question_type['entity'] in ["popword", "drama", "movie"]:
            _json['add_q'] = next_node['name'] + "에 대해서 {}알려드릴까요?".format(more)
        elif next_question_type['entity'] in ["illness"]:
            if next_relation == 'has_good_food':
                _json['add_q'] = next_node['name'] + "에 좋은 음식에 대해 {}알려드릴까요?".format(more)
            else:
                _json['add_q'] = next_node['name'] + " 관련 예방법에 대해서 {}알려드릴까요?".format(more)
        else:
            _json['add_q'] = next_node['name'] + "의 " + leaf_node['name'] + " 외에 " + next_leaf_node['name'] + " 대해서 {}알려드릴까요?".format(more)
    #Sibling node
    elif change == 1:
        if next_question_type['entity'] in ['oldsong']:
            _json['add_q'] = "이번에는 " + next_node['type'] + "년대 " + next_node['name'] + "에 대해서 알려드릴까요?"
        elif next_question_type['entity'] in ['idol_era']:
            _json['add_q'] = "이번에는 " + next_node['type'] + "에 대해서 알려드릴까요?"
        elif next_question_type['entity'] in ["illness"]:
            _json['add_q'] = "이번에는 " + next_node['name'] + "에 좋은 음식에 대해 알려드릴까요?"
        elif next_question_type['entity'] in ['Season_Type']:
            _json['add_q'] = "이번에는 " + next_node['name'] + "에 대해 알려드릴까요?"            
        else:
            _json['add_q'] = "이번에는 " + next_node['name'] + "에 대해서 알려드릴까요?"
    #Move next category
    elif change == 2:
        if next_question_type['entity'] in ['oldsong']:
            _json['add_q'] = "그렇다면 " + next_node['type'] + "년대 " + next_node['name'] + "에 대해서 알려드릴까요?"
        elif next_question_type['entity'] in ['idol_era']:
            _json['add_q'] = "그렇다면 " + next_node['type'] + "에 대해서 알려드릴까요?"
        else:
            _json['add_q'] = "그렇다면 " + next_node['name'] + "에 대해서 알려드릴까요?"
    else:
        print("Error related with change: ", change)

    _json['actionName'] = 'sia'
    _json['serviceName'] = 'emotok'
    _json['init'] = 'successive'
    
    return _json

def answer(entity, relation):
    if relation == "has_idol":
        relation = "has_idol_era"
    
    nodes, leaf_nodes = neo4j_query.get_node_from_entity_relation(entity, relation)
    
    if len(nodes) != len(leaf_nodes):
        raise Exception("lens are different. nodes: {}, leaf_nodes: {}".format(len(nodes), len(leaf_nodes)))
    
    if len(leaf_nodes) > 0:
        index = randrange(0, len(leaf_nodes))
    else:
        index = 0

    node = nodes[index]
    leaf_node = leaf_nodes[index]
    #print("node: ", node)
    #print("leaf_node: ", leaf_node)
    data = dict()

    question_type = neo4j_query.get_question_type_from_node_relation(node, relation)
    data['question_type'] = question_type['name']
    data['question_type_id'] = question_type.id

    data['history'] = {'question_type': [], 'node': [], 'popword': [], 'drama': [], 'movie': [], 'Season_Type': [], 'flower': [], 'GreatMan': [], 'oldsong': [], 'idol_era': [], 'illness': [], 'tour': [], 'FOOD': []}
    data['yon'] = 0

    ####
    # Food랑 season food 구별 할 때 이용??
    ###
    if question_type['entity'] in ['Season_Type']:
        #data['Season_Type'] = neo4j_query.get_today_season_type_id()
        data['Season_Type'] = neo4j_query.get_season_type_from_entity(entity).id


    """
    if question_type['entity'] in ["popword", "drama", "oldsong", "idol_era", "Season"]:
        _json['add_q'] = question_type['name'] + "에 대해 알려드릴까요?"
    else:
        _json['add_q'] = node['name'] + "에 대해 알려드릴까요?"
    """
    data['actionName'] = 'sia'
    data['serviceName'] = 'emotok'

    hint = None
    if relation in ["has_good_food"]:
        if checkTrait(leaf_node['name'][-1]):
            suffix = "이 좋대요"
        else:
            suffix = "가 좋대요"
        answer = entity + "에는 " + leaf_node['name'] + suffix
    elif relation in ["has_season_food"]:
        if checkTrait(leaf_node['name'][-1]):
            suffix = "이 있어요"
        else:
            suffix = "가 있어요"
        answer = entity + "시즌 제철음식으로는 " + leaf_node['name'] + suffix
    elif relation in ["has_idol_era", "has_music_info", "has_song_info", "has_prevention", "has_popword_info", "has_tour_info", "has_tour_reco"]:
        hint = randrange(0, get_len_hint(leaf_node)) + 1
        answer = leaf_node['hint' + str(hint)]
    elif relation in ["has_lifetime_info"]:
        if leaf_node['birth'] == "없음":
            if leaf_node['death'] == "없음":
                if checkTrait(node['name'][-1]):
                    answer = node['name'] + "은 정확한 출생정보와 사망정보가 없어요"
                else:
                    answer = node['name'] + "는 정확한 출생정보와 사망정보가 없어요"
            else:
                if checkTrait(node['name'][-1]):
                    answer = node['name'] + "은 정확한 출생정보는 없지만 " + leaf_node['death'] + "년도까지 살았대요"
                else:
                    answer = node['name'] + "는 정확한 출생정보는 없지만 " + leaf_node['death'] + "년도까지 살았대요"
        else:
            if leaf_node['death'] == "없음":
                if checkTrait(node['name'][-1]):
                    answer = node['name'] + "은 " + leaf_node['birth'] + "년도에 태어났지만 정확한 사망정보가 없어요"
                else:
                    answer = node['name'] + "는 " + leaf_node['birth'] + "년도에 태어났지만 정확한 사망정보가 없어요"
            else:
                if checkTrait(node['name'][-1]):
                    answer = node['name'] + "은 " + leaf_node['birth'] + "년도에 태어나서 " + leaf_node['death'] + "년도까지 살았대요"
                else:
                    answer = node['name'] + "는 " + leaf_node['birth'] + "년도에 태어나서 " + leaf_node['death'] + "년도까지 살았대요"

    else:
        answer = leaf_node['hint']
        
    data['answer'] = answer
    if hint == None:
        data['hint'] = None
    else:
        data['hint'] = "hint" + str(hint)
    ####
    # change node, leaf_node, relation
    ###
    node, relation, leaf_node = changeNode(entity, node, relation, leaf_node)
    
    data['node_id'] = node.id
    data['relation'] = relation
    if leaf_node == None:
        data['leaf_node_id'] = None
    else:
        data['leaf_node_id'] = leaf_node.id
    data['init'] = 'answer'
    
    return data

def changeNode(entity, node, relation, leaf_node):
    new_node = None
    new_relation = None
    new_leaf_node = None
    
    if relation in ["has_purchase_info", "has_storage_info", "has_refine_info", "has_goods_info", "has_cal_info", "has_flower_hint", "has_prevention", "has_good_food", "has_tour_info", "has_tour_reco", "has_career_info", "has_intro_info", "has_lifetime_info"]:
        new_node = node
        new_relation = relation
        new_leaf_node = leaf_node
    elif relation in ["has_music_info", "has_song_info", "has_movie_info", "has_drama_info", "has_popword_info", "has_idol_era"]:
        new_node = leaf_node
        new_relation = None
        new_leaf_node = None
    elif relation == "has_season_food":
        new_node = leaf_node
        new_relation = 'has_intro_info'
        new_leaf_node = neo4j_query.get_leaf_node_from_node_relation(new_node, new_relation)
    else:
        raise Exception("Can't change node: {}, {}, {}, {}".format(entity, node, relation, leaf_node))

    return new_node, new_relation, new_leaf_node

def get_len_hint(node):
    if node['len'] == None:
        maxlen = 0
        for i in range(1, 1000):
            if 'hint' + str(i) not in node:
                maxlen = i-1
                break
    else:
        maxlen = node['len']
        
    return maxlen

def checkTrait(c):
    return (int((ord(c) - 0xAC00) % 28) != 0)
