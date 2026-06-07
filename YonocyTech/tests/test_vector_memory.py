import pytest
import os
import shutil
from memory.vector_store import VectorMemory

def test_vm_add_and_search():
    path = "tests/temp_chroma"
    vm = VectorMemory(persist_directory=path)
    vm.add("The capital of France is Paris", {"city": "Paris"}, "id1")

    results = vm.search("Where is Paris?")
    assert len(results) > 0
    assert "Paris" in results[0]["text"]

    shutil.rmtree(path)

def test_vm_count():
    path = "tests/temp_chroma_count"
    vm = VectorMemory(persist_directory=path)
    vm.add("text 1", {}, "1")
    vm.add("text 2", {}, "2")
    assert vm.count() == 2
    shutil.rmtree(path)

def test_vm_empty_search():
    path = "tests/temp_chroma_empty"
    vm = VectorMemory(persist_directory=path)
    results = vm.search("nothing")
    assert results == []
    shutil.rmtree(path)

def test_vm_delete():
    path = "tests/temp_chroma_del"
    vm = VectorMemory(persist_directory=path)
    vm.add("delete me", {}, "del_id")
    vm.delete("del_id")
    assert vm.count() == 0
    shutil.rmtree(path)

def test_vm_clear_all():
    path = "tests/temp_chroma_clear"
    vm = VectorMemory(persist_directory=path)
    vm.add("a", {}, "1")
    vm.add("b", {}, "2")
    vm.clear_all()
    assert vm.count() == 0
    shutil.rmtree(path)
