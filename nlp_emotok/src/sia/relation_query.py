#그래피 디비를 활용하여 트리플 형태의 데이터를 가져오는 코드
from neo4j import GraphDatabase
from .. import pyjosa
import os,random
import csv

#relation 정보
filename_path = os.path.dirname(os.getcwd())+'/nlp_emotok/src/sia/relation/relation_info.csv'
f = open(filename_path, 'r')
relation_list = f.readlines()

'''
#node_template 정보
node_relation=[]
with open("/usr/local/roja-dasom/nlp-beanq-service/src/dasom2/sia/template/template.csv", 'r',encoding='utf-8') as file:
    template=csv.reader(file)

    for a in template:
        node_relation.append(a)
'''
#로그인 드라이버
driver = GraphDatabase.driver("bolt://35.229.155.246:7000", auth=("neo4j", "1thefull322"))

#힌트로 끝나는 노드
def get_hint(tx,entity,relation):
    for a in tx.run("Match (n{name:$entity})-[:"+relation+"]->(b) return keys(b)",entity=entity):
        for n,word in enumerate(a["keys(b)"]):
            if "name" in a["keys(b)"]:
                a["keys(b)"].remove("name")
            if "type" in a["keys(b)"]:
                a["keys(b)"].remove("type")
        hint=random.choice(a["keys(b)"])

        for b in tx.run("Match (n{name:$entity})-[:"+relation+"]->(b) return b."+hint,entity=entity):
            return b["b."+hint]

    return 0

#노드로 끝나는 것 가져오기
def get_node(tx,entity,relation):
    result = []
    for a in tx.run("Match (n{name:$entity})-[:" + relation + "]->(b) return b.name", entity=entity):
        result.append(a['b.name'])
        '''
        for tem_relation in node_relation:
            if tem_relation[1] == relation:
                return pyjosa.replace_josa(tem_relation[0] % (entity, a["b.name"]))
        '''
    if len(result) == 0:
	    return 0
    else:
        return random.choice(result)

#예외 생애 가져오기
def get_lifetime(tx,entity,relation):
    for a in tx.run("Match (n:LifeTime{type:$entity}) return n.birth, n.death ", entity=entity):
        if a['n.birth'] =="없음":
            if a['n.death'] =="없음":
                return pyjosa.replace_josa(entity+"(은)는 정확한 출생정보와 사망정보가 없어요!")
            else:
                return pyjosa.replace_josa(entity + "(은)는 정확한 출생정보는 없지만 "+a['n.death']+"년도까지 살았대요!")
        else:
            if a['n.death'] == "없음":
                return pyjosa.replace_josa(entity + "(은)는 정확한 사망정보는 없지만 " + a['n.birth'] + "년도에 태어났대요!!")
            else:
                return pyjosa.replace_josa(entity+"(은)는 " +  a['n.birth'] + "년도에 태어나서 "+ a['n.death']+ "년도까지 살았대요!")
    return 0

#예외인 아이돌 가져오기 (아이돌,has_idol,1990년도)
def get_idol(tx,entity,relation):
    for a in tx.run("Match (n:era{name:$entity})-[:has_idol_era"+"]->(b) return b.name",entity=entity):
        idol_era=a["b.name"]
        for c in tx.run("Match (n{name:$idol_era})-[:" + relation + "]->(b) with b, rand() As r order by r return b.name limit 1",idol_era=idol_era):
            return entity+"로는 " +c["b.name"]+"이 있어요!"
    return 0

def get_sia_data(_json):
	for relation in relation_list:
		relation = relation.split(',')
		if relation[0] == _json['relation']:
			func = relation[1]

	func = func.replace('\n','')
	
	with driver.session() as session:
		if func == "get_hint":
			response = session.read_transaction(get_hint, _json['entity'],_json['relation'])
		elif func == "get_node":
			response = session.read_transaction(get_node, _json['entity'],_json['relation'])
		elif func == "get_idol":
			response = session.read_transaction(get_idol, _json['entity'],_json['relation'])
		elif func == "get_lifetime":
			response = session.read_transaction(get_lifetime, _json['entity'],_json['relation'])
	return response
	
def get_amumal_data(_json):
	with driver.session() as session:
		#relation_추출
		rand_relation= session.read_transaction(get_amumal, _json['entity'])
		#hint_추출
		#lifetime일때
		if rand_relation=="has_lifetime_info":
			response = session.read_transaction(get_lifetime, _json['entity'], rand_relation)
		#그냥 힌트일때
		else :
			response = session.read_transaction(get_hint, _json['entity'], rand_relation)

	return response
def get_amumal(tx, entity):
    relation_list=[]
    for a in tx.run("Match (n{name:$entity})-[r]->(b) return type(r) ", entity=entity):
        relation_list.append(a['type(r)'])
    for a in relation_list:
        if a=='type_of':
            relation_list.remove(a)
    return random.choice(relation_list)

#API 1
def get_random_entity_relation():
    with driver.session() as session:
        entity, relation = session.read_transaction(match_random_entity_relation)
    return entity, relation

def match_random_entity_relation(tx):
    entity = None
    relation = "has_intro_info"
    if random.random() >= 0.5:
        for record in tx.run("MATCH (f:FOOD) with f, rand() AS r ORDER BY r RETURN f.name LIMIT 1"):
            entity = record['f.name']
    else:
        for record in tx.run("MATCH (g:GreatMan) WITH g, rand() AS r ORDER BY r RETURN g.name LIMIT 1"):
            entity = record['g.name']

    return entity, relation

#API 2
def get_answer(entity, relation):
    with driver.session() as session:
        answer = session.read_transaction(match_answer, entity, relation)
    return answer

def match_answer(tx, entity, relation):
    for record in tx.run("MATCH (e)-[r:" + relation + "]-(ee) WHERE e.name = \"" + entity + "\" RETURN e, r, ee"):
        if relation == 'has_lifetime_info':
            birth = record['ee']['birth']
            death = record['ee']['death']
            answer = birth + "년에서 " + death + "년까지 살았었어요."
        else:
            answer = record['ee']['hint']
    return answer

def get_next_entity(history, entity):
    with driver.session() as session:
        next_entity, next_relation, is_changed = session.read_transaction(match_relations, history, entity)
    return next_entity, next_relation, is_changed
#OK
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
        if next_entity == entity or next_entity in history:
            continue
        next_relation = "has_intro_info"
        break
        """
        next_relations = []
        for record in tx.run("MATCH (e)-[r]-(ee) WHERE e.name = \"" + next_entity + "\" RETURN e, r, ee"):
            next_relations.append(record['r'].type)

        for next_relation in next_relations:
            if next_entity in history:
                if next_relation not in history[next_entity]:
                    return next_entity, next_relation, True
            else:
                return next_entity, next_relation, True
        """
    return next_entity, next_relation, True

#OK
def get_other_entity(history, entity):
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
    with driver.session() as session:
        name = session.read_transaction(match_name, entity, relation)
    return name
#OK
def match_name(tx, entity, relation):
    for record in tx.run("MATCH (e)-[r:" + relation + "]-(ee) WHERE e.name = \"" + entity + "\" RETURN e, r, ee.name"):
        name = record['ee.name']
    return name
        
def get_next(history, entity):
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
