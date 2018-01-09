'''
大数据搜索splunk实现例子
布隆过滤器 + 分词 + 搜索
分词的目的是要把我们的文本数据分割成可搜索的最小单元

'''
class Bloomfilter(object):
    def __init__(self,size):
        self.values = [False]*size
        self.size = size

    def hash_value(self,value):
        return  hash(value)%self.size

    def add_value(self,value):
        h = self.hash_value(value)
        self.values[h] = True

    def might_contain(self,value):
        h = self.hash_value(value)
        return self.values[h]

    def print_contents(self):
        print(self.values)

'''
主要分割

主要分割使用空格来分词，实际的分词逻辑中，还会有其它的分隔符。例如Splunk的缺省分割符包括以下这些，用户也可以定义自己的分割符。
'''
def major_segments(s):
    major_breaks = ' '
    last = -1
    results = set()
    for idx,ch in enumerate(s):
        if ch in major_breaks:
            segment = s[last + 1:idx]
            results.add(segment)
            last = idx
    segment = s[last+1:]
    results.add(segment)
    return results

'''
次要分割

次要分割和主要分割的逻辑类似，只是还会把从开始部分到当前分割的结果加入。例如“1.2.3.4”的次要分割会有1，2，3，4，1.2，1.2.3

分词的逻辑就是对文本先进行主要分割，对每一个主要分割在进行次要分割。然后把所有分出来的词返回。
'''
def minor_segments(s):
    minor_breaks = '_.'
    last = -1
    results = set()

    for idx,ch in enumerate(s):
        if ch  in minor_breaks:
            segment = s[last+1:idx]
            results.add(segment)
            segment = s[:idx]
            results.add(segment)
            last = idx
    segment = s[last+1:]
    results.add(segment)
    results.add(s)
    return results

def segments(event):
    results = set()
    for major in major_segments(event):
        for minor in minor_segments(major):
            results.add(minor)
    return results


'''

    Splunk代表一个拥有搜索功能的索引集合
    每一个集合中包含一个布隆过滤器，一个倒排词表（字典），和一个存储所有事件的数组
    当一个事件被加入到索引的时候，会做以下的逻辑
        为每一个事件生成一个unqie id，这里就是序号
        对事件进行分词，把每一个词加入到倒排词表，也就是每一个词对应的事件的id的映射结构，注意，一个词可能对应多个事件，所以倒排表的的值是一个Set。倒排表是绝大部分搜索引擎的核心功能。
    当一个词被搜索的时候，会做以下的逻辑
        检查布隆过滤器，如果为假，直接返回
        检查词表，如果被搜索单词不在词表中，直接返回
        在倒排表中找到所有对应的事件id，然后返回事件的内容

'''
class Splunk(object):
    def __init__(self):
        self.bf = Bloomfilter(64)
        self.terms = {}
        self.events = []
    def add_event(self,event):
        event_id = len(self.events)
        self.events.append(event)
        for term in segments(event):
            self.bf.add_value(term)
            if term not in self.terms:
                self.terms[term] = set()
            self.terms[term].add(event_id)
    def search(self,term):
        if not self.bf.might_contain(term):
            return
        if term not in self.terms:
            return
        for event_id in sorted(self.terms[term]):
            yield self.events[event_id]


class SplunkM(object):
    def __init__(self):
        self.bf = Bloomfilter(64)
        self.terms = {}  # Dictionary of term to set of events
        self.events = []

    def add_event(self, event):
        """Adds an event to this object"""

        # Generate a unique ID for the event, and save it
        event_id = len(self.events)
        self.events.append(event)

        # Add each term to the bloomfilter, and track the event by each term
        for term in segments(event):
            self.bf.add_value(term)
            if term not in self.terms:
                self.terms[term] = set()

            self.terms[term].add(event_id)

    def search_all(self, terms):
        """Search for an AND of all terms"""

        # Start with the universe of all events...
        results = set(range(len(self.events)))

        for term in terms:
            # If a term isn't present at all then we can stop looking
            if not self.bf.might_contain(term):
                return
            if term not in self.terms:
                return

            # Drop events that don't match from our results
            results = results.intersection(self.terms[term])

        for event_id in sorted(results):
            yield self.events[event_id]

    def search_any(self, terms):
        """Search for an OR of all terms"""
        results = set()

        for term in terms:
            # If a term isn't present, we skip it, but don't stop
            if not self.bf.might_contain(term):
                continue
            if term not in self.terms:
                continue

            # Add these events to our results
            results = results.union(self.terms[term])

        for event_id in sorted(results):
            yield self.events[event_id]

if __name__ == '__main__':
    bf = Bloomfilter(10)
    bf.add_value('dog')
    bf.add_value('fish')
    bf.add_value('cat')
    bf.print_contents()
    bf.add_value('bird')
    bf.print_contents()

    for item in ['dog', 'fish', 'cat', 'bird', 'duck', 'emu']:
        print('{}:{} {}'.format(item, bf.hash_value(item), bf.might_contain(item)))

    print("test segments----")
    for item in segments("src_ip=1.2.3.4"):
        print(item)

    print("test splunk----")

    s = Splunk()
    s.add_event('src_ip = 1.2.3.4')
    s.add_event('src_ip = 5.6.7.8')
    s.add_event('dst_ip = 1.2.3.4')

    for event in s.search('1.2.3.4'):
        print(event)
    print('-')
    for event in s.search('src_ip'):
        print(event)
    print('-')
    for event in s.search('ip'):
        print(event)

    print("test splunkm----")
    s = SplunkM()
    s.add_event('src_ip = 1.2.3.4')
    s.add_event('src_ip = 5.6.7.8')
    s.add_event('dst_ip = 1.2.3.4')

    for event in s.search_all(['src_ip', '5.6']):
        print(event)
    print( '-')
    for event in s.search_any(['src_ip', 'dst_ip']):
        print(event)