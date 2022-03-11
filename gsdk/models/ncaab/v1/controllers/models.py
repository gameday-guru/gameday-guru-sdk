from typing import Any, Dict, Sequence, Tuple, Set, Protocol
from uuid import uuid4
import redis
from redis.commands.json.path import Path
import datetime
import copy


class EfficiencyPayloadlike(Protocol):
    team_id : str
    possessions : float
    kadjoeff : float
    kadjdeff : float
    badjoeff : float
    badjdeff : float
    radjdeff : float
    radjoeff : float

class EfficiencyPayload(EfficiencyPayloadlike):

    def __init__(self, d : Dict[str, Any]) -> None:
        """Creates an efficiency payload from a dictionary that ought to contain the necessary values.

        Args:
            d (Dict[str, str]): _description_
        """
        self.team_id = d["team_id"]
        self.possessions = float(d["possessions"])
        self.kadjoeff = float(d["kadjoeff"])
        self.kadjdeff = float(d["kadjdeff"])
        self.badjoeff = float(d["badjoeff"])
        self.badjdeff = float(d["badjdeff"])
        self.radjoeff = float(d["radjoeff"])
        self.radjdeff = float(d["radjdeff"])

class EfficiencyDriverUniversalControls:

    key : str
    id : str
    namespace : str
    last_modified : datetime.datetime
    client : redis.Redis[bytes]

    @classmethod
    def day_str(cls, date : datetime.date)->str:
        return date.strftime("%d/%m/%Y")

    @classmethod
    def today_str(cls)->str:
        """Computes the string representation of today.

        Returns:
            str: _description_
        """
        return datetime.date.today().strftime("%d/%m/%Y")

    @classmethod
    def week_date_str(cls)->str:
        """Computes the string for the week

        Returns:
            str: _description_
        """
        return (datetime.date.today() 
        +  datetime.timedelta(6 - datetime.date.today().weekday())).strftime("%d/%m/%Y")

    @classmethod
    def uuid(cls)->str:
        """Generates a univeral unique identifier.

        Returns:
            str: _description_
        """
        return uuid4().bytes.decode("utf-8")

    @classmethod
    def produce_key(cls, namespace : str, id : str,)->str: 
        """Produces a key from a namespace and and id.

        Args:
            namespace (str): is the namespace
            id (str): is the id

        Returns:
            str: the key
        """
        return f"{namespace}:{id}"

    @classmethod
    def get_namespace(cls, val : str)->str:
        """Gets the namespace from a string.

        Args:
            val (str): _description_

        Returns:
            str: _description_
        """
        return val.split(":")[0]

    @classmethod
    def get_id(cls, val : str)->str:
        """Gets the id from a string.

        Args:
            val (str): _description_

        Returns:
            str: _description_
        """
        return val.split(":")[1]

    def rel(self, id : str)->str:
        """Produces a key relative to the namespace in which this object currently exists.

        Args:
            id (str): _description_

        Returns:
            str: _description_
        """
        return self.produce_key(self.namespace, id)

    def reify_key(self):
        """Sets self.key to a key which reflects the id and the namespace.

        Returns:
            _type_: _description_
        """
        self.key = self.produce_key(self.id, self.namespace)
        return self

    def populate_from_key(self, key : str):
        self.key = key
        self.namespace = self.get_namespace(key)
        self.id = self.get_id(key)
        return self

    def set_namespace(self, namespace : str):
        self.namespace = namespace
        return self

    def get(self)->Any:
        return self.client.json().get(self.key, Path.rootPath())

    def set(self, val : Any)->Any:
        return self.client.json().set(self.key, Path.rootPath(), val)

    def mlog(self):
        """Logs a modification event.

        Returns:
            _type_: _description_
        """
        self.last_modified = datetime.datetime.now()
        return self

    def gen(self):
        new = copy.deepcopy(self)
        new.id = self.uuid()
        return new

class EfficiencyRedisMeta(EfficiencyDriverUniversalControls):

    id : str
    head : str
    date_index : Dict[str, str]
    week_index : Dict[str, str]
    client : redis.Redis[bytes]

    def __init__(
        self, 
        key : str,
        client : redis.Redis[Any]
    )->None:
        self.populate_from_key(key)
        self.client = client
        self.date_index = {}

    def new(self)->'EfficiencyRedisMeta':
        """Makes an entirely new version of the Meta.

        Returns:
            EfficiencyRedisMeta: _description_
        """
        self.id = self.uuid()
        self.head = self.uuid() # this will be handled lazily by the head driver
        self.mlog().date_index[self.today_str()] = self.head
        return self

    def serialize(self)->'EfficiencyRedisMeta':
        """Serializes the Meta.

        Returns:
            EfficiencyRedisMeta: _description_
        """
        return self.reify_key() \
            .set({
                "id" : self.id,
                "head" : self.head,
                "date_index" : self.date_index
            })

    def populate(self)->'EfficiencyRedisMeta':
        """Populates the Meta.

        Returns:
            EfficiencyRedisMeta: _description_
        """
        # use the client to get the value by its id
        val = self.get()
        if not val:
            self.new().deep_serialize()
        self.id = val["id"]
        self.head = val["head"]
        self.date_index = val["date_index"]
        self.week_index = val["week_index"]
        return self

    def stage_head(self, head : str)->'EfficiencyRedisMeta':
        """Adds a head to the Meta. Does not serialize

        Args:
            head (str): the key of the head.

        Returns:
            EfficiencyRedisMeta: _description_
        """
        self.head = head
        self.week_index[self.week_date_str()] = self.head
        self.mlog().date_index[self.today_str()] = self.head
        return self

    def add_head(self, head : str)->'EfficiencyRedisMeta':
        """Adds a head to the meta. Serializes.

        Args:
            head (str): is the key for the head.

        Returns:
            EfficiencyRedisMeta: _description_
        """
        return self.stage_head(head).serialize()

    def clone_to(self, namespace : str)->Tuple['EfficiencyRedisMeta', 'EfficiencyRedisMeta']:
        """Clones the meta and its heads and members to a new namespace.

        Returns:
            _type_: _description_
        """
        new = EfficiencyRedisMeta(self.key, self.client) \
            .set_namespace(namespace) \
            .serialize()
        EfficiencyRedisHead(self.rel(self.head), self.client) \
            .clone_to(namespace)
        # tell all of the values in the date_index to clone themselves

        return (self, new)

    def clone(self)->Tuple['EfficiencyRedisMeta', 'EfficiencyRedisMeta']:
        """Clones the meta and its heads and members.

        Returns:
            _type_: _description_
        """
        return self.clone_to(self.uuid())

    def deep_serialize(self)->'EfficiencyRedisMeta':
        """Serializes the Meta, all of its heads, and all of its heads' members.

        Returns:
            EfficiencyRedisMeta: _description_
        """
        return self

    def commit_efficiency(self, efficiency_payload : EfficiencyPayload)->'EfficiencyRedisMeta':
        """Commits an efficiency payload.

        Args:
            efficiency_payload (EfficiencyPayload): _description_

        Returns:
            EfficiencyRedisMeta: _description_
        """
        self.head = EfficiencyRedisHead(self.rel(self.head), self.client).push(efficiency_payload).id
        return self

    def get_team_efficiency(self, team_id : str, date : datetime.date)->EfficiencyPayload:
        """Gets the team efficiency.

        Args:
            team_id (str): _description_
            date (datetime.date): _description_

        Returns:
            EfficiencyPayload: _description_
        """
        head = EfficiencyRedisHead(self.rel(self.date_index[self.day_str(date)]), self.client)
        member = EfficiencyRedisMember(head.rel(head.members[team_id]), self.client)
        return member.to_payload()




class EfficiencyRedisHead(EfficiencyDriverUniversalControls):
    
    meta : str
    prev : Sequence[str]
    next : Sequence[str]
    members : Dict[str, str]

    def __init__(self, key : str, client : redis.Redis[bytes]) -> None:
        self.populate_from_key(key)
        self.client = client
        self.prev = []
        self.next = []
        self.members = {}

    def new(
        self,
        meta : str = EfficiencyRedisMeta.uuid(),
        prev : Sequence[str] = [],
        next : Sequence[str] = [],
        members : Dict[str, str] = {}
    )->'EfficiencyRedisHead':
        """Makes an entirely new version of the Meta.

        Returns:
            EfficiencyRedisMeta: _description_
        """
        self.id = self.uuid()
        self.meta = meta
        self.prev = prev
        self.next = next
        self.members = members
        return self

    def push(self, efficiency_payload : EfficiencyPayload)->'EfficiencyRedisHead':
        new_head = self.gen()
        new_head.prev = [self.id]
        new_head.next = []
        new_member = EfficiencyRedisMember.create(
            self.namespace,
            self.client,
            efficiency_payload,
            [new_head.id]
        ).serialize()
        new_head.members[efficiency_payload.team_id] = new_member.id
        return new_head


    def get_tree_as_sequence(self, found : Set[str]=set())->Sequence[str]:
        """Gets the tree as a sequence

        Args:
            found (Set[str], optional): _description_. Defaults to set().

        Returns:
            Sequence[str]: _description_
        """

        if self.id not in found:
            found.add(self.id)

        for node in set([*self.prev, *self.next]) - found:
            if node not in found:
                EfficiencyRedisHead(self.rel(node), self.client).get_tree_as_sequence(found)

        return list(found)

    def clone_members_to(self, namespace : str)->'EfficiencyRedisHead':
        """_summary_

        Args:
            namespace (str): _description_

        Returns:
            EfficiencyRedisHead: _description_
        """
        for member in self.members:
            # change the namespace
            EfficiencyRedisMember(self.rel(self.members[member]), self.client) \
                .set_namespace(namespace) \
                .serialize()
        return self

    def clone_to(self, namespace : str)->Tuple['EfficiencyRedisHead', 'EfficiencyRedisHead']:
        """Clones the head and associated nodes to a new 
        namespace.

        Returns:
            _type_: _description_
        """
        new = EfficiencyRedisHead(self.key, self.client) \
            .set_namespace(namespace) \
            .serialize() \
            .clone_members_to(namespace)
        for node in self.get_tree_as_sequence(found=set([new.key])):
            EfficiencyRedisHead(self.rel(node), self.client) \
                .set_namespace(namespace) \
                .serialize() \
                .clone_members_to(namespace)
        return (self, new)

    def serialize(self)->'EfficiencyRedisHead':
        """Serializes the efficiency head.

        Returns:
            EfficiencyRedisHead: _description_
        """
        self.mlog().set({
            "meta" : self.meta,
            "prev" : self.prev,
            "next" : self.next,
            "members" : self.members
        })
        return self
        

class EfficiencyRedisMember(EfficiencyDriverUniversalControls):

    id : str
    heads : Sequence[str]
    team_id : str
    possessions : float
    kadjoeff : float
    kadjdeff : float
    badjoeff : float
    badjdeff : float
    radjdeff : float
    radjoeff : float

    def __init__(self, key : str, client : redis.Redis[bytes])->None:
        """Initializes an efficiency member.

        Args:
            key (str): _description_
            client (redis.Redis[bytes]): _description_
        """
        self.populate_from_key(key)
        self.client = client

    @classmethod
    def create(cls, 
        namespace : str, 
        client : redis.Redis[bytes],
        efficiency_payload : EfficiencyPayload,
        heads : Sequence[str]
    )->'EfficiencyRedisMember':
        """Helper for creating an efficiency member.

        Args:
            namespace (str): _description_
            client (redis.Redis[bytes]): _description_
            efficiency_payload (EfficiencyPayload): _description_
            heads (Sequence[str]): _description_

        Returns:
            EfficiencyRedisMember: _description_
        """
        new = EfficiencyRedisMember(cls.produce_key(namespace, cls.uuid()), client)
        new.possessions = efficiency_payload.possessions
        new.kadjoeff = efficiency_payload.kadjoeff
        new.kadjdeff = efficiency_payload.kadjdeff
        new.badjoeff = efficiency_payload.badjoeff
        new.badjdeff = efficiency_payload.badjdeff
        new.radjoeff = efficiency_payload.radjoeff
        new.radjdeff = efficiency_payload.radjdeff
        new.heads = heads
        return new


    def serialize(self)->'EfficiencyRedisMember':
        """Serializes the efficiency Redis member.

        Returns:
            EfficiencyRedisMember: _description_
        """
        self.mlog().set({
            "heads" : self.heads,
            "team_id" : self.team_id,
            "possessions" : self.possessions,
            "kedjoeff" : self.kadjoeff,
            "kadjdeff" : self.kadjdeff,
            "badjoeff" : self.badjoeff,
            "badjdeff" : self.badjdeff,
            "radjoeef" : self.radjoeff,
            "radjdeff" : self.radjdeff
        })
        return self

    def to_payload(self)->EfficiencyPayload:
        """Turns the efficiency member into an efficiency payload.

        Returns:
            EfficiencyPayload: _description_
        """
        return EfficiencyPayload({
            "heads" : self.heads,
            "team_id" : self.team_id,
            "possessions" : self.possessions,
            "kedjoeff" : self.kadjoeff,
            "kadjdeff" : self.kadjdeff,
            "badjoeff" : self.badjoeff,
            "badjdeff" : self.badjdeff,
            "radjoeef" : self.radjoeff,
            "radjdeff" : self.radjdeff
        })
