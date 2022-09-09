translate([0, 0, 290])
rotate([0, 0, 0])
import("Auxivo_EduExo_Maker/EduExo STL files/Upper_Arm_Cuff_Large_180.stl", convexity=3);

translate([5, 5, 200])
rotate([0, 0, 0])
import("Auxivo_EduExo_Maker/EduExo STL files/Upper_Arm_Segment.stl", convexity=3);

translate([0, 0, 200])
rotate([0, 0, 0])
import("Auxivo_EduExo_Maker/EduExo STL files/Upper_Arm_Cuff_Large_180.stl", convexity=3);

translate([0, 25, 175])
rotate([180, 270, 0])
import("Auxivo_EduExo_Maker/EduExo STL files/MotorAdapter.stl", convexity=3);

translate([15, 0, 150])
rotate([0, -90, 0])
import("Auxivo_EduExo_Maker/EduExo STL files/Interface_Motor_Sensor.stl", convexity=3);


translate([15, 0, 50])
rotate([0, -90, 0])
import("Auxivo_EduExo_Maker/EduExo STL files/Lower_Arm_Segment.stl", convexity=3);
