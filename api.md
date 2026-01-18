# Wearable Robot API 문서

## 개요

Upperlimb_1DOF는 상지 외골격 로봇을 제어하기 위한 싱글톤 API 클래스입니다.

---

## 사용 예제

### setup()
```python
from wearable_robot_api import Upperlimb_1DOF

robot = Upperlimb_1DOF(node)

def setup():
    # 초기화 (반복 횟수, 주파수 설정)
    robot.init(rep_count=20, freq=60)
```

### loop()
```python
# 제어 루프 내에서 API 사용 예제
def loop():
    # 센서 값 읽기
    current_angle = robot.get_target_angle()
    current_velocity = robot.get_velocity()
    current_force = robot.get_force()
    current_position = robot.get_position()

    # 속도 명령 설정
    robot.set_velocity(desired_velocity)

    # 제어 파라미터 읽기
    damping = robot.get_damping()
    spring = robot.get_spring()
    moment = robot.get_moment()
```

---

## API 레퍼런스

### Upperlimb_1DOF class
상지 외골격 로봇 제어를 위한 싱글톤 클래스입니다.

**특징:**
- 싱글톤 패턴으로 구현되어 프로그램 내에서 하나의 인스턴스만 존재
- ROS2 노드와 연동하여 동작

---

### `Upperlimb_1DOF.__init__(node=None)`
클래스 생성자입니다.

**매개변수:**
- `node` (optional): ROS2 노드 객체

**초기화 속성:**
- `rep_count`: 반복 횟수 (기본값: 0)
- `freq`: 주파수 (기본값: 60)
- `velocity_cmd`: 속도 명령 (기본값: 0.0)
- `DELTA_TIME`: 시간 간격 (기본값: 0.02초)

**예제:**
```python
robot = Upperlimb_1DOF(node)
```

---

### `init(rep_count=20, freq=60)`
상지 제어 파라미터를 초기화합니다.

**매개변수:**
- `rep_count` (int): 목표 반복 횟수 (기본값: 20)
- `freq` (int): 제어 주파수 (기본값: 60Hz)

**예제:**
```python
robot.init(rep_count=30, freq=50)
```

---

### `get_target_angle()`
현재 목표 각도를 반환합니다.

**반환값:**
- `float`: 목표 각도 (degrees)

**예제:**
```python
angle = robot.get_target_angle()
print(f"Target angle: {angle}°")
```

---

### `get_velocity()`
현재 센서 속도를 반환합니다.

**반환값:**
- `float`: 현재 속도

**예제:**
```python
velocity = robot.get_velocity()
```

---

### `set_velocity(velocity)`
속도 명령을 설정합니다.

**매개변수:**
- `velocity` (float): 설정할 속도 값

**예제:**
```python
robot.set_velocity(1.5)
```

---

### `get_velocity_cmd()`
현재 설정된 속도 명령을 반환합니다.

**반환값:**
- `float`: 속도 명령 값

**예제:**
```python
cmd = robot.get_velocity_cmd()
```

---

### `get_previous_velocity()`
이전 센서 속도를 반환합니다.

**반환값:**
- `float`: 이전 속도 값

**예제:**
```python
prev_vel = robot.get_previous_velocity()
```

---

### `set_previous_velocity(velocity)`
이전 센서 속도를 설정합니다.

**매개변수:**
- `velocity` (float): 설정할 이전 속도 값

**예제:**
```python
robot.set_previous_velocity(1.0)
```

---

### `get_force()`
현재 센서 힘을 반환합니다.

**반환값:**
- `float`: 현재 힘 값

**예제:**
```python
force = robot.get_force()
```

---

### `get_position()`
현재 센서 위치를 반환합니다.

**반환값:**
- `float`: 현재 위치 값

**예제:**
```python
position = robot.get_position()
```

---

### `get_moment()`
관성 모멘트 계수를 반환합니다.

**반환값:**
- `float`: 관성 모멘트 (기본값: 0.0)

**예제:**
```python
moment = robot.get_moment()
```

---

### `get_spring()`
스프링 계수를 반환합니다.

**반환값:**
- `float`: 스프링 계수 (기본값: 0.0)

**예제:**
```python
spring = robot.get_spring()
```

---

### `get_damping()`
댐핑 계수를 반환합니다.

**반환값:**
- `float`: 댐핑 계수 (기본값: 100.0)

**예제:**
```python
damping = robot.get_damping()
```

---

### `rep_count`
목표 반복 횟수를 저장하는 속성입니다.

**타입:** `int`

**예제:**
```python
total_reps = robot.rep_count
```

---

### `freq`
제어 주파수를 저장하는 속성입니다.

**타입:** `int` (기본값: 60Hz)

**예제:**
```python
control_freq = robot.freq
```

---

## 추가 속성

### `target_th` (property)
목표 각도를 라디안 단위로 반환하는 읽기 전용 속성입니다.

**반환값:**
- `float`: 목표 각도 (radians)

**예제:**
```python
angle_rad = robot.target_th
```

---

## 주의사항
1. 이 클래스는 싱글톤 패턴으로 구현되어 있어 여러 번 생성해도 같은 인스턴스를 반환합니다.
2. ROS2 노드가 없으면 센서 값들은 0.0을 반환합니다.
3. `DELTA_TIME`은 노드에서 제공되는 값을 사용하며, 없을 경우 0.02초를 기본값으로 사용합니다.
