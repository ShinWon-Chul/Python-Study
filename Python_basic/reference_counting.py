class Foo:
    def __init__(self):
        self.value = 1
        self.friend = None
    def __del__(self):
        # __del__() 메소드를 정의하여 객체가 삭제될 때 자신이 파괴된다는 유언을 출력
        print(f'{id(self):x} is destroyed.')

a, b = Foo(), Foo()

a.friend = b  ## b를 a의 속성으로 만든다
b = None      ## b를 a.friend의 속성으로 참조하고 있기 때문에 b의 바인딩을 바꾸어도 제거 되지 않는다. 
a = None      ## a가 바인딩하던 첫번째 객체만 제거된다. a.friend 에 대한 참조를 제거하는 작업이 전혀 진행되지 않았기 때문


class Foo:
    def __init__(self):
        self.v = 1
        self.friend = None
    def __del__(self):
        self.friend = None
        print(f'{id(self):x} is destroyed.')

a, b = Foo(), Foo()
a.friend = b
b = None  # 참조가 살아있기 때문에 파괴되지 않음
a = None  # 최초 b 였던 두번째 객체에 대한 참조가 모두 제거되면서 b 객체가 제거된다. 그리고 곧이어 a 객체도 제거


a, b, c = [Foo() for _ in range(3)]
a.friend = b
b.friend = a
b = None
# a = None이 호출되는 시점에 원래 a 였던 객체의 참조수는 2에서 1로 줄어든다.
# 하지만 남은 참조를 가지고 있던 이름 b는  None을 가리키고 있고, b.friend 라는 속성 이름 자체에 대한 접근이 막혔다. 
# 따라서 a.__del__() 이 호출될 수 없기 때문에 두 객체는 메모리에 계속 남아 메모리 누수가 발생하게 된다.
a = None  

c.friend = c # 자기 자신의 속성 이름에 의해서 스스로 순환참조 생성
c = None # c.friend=None 과 같은 식으로 먼저 속성에 의한 참조를 해제하지 않는 이상 메모리 누수를 일으키는 고립된 객체가 된다.