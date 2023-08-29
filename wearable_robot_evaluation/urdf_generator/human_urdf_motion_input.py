from urdf_parser_py.urdf import *

class Human:
    def __init__(self, height, weight, arm_length, leg_length, torso_length, head_circumference):
        self.height = height  # 키 (m)
        self.weight = weight  # 체중 (kg)
        self.arm_length = arm_length  # 팔 길이 (m)
        self.leg_length = leg_length  # 다리 길이 (m)
        self.torso_length = torso_length  # 몸통 길이 (m)
        self.head_circumference = head_circumference  # 머리 둘레 (m)

    def __str__(self):
        return f"""Human Dimensions:
        Height: {self.height} cm
        Weight: {self.weight} kg
        Arm Length: {self.arm_length} cm
        Leg Length: {self.leg_length} cm
        Torso Length: {self.torso_length} cm
        Head Circumference: {self.head_circumference} cm"""

def create_human_urdf(human):
    robot = URDF.from_xml_file('human_45dof.urdf')
    elbow_length = 0.30

    for link in robot.links:
        print(link.name)
        if 'elbow' in link.name:
            link.visual.origin.position = [0.0, -elbow_length, 0.0]
            link.collision.origin.position = [0.0, -elbow_length, 0.0]
        if link.visual and link.visual.origin:
            print(link.visual.origin.position)
        if link.collision:
            print(link.collision.origin.position)

    return robot.to_xml_string()

if __name__ == "__main__":
    print("휴먼 트윈의 상지운동 최대 근력 및 가동 범위 입력")
    muscle_strength = float(input("Enter the maximum muscle strength in N/m: "))
    min_motion_range = float(input("Enter the min degree of motion input in degree: "))
    max_motion_range = float(input("Enter the max degree of motion input in degree: "))
    print("휴먼 트윈의 상지운동 최대 근력 및 가동 범위 입력 완료")
    print("-----------------------------")
    input("\nPress enter to continue...\n")

    person = Human(175, 70, 65, 90, 50, 56)
    #person = Human(height, weight, arm_length, leg_length, torso_length, head_circumference)
    human_urdf = create_human_urdf(person)
    print(human_urdf)

    print("휴먼 트윈 URDF의 상지운동 최대 근력 및 가동 범위 수정 완료")
