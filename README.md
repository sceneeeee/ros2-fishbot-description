# ros2-fishbot-description

一个基于 ROS 2 的 FishBot 机器人描述学习项目，围绕 **URDF / Xacro 建模、模块化机器人结构组织、传感器与执行器拆分、RViz 显示**，以及 **Gazebo 仿真准备** 展开。

这个仓库既保留了最基础的单文件机器人描述练习，也继续发展出了一个更接近实际项目组织方式的模块化 FishBot 模型，适合作为 ROS 2 机器人描述方向的阶段性学习项目。

---

## 项目简介

这个项目记录了我学习 ROS 2 机器人描述建模过程中的一个阶段性成果，主要包含两条学习主线：

1. **从简单 URDF 入门**
   - 通过 `first_robot.urdf` 学习基础语法
   - 理解 link、joint、惯性、可视化等基本概念
   - 过渡到 `first_robot.xacro`，熟悉参数化与宏的写法

2. **向模块化 FishBot 结构演进**
   - 使用 Xacro 对机器人进行模块拆分
   - 将底盘、惯性、传感器、执行器、Gazebo 插件分别组织
   - 为后续仿真、控制、导航等内容打基础

---

## 当前项目包含的内容

### 1. 基础机器人描述练习
项目保留了最基础的单文件建模内容：

- `urdf/first_robot.urdf`
- `urdf/first_robot.xacro`

适合用来练习：

- URDF 基本结构
- link / joint 的组织方式
- 材质、几何体和惯性参数
- 从 URDF 过渡到 Xacro 的基本思路

### 2. 模块化 FishBot 描述
FishBot 的机器人描述位于：

- `urdf/fishbot/fishbot.urdf.xacro`

该文件作为整机装配入口，统一引用并组合多个子模块，包括：

- 机器人本体
- 传感器模块
- 执行器模块
- Gazebo 插件模块

这种组织方式更接近真实项目中的机器人描述维护方式，后续扩展也更方便。

### 3. 传感器模块
当前仓库中已经包含常见传感器的 Xacro 模块：

- `sensor/camera.urdf.xacro`
- `sensor/imu.urdf.xacro`
- `sensor/laser.urdf.xacro`

这些模块用于练习：

- 传感器 link / joint 挂载
- 传感器安装位姿设置
- 将多个传感器组合到同一个机器人模型中
- 为后续可视化与仿真输出打基础

### 4. 执行器模块
当前 FishBot 还包含底盘执行器相关模块：

- `actuator/wheel.urdf.xacro`
- `actuator/caster.urdf.xacro`

这部分使模型从“静态展示”进一步走向“可运动底盘”的组织方式。

### 5. Gazebo 插件准备
项目中已经加入 Gazebo 相关插件配置：

- `plugins/gazebo_control_plugin.xacro`
- `plugins/gazebo_sensor_plugin.xacro`

这部分说明该项目已经开始从纯描述建模，过渡到仿真方向，包括：

- 差速底盘控制插件
- 传感器仿真插件
- 为后续 Gazebo 场景测试做准备

### 6. RViz 显示与 Launch 启动
项目提供了显示机器人模型的 launch 文件与 RViz 配置：

- `launch/display_robot.launch.py`
- `config/display_robot_model.rviz`

可以用于快速加载模型并在 RViz 中查看机器人结构、TF 和模型效果。

### 7. 仿真场景资源
仓库还包含 world 相关资源，例如：

- `world/custom_room.world`
- `world/room/`

这部分表明项目已经不仅停留在模型显示层面，而是开始为仿真环境搭建做准备。

---

## 项目结构

```text
ros2-fishbot-description/
├── README.md
├── .gitignore
└── src/
    └── fishbot_description/
        ├── CMakeLists.txt
        ├── package.xml
        ├── LICENSE
        ├── config/
        │   └── display_robot_model.rviz
        ├── launch/
        │   └── display_robot.launch.py
        ├── urdf/
        │   ├── first_robot.gv
        │   ├── first_robot.pdf
        │   ├── first_robot.urdf
        │   ├── first_robot.xacro
        │   └── fishbot/
        │       ├── base.urdf.xacro
        │       ├── common_inertial.xacro
        │       ├── fishbot.urdf.xacro
        │       ├── actuator/
        │       │   ├── caster.urdf.xacro
        │       │   └── wheel.urdf.xacro
        │       ├── sensor/
        │       │   ├── camera.urdf.xacro
        │       │   ├── imu.urdf.xacro
        │       │   └── laser.urdf.xacro
        │       └── plugins/
        │           ├── gazebo_control_plugin.xacro
        │           └── gazebo_sensor_plugin.xacro
        └── world/
            ├── custom_room.world
            └── room/
````

---

## 环境建议

建议使用以下环境进行学习与测试：

* Ubuntu 22.04 / 24.04
* ROS 2 Humble / Jazzy
* colcon
* xacro
* rviz2
* robot_state_publisher
* joint_state_publisher

如果你要继续使用 Gazebo 相关功能，还需要对应版本的 Gazebo / gazebo_ros 环境。

---

## 构建方法

在工作区根目录执行：

```bash
colcon build
```

编译完成后加载环境：

```bash
source install/setup.bash
```

---

## 运行方法

### 1. 默认方式：加载基础机器人模型

这个 launch 文件默认会加载 `first_robot.urdf`：

```bash
ros2 launch fishbot_description display_robot.launch.py
```

### 2. 指定模型：加载模块化 FishBot

由于 launch 文件提供了 `model` 参数，所以也可以手动指定 FishBot 的 Xacro 文件。

在工作区根目录下可以这样运行：

```bash
ros2 launch fishbot_description display_robot.launch.py \
model:=$PWD/src/fishbot_description/urdf/fishbot/fishbot.urdf.xacro
```

这样就可以直接查看模块化 FishBot 模型。

---

## 这个项目适合练习什么

这个项目适合用于练习和整理以下内容：

* ROS 2 机器人描述功能包结构
* URDF 基础建模
* Xacro 宏与参数化
* 机器人结构模块化拆分
* 传感器挂载与组合
* 执行器建模
* RViz 模型显示
* Gazebo 插件组织方式
* 为后续仿真、控制、导航做准备

---

## 项目特点

我觉得这个项目的价值主要不在于“做成一个完整产品”，而在于它完整记录了一个学习路径：

* 从单文件 URDF 到 Xacro
* 从简单模型到模块化模型
* 从纯显示到仿真准备
* 从机器人本体到传感器、执行器和场景资源的逐步扩展

对正在学习 ROS 2 robot description 的同学来说，这样的项目非常适合用来作为自己的阶段性仓库。

---

## 后续可继续完善的方向

后续还可以继续往这些方向扩展：

* 增加专门的 Gazebo 启动文件
* 完善 FishBot 在 Gazebo 中的完整加载流程
* 增加模型运行截图和仿真截图
* 增加 TF 树说明
* 完善 package 元信息
* 增加更完整的底盘控制与导航实验
* 补充传感器话题和插件说明
* 增加更规范的版本记录与 release 说明

---

## License

本项目使用 Apache-2.0 License，详见仓库中的 `LICENSE` 文件。
