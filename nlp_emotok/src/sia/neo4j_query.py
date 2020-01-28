import time
import numpy as np
from neo4j import GraphDatabase
import logging

#driver = GraphDatabase.driver("bolt://35.229.155.246:7000", auth=("neo4j", "1thefull322"))
class Singleton:
    __instance = None
    driver = None

    @staticmethod
    def instance():
        if Singleton.__instance == None:
            Singleton()
        return Singleton.__instance

    def __init__(self):
        if Singleton.__instance != None:
            raise Exception("This class is a singleton")
        else:
            Singleton.__instance = self

def getDriver():
    if Singleton.instance().driver == None:
        Singleton.instance().driver = GraphDatabase.driver("bolt://35.229.155.246:7000", auth=("neo4j", "1thefull322"))
    return Singleton.instance().driver


def get_node_from_entity_relation(entity, relation):
    driver = getDriver()
    with driver.session() as session:
        nodes, leaf_nodes = session.read_transaction(match_node_from_entity_relation, entity, relation)
    return nodes, leaf_nodes

def match_node_from_entity_relation(tx, entity, relation):
    nodes = []
    leaf_nodes = []
    # NEW : add code for "has_Datetime" case in question.answer --
    if relation != None:
        # MOVE --
        for record in tx.run("MATCH (e)-[:{}]->(ee) WHERE e.name = \"{}\" RETURN e, ee".format(relation, entity)):
            nodes.append(record['e'])
            leaf_nodes.append(record['ee'])
        # -- move end
    else:
        for record in tx.run("MATCH (e)-[]->(ee) WHERE ID(e)={} RETURN e, ee".format(entity.id)):
            nodes.append(record['e'])
            leaf_nodes.append(record['ee'])
    # -- end
    return nodes, leaf_nodes

def get_node_from_entity(entity):
    driver = getDriver()
    with driver.session() as session:
        node = session.read_transaction(match_node_from_entity, entity)
    return node

def match_node_from_entity(tx, entity):
    for record in tx.run("MATCH (e) WHERE e.name = \"{}\" RETURN e".format(entity)):
        return record['e']
"""
def get_all_relations_from_node(node):
    with driver.session() as session:
        relations = session.read_transaction(match_all_relations_from_node, node)
    return relations

def match_all_relations_from_node(tx, node):
    relations = []
    for record in tx.run("MATCH (e)-[r]-(ee) WHERE id(e) = {} RETURN e, r, ee".format(node.id)):
        relations.append(record['r'])

"""
#Common API
def get_node_hint_len(node):
    if node['len'] == None:
        maxlen = 0
        for i in range(1, 1000):
            if 'hint' + str(i) not in node:
                maxlen = i-1
                break
    else:
        maxlen = node['len']
        
    return maxlen

def get_today_season_type_id():
    now = time.gmtime(time.time())
    if 3 <= now.tm_mon and now.tm_mon < 6:
        ID =  1182
    elif 6 <= now.tm_mon and now.tm_mon < 9:
        ID =  1202
    elif 9 <= now.tm_mon and now.tm_mon < 12:
        ID =  1203
    else:
        ID =  1204
        
    return ID

def get_season_type_from_entity(entity):
    driver = getDriver()    
    with driver.session() as session:
        season_type = session.read_transaction(match_season_type_from_entity, entity)
    return season_type

def match_season_type_from_entity(tx, entity):
    for record in tx.run("MATCH (n) WHERE n.name = \"{}\" RETURN n".format(entity)):
        node = record['n']
    return node

def get_node_from_id(ID):
    driver = getDriver()    
    with driver.session() as session:
        node = session.read_transaction(match_node_from_id, ID)
    return node

def match_node_from_id(tx, ID):
    for record in tx.run("MATCH (n) WHERE id(n) = {} RETURN n".format(ID)):
        node = record['n']
    return node

def get_leaf_node_from_node_relation(node, relation):
    driver = getDriver()    
    with driver.session() as session:
        leaf_node = session.read_transaction(match_leaf_node_from_relation, node.id, relation)
    return leaf_node

def match_leaf_node_from_relation(tx, ID, relation):
    for record in tx.run("MATCH (n)-[:{}]-(l) WHERE id(n) = {} RETURN n, l".format(relation, ID)):
        leaf_node = record['l']
    return leaf_node

def get_relation_from_ids(node_id, leaf_node_id):
    driver = getDriver()    
    with driver.session() as session:
        relation = session.read_transaction(match_relation_from_ids, node_id, leaf_node_id)
    return relation

def match_relation_from_ids(tx, node_id, leaf_node_id):
    for record in tx.run("MATCH (n)-[r]-(l) WHERE id(n) = {} and id(l) = {} RETURN n, r, l".format(node_id, leaf_node_id)):
        relation = record['r'].type
    return relation

def match_seasons_ids(tx):
    seasons_ids = []
    for record in tx.run("MATCH (s:Season_Type) RETURN s"):
        seasons_ids.append(record['s'].id)
    return seasons_ids

def match_foods_from_season_id(tx, season_id):
    foods = []
    for record in tx.run("MATCH (s)-[:has_season_food]-(f) WHERE id(s) = {} RETURN f".format(season_id)):
        foods.append(record['f'])
    return foods

def get_spare_entities(history):
    driver = getDriver()    
    #Get all category
    with driver.session() as session:
        question_nodes = session.read_transaction(match_question_nodes)

    entities = []
    for question_node in question_nodes:
        entities.append(question_node['entity'])

    #Delete used category
    for entity in history['question_type']:
        if entity in entities:
            entities.remove(entity)

    return entities

def move_next_category(history):
    next_question_type = None
    next_node = None
    next_relation = None
    next_leaf_node = None
    next_hint = None

    change = 2
    is_end = False

    entities = get_spare_entities(history)

    #End point: No spare category.    
    if len(entities) == 0:
        is_end = True
    #End point: Change into new category.        
    else:
        next_entity = np.random.choice(entities ,1).item()
        next_question_type, next_node, next_relation, next_leaf_node, next_hint = get_random_entity_relation_from_entity(next_entity)
    
    return (next_question_type, next_node, next_relation, next_leaf_node, next_hint, is_end, change)

def get_leaf_nodes(node, relation):
    driver = getDriver()    
    with driver.session() as session:
        leaf_nodes = session.read_transaction(match_leaf_nodes, node, relation)
    return leaf_nodes

def match_leaf_nodes(tx, node, relation):
    leaf_nodes = []
    if relation != None:
        match = "MATCH (n)-[:{}]-(l) WHERE id(n) = {} RETURN l".format(relation, node.id)
    else:
        match = "MATCH (n)-[]-(l) WHERE id(n) = {} RETURN l".format(node.id)
    for record in tx.run(match):
        leaf_nodes.append(record['l'])
    return leaf_nodes

#API 1
def get_random_entity_relation():
    driver = getDriver()    
    with driver.session() as session:
        #Get all question types & Select one type.
        question_types = session.read_transaction(match_question_nodes)
        # NEW : delete random question of 'Hobby' --
        for a in question_types:
            if a['entity']== 'Hobby':
                question_types.remove(a)
        # -- end
        question_type = question_types[np.random.choice(len(question_types), 1)[0]]

        try:
            #Get initial node in the type.
            node, relation = session.read_transaction(match_init_node_relation, question_type)

            if question_type['entity'] == 'tour':
                leaf_node = session.read_transaction(match_init_leaf_node, node, relation)
                maxlen = get_node_hint_len(leaf_node)
                #hint = 'hint' + str(np.random.choice(leaf_node['len'], 1)[0] + 1)
                hint = 'hint' + str(np.random.choice(maxlen, 1)[0] + 1)
            elif relation == None:
                #leaf_node = node
                leaf_node = None
                maxlen = get_node_hint_len(node)
                #hint = 'hint' + str(np.random.choice(node['len'], 1)[0] + 1)
                hint = 'hint' + str(np.random.choice(maxlen, 1)[0] + 1)
            else:
                leaf_node = session.read_transaction(match_init_leaf_node, node, relation)
                hint = None
        except Exception as ex:
            logging.basicConfig(filename="random.txt", filemode="a", format="%(name)s - %(levelname)s - %(message)s")
            logging.error(node, " : ", relation, "\n", ex)
            
        
    return question_type, node, relation, leaf_node, hint

def match_question_nodes(tx):
    nodes = []
    for record in tx.run("MATCH (q:Question_Type) RETURN q"):
        nodes.append(record['q'])
    return nodes

def match_init_node_relation(tx, question_type):
    #Find node
    if question_type['entity'] in ["popword", "movie", "drama", "idol_era", "oldsong"]:
        # for record in tx.run("MATCH (n:{}) RETURN n".format(question_type['entity'])):
        #     node = record['n']
        # NEW : there are several nodes for "idol_era"&"oldsong", but only last node can be selected. so add rand() to pick it randomly --
        for record in tx.run("MATCH (n:{}) with n, rand() AS r ORDER BY r RETURN n LIMIT 1".format(question_type['entity'])):
            node = record['n']
        # -- end
    elif question_type['entity'] in ["Season_Type"]:
        ID = get_today_season_type_id()

        for record in tx.run("MATCH (n)-[]-(f:FOOD) WHERE id(n) = {} with f, rand() AS r ORDER BY r RETURN f LIMIT 1".format(ID)):
            node = record['f']
    else:
        for record in tx.run("MATCH (n:{}) with n, rand() AS r ORDER BY r RETURN n LIMIT 1".format(question_type['entity'])):
            node = record['n']

    #Find relation
    label = list(node.labels)[0]
    # NEW : add 'Event' in case
    if label in ["FOOD", "GreatMan", "Event"]:
        relation = "has_intro_info"
    elif label in ["tour"]:
        relation = "has_tour_info"
    elif label in ["flower"]:
        relation = "has_flower_hint"
    elif label in ["illness"]:
        relation = "has_good_food"
    # NEW : add 'Body' case - set default relation
    elif label in ["Body"]:
        relation = "has_tip_info"
    # -- end
    elif label in ["popword", "movie", "drama", "idol_era", "oldsong"]:
        relation = None
    # NEW : modify spelling error [ lable -> label ]
    elif label in ["Season_Type"]:
        relation = 'has_season_food'
    else:
        print("match_init_node_relation error: ", label, ', ', node)
        #exit()
    return node, relation

def match_init_leaf_node(tx, node, relation):
    for record in tx.run("MATCH (n)-[:{}]-(l) WITH l, rand() AS r ORDER BY r WHERE id(n) = {} RETURN l LIMIT 1".format(relation, node.id)):
        leaf_node = record['l']

    return leaf_node

#API 2
def get_answer(node, relation, leaf_node, hint):
    driver = getDriver()    
    with driver.session() as session:
        answer = session.read_transaction(match_answer, node, relation, leaf_node, hint)
    return answer

def match_answer(tx, node, relation, leaf_node, hint):
    if list(node.labels)[0] == "illness":
        if relation == 'has_good_food':
            if checkTrait(leaf_node['name'][-1]):
                answer = node['name'] + "에는 " + leaf_node['name'] + '이 좋대요.'
            else:
                answer = node['name'] + "에는 " + leaf_node['name'] + '가 좋대요.'
        else:
            answer = leaf_node[hint]
    elif leaf_node == None:
        for record in tx.run("MATCH (n) WHERE id(n) = {} RETURN n".format(node.id)):
            answer = record['n'][hint]
    # NEW : add case --
    elif relation == 'has_Datetime':
        name = node['name']
        tNode, time_nodes = get_node_from_entity_relation(leaf_node, None)
        if len(time_nodes) == 3:
            for record in time_nodes:
                if '년' in record['name']:
                    year = " " + record['name']
                elif '월' in record['name']:
                    month = " " + record['name']
                elif '일' in record['name']:
                    day = " " + record['name']
        else:
            year = " " + time_nodes[0]['name']
            month = ""
            day = ""
        if checkTrait(name[-1]):
            answer = name + "은" + year + "{}{}에 일어났어요.".format(month, day)
        else:
            answer = name + "는" + year + "{}{}에 일어났어요.".format(month, day)
    # -- end
    else:
        for record in tx.run("MATCH (n)-[]-(l) WHERE id(n) = {} AND id(l) = {} RETURN n, l".format(node.id, leaf_node.id)):
            if list(node.labels)[0] == 'tour':
                answer = record['l'][hint]
            elif relation == 'has_lifetime_info':
                birth = record['l']['birth']
                death = record['l']['death']
                name = node['name']
                if checkTrait(name[-1]):
                    answer = name + "은 " + birth + "년에서 " + death + "년까지 살았었어요."
                else:
                    answer = name + "는 " + birth + "년에서 " + death + "년까지 살았었어요."
            # NEW : add case --
            elif relation == 'has_good_food':
                if checkTrait(leaf_node['name'][-1]):
                    answer = node['name'] + " 건강에는 " + leaf_node['name'] + '이 좋대요.'
                else:
                    answer = node['name'] + " 건강에는 " + leaf_node['name'] + '가 좋대요.'
            # -- end
            else:
                answer = record['l']['hint']
    return answer

def get_next_query(req, history, question_type, node, relation, leaf_node, yon, hint):
    next_question_type = None
    next_node = None
    next_relation = None
    next_leaf_node = None
    next_hint = None
    is_end = False
    is_changed = False
    change = 0

    if question_type['entity'] in ["popword", "drama", "movie"]:
        if yon == 0:
            ret = get_spare_hints(req, history, question_type, node, relation, leaf_node, yon, hint)
        elif yon == 1:
            ret = move_next_category(history)            
        else:
            raise ValueError('yon over the limit in ', question_type['entitiy'])
    elif question_type['entity'] in ["flower"]:
        if yon == 0:
            ret = get_spare_sibling_nodes(req, history, question_type, node, relation, leaf_node, yon, hint)
        elif yon == 1:
            ret = move_next_category(history)
        else:
            raise ValueError('yon over the limit in ', question_type['entitiy'])            
    elif question_type['entity'] in ["idol_era", "oldsong"]:
        if yon == 0:
            ret = get_spare_hints(req, history, question_type, node, relation, leaf_node, yon, hint)
        elif yon == 1:
            ret = get_spare_sibling_nodes(req, history, question_type, node, relation, leaf_node, yon, hint)
        elif yon == 2:
            ret = move_next_category(history)
        else:
            raise ValueError('yon over the limit in ', question_type['entitiy'])
    elif question_type['entity'] in ["illness"]:
        if yon == 0:
            if relation == 'has_prevention':
                ret = get_spare_hints(req, history, question_type, node, relation, leaf_node, yon, hint)
            else:
                ret = get_spare_leaf_nodes(req, history, question_type, node, relation, leaf_node, yon, hint)
        elif yon == 1:
            if relation == 'has_prevention':
                ret = get_spare_sibling_nodes(req, history, question_type, node, relation, leaf_node, yon, hint)
            else:
                next_question_type = question_type
                next_node = node
                next_relation = 'has_prevention'
                next_leaf_node = get_leaf_node_from_node_relation(next_node, next_relation)
                maxlen = get_node_hint_len(next_leaf_node)
                """
                if next_leaf_node['len'] == None:
                    maxlen = 0
                    for i in range(1, 1000):
                        if 'hint' + str(i) not in next_leaf_node:
                            maxlen = i-1
                            break
                else:
                    maxlen = next_leaf_node['len']
                """
                #next_hint = 'hint' + str(np.random.choice(next_leaf_node['len'], 1).item() + 1)
                next_hint = 'hint' + str(np.random.choice(maxlen, 1).item() + 1)
                ret = (next_question_type, next_node, next_relation, next_leaf_node, next_hint, is_end, 0)
        elif yon == 2:
            ret = get_spare_sibling_nodes(req, history, question_type, node, relation, leaf_node, yon, hint)
        elif yon == 3:
            ret = move_next_category(history)                         
        else:
            raise ValueError('yon over the limit in ', question_type['entitiy'])            
    elif question_type['entity'] in ["tour"]:
        if yon == 0:
            ret = get_spare_hints(req, history, question_type, node, relation, leaf_node, yon, hint)
        elif yon == 1:
            if relation == 'has_tour_info':
                next_question_type = question_type
                next_node = node
                next_relation = 'has_tour_reco'
                next_leaf_node = get_leaf_node_from_node_relation(next_node, next_relation)
                maxlen = get_node_hint_len(next_leaf_node)
                #next_hint = 'hint' + str(np.random.choice(next_leaf_node['len'], 1)[0] + 1)
                next_hint = 'hint' + str(np.random.choice(maxlen, 1)[0] + 1)
                ret = (next_question_type, next_node, next_relation, next_leaf_node, next_hint, is_end, 0)
            else:
                ret = get_spare_sibling_nodes(req, history, question_type, node, relation, leaf_node, yon, hint)
        elif yon == 2:
            ret = get_spare_sibling_nodes(req, history, question_type, node, relation, leaf_node, yon, hint)
        elif yon == 3:
            ret = move_next_category(history)                        
        else:
            raise ValueError('yon over the limit in ', question_type['entitiy'])            
    elif question_type['entity'] in ["FOOD"]:
        if yon == 0:
            ret = get_spare_leaf_nodes(req, history, question_type, node, relation, leaf_node, yon, hint)
        elif yon == 1:
            ret = get_spare_sibling_nodes(req, history, question_type, node, relation, leaf_node, yon, hint)
        elif yon == 2:
            ret = move_next_category(history)                         
        else:
            raise ValueError('yon over the limit in ', question_type['entitiy'])            
    elif question_type['entity'] in ["Season_Type"]:
        if yon == 0:
            all_leaf_nodes = get_leaf_nodes(node, None)
            leaf_nodes = []
            for leaf_node in all_leaf_nodes:
                labels = list(leaf_node.labels)[0]
                if labels not in ["Season_Type", "illness", "Question_Type"]:
                    leaf_nodes.append(leaf_node)
            
            leaf_nodes_ids = [leaf_node.id for leaf_node in leaf_nodes]
            for ID in history[str(node.id)]:
                if ID in leaf_nodes_ids:
                    leaf_nodes_ids.remove(ID)

            if len(leaf_nodes_ids) != 0:
                next_question_type = question_type
                next_node = node
                next_leaf_node = get_node_from_id(np.random.choice(leaf_nodes_ids, 1).item())
                next_relation = get_relation_from_ids(next_node.id, next_leaf_node.id)
                next_hint = hint
                ret = (next_question_type, next_node, next_relation, next_leaf_node, next_hint, False, 0)
            else:
                ret = get_specific_season_food(req, history, question_type, node, relation, leaf_node, yon, hint)
        elif yon == 1:
            ret = get_specific_season_food(req, history, question_type, node, relation, leaf_node, yon, hint)
        elif yon == 2:
            ret = get_other_season_food(req, history, question_type, node, relation, leaf_node, yon, hint)
        elif yon == 3:
            ret = move_next_category(history)                         
        else:
            raise ValueError('yon over the limit in ', question_type['entitiy'])
    # NEW : add 'Event', 'Body' in case
    elif question_type['entity'] in ["GreatMan", "Event", "Body"]:
        if yon == 0:
            ret = get_spare_leaf_nodes(req, history, question_type, node, relation, leaf_node, yon, hint)
        elif yon == 1:
            ret = get_spare_sibling_nodes(req, history, question_type, node, relation, leaf_node, yon, hint)
        elif yon == 2:
            #next_question_type, next_node, next_relation, next_leaf_node, next_hint, is_end, is_changed = move_next_category(history)
            ret = move_next_category(history)
        else:
            raise ValueError('yon over the limit in ', question_type['entitiy'])
    # NEW : add case --
    elif question_type['entity'] in ["Hobby"]:
        if yon==0:
            ret = get_spare_sibling_nodes(req, history, question_type, node, relation, leaf_node, yon, hint)
        elif yon==1:
            ret = move_next_category(history)
        else:
            raise ValueError('yon over the limit in ', question_type['entitiy'])
    # -- end
    else:
        raise ValueError('question_type is not valid: ', question_type['entitiy'])            

    #return next_question_type, next_node, next_relation, next_leaf_node, next_hint, is_end, is_changed
    return ret

def get_spare_hints(req, history, question_type, node, relation, leaf_node, yon, hint):
    if leaf_node == None:
        hint_id = node.id
    else:
        hint_id = leaf_node.id
    driver = getDriver()        
    with driver.session() as session:
        hints = session.read_transaction(match_hint_from_leaf_node, hint_id)
        #hints = session.read_transaction(match_hint_from_leaf_node, leaf_node.id)

    keys = list(hints.keys())
    #for ID in history[str(leaf_node.id)]:
    for ID in history[str(hint_id)]:
        if ID in keys:
            keys.remove(ID)

    if len(keys) != 0:
        key = np.random.choice(keys, 1).item()
        next_question_type = question_type
        next_node = node
        next_relation = relation
        next_leaf_node = leaf_node
        #next_hint = hints[key]
        next_hint = key
        ret = (next_question_type, next_node, next_relation, next_leaf_node, next_hint, False, 0)
    else:
        if question_type['entity'] in ['tour']:
            if relation == 'has_tour_info':
                next_question_type = question_type
                next_node = node
                next_relation = 'has_tour_reco'
                next_leaf_node = get_leaf_node_from_node_relation(next_node, next_relation)
                maxlen = get_node_hint_len(next_leaf_node)
                #next_hint = 'hint' + str(np.random.choice(next_leaf_node['len'], 1)[0] + 1)
                next_hint = 'hint' + str(np.random.choice(maxlen, 1)[0] + 1)
                ret = (next_question_type, next_node, next_relation, next_leaf_node, next_hint, False, 1)
            else:
                ret = get_spare_sibling_nodes(req, history, question_type, node, relation, leaf_node, yon, hint)
                #next_question_type, next_node, next_relation, next_leaf_node, next_hint, is_end, is_changed = move_next_category(history)
        elif question_type['entity'] in ['illness']:
            if relation == 'has_good_food':
                pass

    return ret

def get_spare_leaf_nodes(req, history, question_type, node, relation, leaf_node, yon, hint):
    next_question_type = None
    next_node = None
    next_relation = None
    next_leaf_node = None
    next_hint = None
    is_end = None
    change = 0
    
    leaf_nodes = get_leaf_nodes(node, None)
    leaf_nodes_ids = [leaf_node.id for leaf_node in leaf_nodes]
    for ID in history[str(node.id)]:
        if ID in leaf_nodes_ids:
            leaf_nodes_ids.remove(ID)
    # NEW : because of get_leaf_nodes func, Question_type node also added to dictionary named 'leaf_node_ids'. so add this code to remove question type node in dic --
    for ID in leaf_nodes_ids:
        if ID == question_type.id:
            leaf_nodes_ids.remove(ID)
    # -- end

    if len(leaf_nodes_ids) != 0:
        next_question_type = question_type
        next_node = node
        next_leaf_node = get_node_from_id(np.random.choice(leaf_nodes_ids, 1).item())
        next_relation = get_relation_from_ids(next_node.id, next_leaf_node.id)
        next_hint = hint
        ret = (next_question_type, next_node, next_relation, next_leaf_node, next_hint, is_end, change)
    else:
        ret = get_spare_sibling_nodes(req, history, question_type, node, relation, leaf_node, yon, hint)

    return ret

def get_spare_sibling_nodes(req, history, question_type, node, relation, leaf_node, yon, hint):
    next_question_type = None
    next_node = None
    next_relation = None
    next_leaf_node = None
    next_hint = None
    is_end = False
    change = 1

    label = list(node.labels)[0]
    driver = getDriver()
    with driver.session() as session:
        sibling_nodes = session.read_transaction(match_nodes_from_labels, label)

    spare_nodes = []
    for sibling_node in sibling_nodes:
        if sibling_node.id not in history[question_type['entity']]:
            spare_nodes.append(sibling_node)

    if len(spare_nodes) != 0:
        next_question_type = question_type
        next_node = spare_nodes[np.random.choice(len(spare_nodes), 1).item()]
        # NEW : add 'Event', 'Hobby' in case
        if question_type['entity'] in ['GreatMan', 'FOOD', 'Event', 'Hobby']:
            next_relation = 'has_intro_info'
        # NEW : add 'Body' case --
        elif question_type['entity'] in ["Body"]:
            next_relation = 'has_good_food'
        # -- end
        elif question_type['entity'] in ["flower"]:
            next_relation = 'has_flower_hint'
        elif question_type['entity'] in ["tour"]:
            next_relation = 'has_tour_info'
        elif question_type['entity'] in ["illness"]:
            next_relation = 'has_good_food'
        else:
            next_relation = None
            
        if next_relation != None:
            # ############################################
            next_leaf_node = get_leaf_node_from_node_relation(next_node, next_relation)
        else:
            next_leaf_node = None
            
        if question_type['entity'] in ["tour"]:
            maxlen = get_node_hint_len(next_leaf_node)
            #next_hint = 'hint' + str(np.random.choice(next_leaf_node['len'], 1)[0] + 1)
            next_hint = 'hint' + str(np.random.choice(maxlen, 1)[0] + 1)
        elif question_type['entity'] in ["oldsong", "idol_era"]:
            maxlen = get_node_hint_len(next_node)
            #next_hint = 'hint' + str(np.random.choice(next_node['len'], 1)[0] + 1)
            next_hint = 'hint' + str(np.random.choice(maxlen, 1)[0] + 1)
        else:
            next_hint = None
    else:
        next_question_type, next_node, next_relation, next_leaf_node, next_hint, is_end, change = move_next_category(history)

    return (next_question_type, next_node, next_relation, next_leaf_node, next_hint, is_end, change)

def get_specific_season_food(req, history, question_type, node, relation, leaf_node, yon, hint):
    driver = getDriver()    
    season_type_id = req['Season_Type']
    with driver.session() as session:
        season_foods = session.read_transaction(match_foods_from_season_id, season_type_id)

    season_foods_ids = [season_food.id for season_food in season_foods]
    for ID in history['FOOD'] + history['Season_Type']:
        if ID in season_foods_ids:
            season_foods_ids.remove(ID)

    if len(season_foods_ids) != 0:
        next_question_type = question_type
        next_node = get_node_from_id(np.random.choice(season_foods_ids, 1).item())
        next_relation = 'has_intro_info'
        next_leaf_node = get_leaf_node_from_node_relation(next_node, next_relation)
        next_hint = hint
        ret = (next_question_type, next_node, next_relation, next_leaf_node, next_hint, False, 1)
    else:
        ret = get_other_season_food(req, history, question_type, node, relation, leaf_node, yon, hint)

    return ret

def get_other_season_food(req, history, question_type, node, relation, leaf_node, yon, hint):
    driver = getDriver()    
    with driver.session() as session:
        seasons_ids = session.read_transaction(match_seasons_ids)

    for ID in history['Season_Type']:
        if ID in seasons_ids:
            seasons_ids.remove(ID)

    with driver.session() as session:
        season_foods = session.read_transaction(match_foods_from_season_id, np.random.choice(seasons_ids, 1).item())
    season_foods_ids = [season_food.id for season_food in season_foods]
    for ID in history['FOOD']  + history['Season_Type']:
        if ID in season_foods_ids:
            season_foods_ids.remove(ID)

    if len(season_foods_ids) != 0:
        next_question_type = question_type
        next_node = get_node_from_id(np.random.choice(season_foods_ids, 1).item())
        next_relation = 'has_intro_info'
        next_leaf_node = get_leaf_node_from_node_relation(next_node, next_relation)
        next_hint = hint
        ret = (next_question_type, next_node, next_relation, next_leaf_node, next_hint, False, 1)
    else:
        ret = move_next_category(history)                         

    return ret

######################################
def match_nodes_from_labels(tx, labels):
    nodes = []
    for record in tx.run("MATCH (n:{}) RETURN n".format(labels)):
        nodes.append(record['n'])
    return nodes

def match_hint_from_leaf_node(tx, leaf_node_id):
    for record in tx.run("MATCH (n) WHERE id(n) = {} RETURN n".format(leaf_node_id)):
        leaf_node = record['n']

    maxlen = get_node_hint_len(leaf_node)
    """
    if leaf_node['len'] == None:
        maxlen = 0
        for i in range(1, 1000):
            if 'hint' + str(i) not in leaf_node:
                maxlen = i-1
                break
    else:
        maxlen = leaf_node['len']
    """        
    hints = {}
    #for i in range(1, leaf_node['len']+1):
    for i in range(1, maxlen + 1):
        hints['hint' + str(i)] = leaf_node['hint' + str(i)]

    return hints

def match_question_type_from_entity(tx, entity):
    question_type = None
    for record in tx.run("MATCH (q:Question_Type) WHERE q.entity = \"{}\" RETURN q".format(entity)):
        question_type = record['q']
        
    return question_type

def get_random_entity_relation_from_entity(entity):
    driver = getDriver()    
    with driver.session() as session:
        #Get all question types & Select one type.
        question_type = session.read_transaction(match_question_type_from_entity, entity)

        #Get initial node in the type.
        node, relation = session.read_transaction(match_init_node_relation, question_type)

        if question_type['entity'] == 'tour':
            leaf_node = session.read_transaction(match_init_leaf_node, node, relation)
            maxlen = get_node_hint_len(leaf_node)
            #hint = 'hint' + str(np.random.choice(leaf_node['len'], 1)[0] + 1)
            hint = 'hint' + str(np.random.choice(maxlen, 1)[0] + 1)
        elif relation == None:
            leaf_node = None
            maxlen = get_node_hint_len(node)
            #hint = 'hint' + str(np.random.choice(node['len'], 1)[0] + 1)
            hint = 'hint' + str(np.random.choice(maxlen, 1)[0] + 1)
        else:
            leaf_node = session.read_transaction(match_init_leaf_node, node, relation)
            hint = None
        
    return question_type, node, relation, leaf_node, hint

def match_relations(tx, node, relation):
    relations = []
    for record in tx.run("MATCH (e)-[r:{}]-(ee) WHERE id(e) = {} RETURN e, r, ee".format(relation, node.id)):
        relations.append(record['r'])
    return relations

##############


def get_next_entity(history, entity):
    driver = getDriver()
    with driver.session() as session:
        next_entity, next_relation, is_changed = session.read_transaction(match_relations, history, entity)
    return next_entity, next_relation, is_changed
#OK
"""
def match_relations(tx, history, entity):
    relations = []
    for record in tx.run("MATCH (e)-[r]-() WHERE e.name = \"" + entity + "\" RETURN e, r"):
        relations.append(record['r'].type)

    for relation in relations:
        if entity in history:
            if relation not in history[entity]:
                return entity, relation, False
        else:
            return entity, relation, False

    for record in tx.run("MATCH (e) WHERE e.name = \"" + entity + "\" RETURN labels(e)"):
        label = record['labels(e)'][0]

    for record in tx.run("MATCH (e:" + label + ") RETURN e.name"):
        next_entity = record['e.name']
        print("record: ", record['e.name'])
        if next_entity == entity or next_entity in history:
            continue
        next_relation = "has_intro_info"
        break

        next_relations = []
        for record in tx.run("MATCH (e)-[r]-(ee) WHERE e.name = \"" + next_entity + "\" RETURN e, r, ee"):
            next_relations.append(record['r'].type)

        for next_relation in next_relations:
            if next_entity in history:
                if next_relation not in history[next_entity]:
                    return next_entity, next_relation, True
            else:
                return next_entity, next_relation, True
    return next_entity, next_relation, True
"""
#OK
def get_other_entity(history, entity):
    driver = getDriver()    
    with driver.session() as session:
        other_type = session.read_transaction(match_other_entity, history, entity)
        other_entity, relation = session.read_transaction(match_random_entity, history, other_type)
    return other_entity, relation
#OK
def match_other_entity(tx, history, entity):
    for record in tx.run("MATCH (e) WHERE e.name = \"" + entity + "\" RETURN labels(e)"):
        label = record['labels(e)'][0]

    if label == "GreatMan":
        other = "FOOD"
    elif label == "FOOD":
        other = "GreatMan"

    return other
#OK
def match_random_entity(tx, history, other_type):
    for record in tx.run("MATCH (n:" + other_type + ") with n, rand() AS r ORDER BY r return n.name LIMIT 1"):
        other_entity = record['n.name']

    """
    relations = []
    for record in tx.run("MATCH (n)-[r]-() WHERE n.name = \"" + other_entity + "\" RETURN n, type(r)"):
        relations.append(record['type(r)'])
    """
    relation = "has_intro_info"
    return other_entity, relation
    #return other_entity, random.choice(relations)

#OK
def get_from_relation_to_name(entity, relation):
    driver = getDriver()    
    with driver.session() as session:
        name = session.read_transaction(match_name, entity, relation)
    return name
#OK
def match_name(tx, entity, relation):
    for record in tx.run("MATCH (e)-[r:" + relation + "]-(ee) WHERE e.name = \"" + entity + "\" RETURN e, r, ee.name"):
        name = record['ee.name']
    return name
        
def get_next(history, entity):
    driver = getDriver()    
    with driver.session() as session:
        next_entity, next_relation = session.read_transaction(match_next, history, entity)
    return next_entity, next_relation

def match_next(tx, history, entity):
    relations = []
    for record in tx.run("MATCH (e)-[r]-(ee) WHERE e.name = \"" + entity + "\" RETURN e, type(r), ee"):
        relations.append(record['type(r)'])

    for relation in relations:
        if entity in history:
            if relation not in history[entity]:
                return entity, relation
        else:
            return entity, relation

def checkTrait(c):
    return (int((ord(c) - 0xAC00) % 28) != 0)

def get_question_type_from_node_relation(node, relation):
    if relation in ["has_purchase_info", "has_storage_info", "has_refine_info", "has_goods_info", "has_cal_info"]:
        if node['type'] == "제철음식":
            entity = "Season_Type"
        else:
            entity = "FOOD"
    elif relation == "has_flower_hint":
        entity = "flower"
    elif relation in ["has_prevention", "has_good_food"]:
        # NEW : add case --
        if node['type'] == "Body":
            entity = "Body"
        else:
            # MOVE --
            entity = "illness"
            # -- move end
        # -- end
    # NEW : add case
    elif relation == "has_tip_info":
        entity = "Body"
    # -- end
    elif relation in ["has_tour_info", "has_tour_reco"]:
        entity = "tour"
    elif relation in ["has_music_info", "has_song_info"]:
        entity = "oldsong"
    elif relation == "has_movie_info":
        entity = "movie"
    elif relation == "has_drama_info":
        entity = "drama"
    elif relation == "has_popword_info":
        entity = "popword"
    elif relation == "has_career_info":
        entity = "GreatMan"
    elif relation == "has_intro_info":
        if node['type'] == "제철음식":
            entity = "Season_Type"
        elif node['type'] == "음식":
            entity = "FOOD"
        # NEW : add case --
        elif node['type'] == "Event":
            entity = "Event"
        elif node['name'] == "취미":
            entity= "Hobby"
        # -- end
        else:
            entity = "GreatMan"
    # NEW : add case --
    elif relation == "has_Datetime":
        entity = "Event"
    # -- end
    elif relation == "has_season_food":
        entity = "Season_Type"
    elif relation == "has_idol_era":
        entity = "idol_era"
    elif relation == "has_lifetime_info":
        entity = "GreatMan"
    else:
        raise Exception("Can't infer question type: {}".format(relation))
    driver = getDriver()
    with driver.session() as session:
        question_type = session.read_transaction(match_question_type_from_entity, entity)
    
    return question_type
