import pytest
from main import Mongo_Client
from traceback import print_stack

testr = Mongo_Client()

def test_connect():
    result = testr.connect()
    assert(result is not None)

def test_create():
    result = testr.create()
    assert(result is None)
     
def test_load():
     testr.delete_all()
     result = testr.load()
     assert(len(result) == 2 and  result[0] == 1000 and result[1] == 10000)
    
    
def test_update():
    result = testr.update("3,2022-12-19 14:48:21,4,Name#3,email3@abcddd.com,439538,127484,2")
    assert(result is not None)
    assert(result.matched_count==1)


def test_query1():
    result = testr.query1(1)
    assert(result is not None)
    assert(result['id']==1)
    
    result = testr.query1(949)
    assert(result is not None)
    assert(result['id']==949)


def test_query2():
    result = testr.query2(1)
    assert result is not None
    assert(",".join([ str(row['id']) for row in result]) == '638,970,574,547,620,855,194,322,260,478')
    
    result = testr.query2(9)
    assert(result is not None)
    assert(",".join([ str(row['id']) for row in result]) == '243,765,567,157,879,43,715,367,192,269')



def test_query3():
    result = testr.query3(2,"2022-12-17 05:30:00","2022-12-17 15:00:00")
    assert(result is not None)
    assert(",".join([ str(row['_id']['id']) for row in result]) == '50,421,516,797,179')
    
    result = testr.query3(7,"2022-12-18 00:00:00","2022-12-19 11:00:00")
    assert(result is not None)
    assert(",".join([ str(row['_id']['id']) for row in result]) == '32,186,557,911,277')
    
   
