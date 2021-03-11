## How-to Algo 7. Teamwork

 
## Codingame

**[Ссылка на контекст](https://www.codingame.com/multiplayer/bot-programming/fantastic-bits)**


## Лайфкодинги

### 02/22 

[https://youtu.be/YNaz9K65Z8U](https://youtu.be/YNaz9K65Z8U)

### 03/01

[https://youtu.be/21i3UjcWGSQ](https://youtu.be/21i3UjcWGSQ)

Обсуждаем написания бота:

- [03:15](https://www.youtube.com/watch?v=21i3UjcWGSQ&t=195s) - чуть-чуть про вектора;
- [17:00](https://youtu.be/21i3UjcWGSQ&t=1020s) - читаем "чужой" код;
- [30:00](https://youtu.be/21i3UjcWGSQ&t=1800s) - запускаем простую стратегию в codingame;
- [49:00](https://youtu.be/21i3UjcWGSQ&t=2940s) - чуть-чуть про тестирование (пока нечего тестировать);
- [54:00](https://youtu.be/21i3UjcWGSQ&t=3240s) - ищем ближайший snaffle;

### 03/11 

Материалы:

- [Стратегии для принятия решений](https://www.codingame.com/blog/lazy-keep-simple/);
- [Идеи для игры](https://www.codingame.com/forum/t/fantastic-bits-feedback-strategy/2360/38);
- [Multiagent](https://www.cs.utexas.edu/~larg/ijcai17_tutorial/multiagent_learning.pdf);
- [Ad Hoc Teamwork](https://arxiv.org/pdf/1809.07880v1.pdf);

## Примеры (Python)

### Entity


```python

class Entity:
    """Описание класса игрока"""

    def __init__(self, entity_id, entity_type, x, y, speed_x, speed_y, state, radius=100.0, max_speed=150.0, mass=1.0, friction=1.0):
        self.entity_id = int(entity_id)
        self.entity_type = entity_type
        self.position = Vec2(int(x), int(y))
        self.velocity = Vec2(int(speed_x), int(speed_y))
        self.state = int(state)
        self.mass = mass
        self.radius = radius
        self.max_speed = max_speed
        self.friction = friction

        self.avoidance = Vec2.zero()
        self.steer     = Vec2.zero()
        self.desired_velocity = self.velocity

        self.thrust    = 150


```


### Чтение из консоли


```python
entity_id, entity_type, x, y, vx, vy, state = input().split()

wizard = Entity(entity_id, entity_type, x, y, vx, vy, state, 400, 300, 1.0, 0.75)
```
