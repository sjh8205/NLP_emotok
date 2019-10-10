import relation_query

def random(req):
    _json = dict()
    entity, relation = relation_query.get_random_entity_relation()
    _json['entity'] = entity
    _json['relation'] = relation
    _json['history'] = {}
    _json['yon'] = 0
    _json['add_q'] = entity + "에 대해 알려드릴까요?"
    
    return _json

def successive(req):
    entity = req['entity']
    relation = req['relation']
    history = req['history']

    if entity in history:
        if relation not in history[entity]:
            history[entity].append(relation)
    else:
        history[entity] = [relation]

    _json = dict()
    _json['history'] = history

    #Make answer and successive question in same context
    if req['yon'] == 0:
        _json['answer'] = relation_query.get_answer(entity, relation)


        next_entity, next_relation, is_changed = relation_query.get_next_entity(history, entity)

        current_name = relation_query.get_from_relation_to_name(entity, relation)
        if is_changed:
            next_name = relation_query.get_from_relation_to_name(next_entity, next_relation)
            _json['add_q'] = entity + " 외에 " + next_entity + " 대해서 알려드릴까요?"
        else:
            next_name = relation_query.get_from_relation_to_name(entity, next_relation)
            _json['add_q'] = current_name + " 외에 " + next_name + " 대해서 알려드릴까요?"

            _json['entity'] = next_entity
            _json['relation'] = next_relation

    #Only make successive question in other context (find sibling entity)
    elif req['yon'] == 1:
        next_entity, next_relation  = relation_query.get_other_entity(history, entity)

        _json['entity'] = next_entity                
        _json['relation'] = next_relation

        index = random.randint(0, 2)
        if index == 0:
            _json['add_q'] = "그럼 이번에는 " + next_entity + "에 대해 알려드릴까요?"              
        elif index == 1:
            _json['add_q'] = "그렇다면 " + next_entity + " 관련해서는 궁금하지 않으세요?"              
        else:
            _json['add_q'] = "으음 다른 이야기를 해볼까요? " + next_entity + "에 관해 소개해드릴까요?"

    _json['yon'] = req['yon']
    
    return _json
