from ursina import *
from ursina.shaders import lit_with_shadows_shader
import math
import time

app = Ursina()

# ---------------------------------------------------------
# 1. Aesthetics, Window Background & Lighting
# ---------------------------------------------------------
window.color = color.hex('#050508')

color_maze = color.hex('#777777')
color_ball = color.cyan

main_light = DirectionalLight(y=20, z=30, shadows=True, rotation=(60, -30, 45))
AmbientLight(color=color.rgba(140, 140, 150, 1))

# ---------------------------------------------------------
# 2. 3D Environment
# ---------------------------------------------------------
platform = Entity(
    model='labirinto.obj',
    scale=(0.01, 0.01, 0.01),
    color=color_maze,
    texture='white_cube',
    collider='mesh',
    double_sided=True,
    shader=lit_with_shadows_shader
)

# Hardcoded physical boundaries based on the 3D model
min_x, max_x = -0.70, 0.70
min_z, max_z = -0.70, 0.70

# ---------------------------------------------------------
# 3. Physics Variables & Entities
# ---------------------------------------------------------
start_pos = Vec3(min_x + 0.05, 0.1, max_z - 0.05)

ball = Entity(
    model='sphere', scale=0.03, color=color_ball, collider='sphere',
    position=start_pos, shader=lit_with_shadows_shader
)
ball.vel_x = 0.0
ball.vel_z = 0.0

finish_line = Entity(
    model='cube', scale=(0.08, 0.01, 0.08), color=color.yellow,
    x=max_x - 0.05, z=min_z + 0.05, y=0.04, shader=lit_with_shadows_shader
)

# ---------------------------------------------------------
# 4. SCADA DASHBOARD & SPLIT SCREEN SETUP
# ---------------------------------------------------------
camera_pivot = Entity()
camera.parent = camera_pivot
# Movemos o centro da simulação 3D para a DIREITA (X = 0.25)
base_camera_pos = Vec3(0.25, 2.8, -2.2)
camera.position = base_camera_pos
camera.look_at(platform)

camera_locked = False
last_toggle_time = 0
game_won = False
zoom_level = 1.0

# --- SIDEBAR (Left Panel) ---
sidebar = Entity(parent=camera.ui, model='quad', scale=(0.65, 1.0), color=color.hex('#0e0e12'), position=(-0.56, 0),
                 z=1)
# Cyan dividing line
Entity(parent=camera.ui, model='quad', scale=(0.005, 1.0), color=color_ball, position=(-0.235, 0), z=0)

# Main Texts
ui_text = Text(parent=camera.ui, text='MODE: MANUAL | CAM: FREE', position=(-0.85, 0.48), scale=1.3, color=color.white,
               z=-1)
pd_telemetry = Text(parent=camera.ui, text='TELEMETRY DATA', position=(-0.85, 0.42), scale=1.0, color=color.yellow,
                    z=-1)
victory_text = Text(parent=camera.ui, text='<yellow>VICTORY!\n<white>Press B to Restart', position=(0.25, 0),
                    origin=(0, 0), scale=5, enabled=False)

# ---------------------------------------------------------
# LIVE GRAPHS (Ultra High Resolution)
# ---------------------------------------------------------
# Maximized sampling points for gapless rendering
GRAPH_POINTS = 300
last_graph_time = 0

# Graph X
graph_x_bg = Entity(parent=camera.ui, model='quad', scale=(0.55, 0.20), color=color.hex('#16161a'),
                    position=(-0.56, 0.12), z=0)
Text(parent=camera.ui, text='Servo X (Yellow=Target, Cyan=Real)', position=(-0.83, 0.25), scale=1.0, color=color.white,
     z=-1)
for i in range(1, 4):
    Entity(parent=graph_x_bg, model='line', color=color.white33, scale=(1, 1), position=(0, -0.5 + (i * 0.25), -0.01))

hist_target_x = [0] * GRAPH_POINTS
hist_real_x = [0] * GRAPH_POINTS
# Thick circular dots overlapping perfectly to form a solid line
dots_t_x = [Entity(parent=graph_x_bg, model='circle', color=color.yellow, scale=(0.01, 0.02),
                   x=-0.48 + (i / GRAPH_POINTS) * 0.96, z=-0.02) for i in range(GRAPH_POINTS)]
dots_r_x = [Entity(parent=graph_x_bg, model='circle', color=color_ball, scale=(0.012, 0.024),
                   x=-0.48 + (i / GRAPH_POINTS) * 0.96, z=-0.03) for i in range(GRAPH_POINTS)]

# Graph Z
graph_z_bg = Entity(parent=camera.ui, model='quad', scale=(0.55, 0.20), color=color.hex('#16161a'),
                    position=(-0.56, -0.15), z=0)
Text(parent=camera.ui, text='Servo Z (Yellow=Target, Cyan=Real)', position=(-0.83, -0.02), scale=1.0, color=color.white,
     z=-1)
for i in range(1, 4):
    Entity(parent=graph_z_bg, model='line', color=color.white33, scale=(1, 1), position=(0, -0.5 + (i * 0.25), -0.01))

hist_target_z = [0] * GRAPH_POINTS
hist_real_z = [0] * GRAPH_POINTS
dots_t_z = [Entity(parent=graph_z_bg, model='circle', color=color.yellow, scale=(0.01, 0.02),
                   x=-0.48 + (i / GRAPH_POINTS) * 0.96, z=-0.02) for i in range(GRAPH_POINTS)]
dots_r_z = [Entity(parent=graph_z_bg, model='circle', color=color_ball, scale=(0.012, 0.024),
                   x=-0.48 + (i / GRAPH_POINTS) * 0.96, z=-0.03) for i in range(GRAPH_POINTS)]

# Minimap at the bottom of the dashboard
minimap_bg = Entity(parent=camera.ui, model='quad', scale=(0.28, 0.28), color=color.black66, position=(-0.56, -0.42),
                    z=0)
minimap_ball = Entity(parent=minimap_bg, model='circle', scale=0.06, color=color_ball, z=-0.1)
trail_dots = []
last_trail_time = 0

prev_err_x = 0.0
prev_err_z = 0.0


def reset_game():
    global game_won, trail_dots, hist_target_x, hist_real_x, hist_target_z, hist_real_z

    # Physics reset
    ball.position = start_pos
    ball.vel_x = 0.0
    ball.vel_z = 0.0
    platform.rotation_x = 0
    platform.rotation_z = 0
    game_won = False
    victory_text.enabled = False

    # Camera reset
    camera_pivot.position = Vec3(0, 0, 0)

    # UI Reset
    for dot in trail_dots:
        destroy(dot)
    trail_dots.clear()

    hist_target_x = [0] * GRAPH_POINTS
    hist_real_x = [0] * GRAPH_POINTS
    hist_target_z = [0] * GRAPH_POINTS
    hist_real_z = [0] * GRAPH_POINTS


# ---------------------------------------------------------
# 5. Main Loop (Sub-stepping Physics & High-Res Graphics)
# ---------------------------------------------------------
def update():
    global camera_locked, last_toggle_time, game_won, last_trail_time, trail_dots
    global prev_err_x, prev_err_z, last_graph_time, zoom_level
    global hist_target_x, hist_real_x, hist_target_z, hist_real_z

    if held_keys['gamepad b'] or held_keys['r']:
        reset_game()
        return

    if game_won:
        return

    current_time = time.time()

    # ---------------------------------------------------------
    # UI, CAMERA ZOOM & CAMERA PANNING
    # ---------------------------------------------------------
    if (held_keys['gamepad right stick'] or held_keys['c']) and (current_time - last_toggle_time > 0.3):
        camera_locked = not camera_locked
        last_toggle_time = current_time
        status = "LOCKED" if camera_locked else "FREE"
        color_status = "<red>" if camera_locked else "<green>"
        ui_text.text = f'MODE: MANUAL | CAM: {color_status}{status}'

    # Zoom in/out
    zoom_in = held_keys['gamepad right trigger'] + held_keys['e']
    zoom_out = held_keys['gamepad left trigger'] + held_keys['q']

    if zoom_in > 0 or zoom_out > 0:
        zoom_speed = 1.5 * time.dt
        zoom_level -= (zoom_in - zoom_out) * zoom_speed
        zoom_level = clamp(zoom_level, 0.4, 2.5)
        camera.position = base_camera_pos * zoom_level

    # Camera Panning (Using D-Pad to move along local camera axes)
    pan_x = held_keys['gamepad dpad right'] - held_keys['gamepad dpad left']
    pan_y = held_keys['gamepad dpad up'] - held_keys['gamepad dpad down']

    if abs(pan_x) > 0 or abs(pan_y) > 0:
        pan_speed = 1.5 * time.dt
        camera_pivot.position += camera.right * pan_x * pan_speed
        camera_pivot.position += camera.up * pan_y * pan_speed

    # Dynamic top-down lighting adjustment
    light_pitch = 45 + (camera_pivot.rotation_x / 80.0) * 45
    light_yaw = -30 * (1 - (camera_pivot.rotation_x / 80.0))
    main_light.rotation = (light_pitch, light_yaw, 45)

    # ---------------------------------------------------------
    # PD CONTROLLER & STRICT SERVO SATURATION
    # ---------------------------------------------------------
    joy_x = held_keys['gamepad left stick x'] + held_keys['right arrow'] - held_keys['left arrow']
    joy_y = held_keys['gamepad left stick y'] + held_keys['up arrow'] - held_keys['down arrow']

    # Target rotation mapped strictly to manual input (+/- 20 degrees)
    target_rot_z = joy_x * 20
    target_rot_x = joy_y * 20

    err_x = target_rot_x - platform.rotation_x
    err_z = target_rot_z - platform.rotation_z

    d_err_x = (err_x - prev_err_x) / time.dt
    d_err_z = (err_z - prev_err_z) / time.dt
    prev_err_x, prev_err_z = err_x, err_z

    Kp = 5.0
    Kd = 0.1

    control_x = (Kp * err_x) + (Kd * d_err_x)
    control_z = (Kp * err_z) + (Kd * d_err_z)

    # Update platform rotation and rigorously clamp to safe 90 degree total bounds (-45 to 45)
    platform.rotation_x = clamp(platform.rotation_x + control_x * time.dt, -45, 45)
    platform.rotation_z = clamp(platform.rotation_z + control_z * time.dt, -45, 45)

    pd_telemetry.text = (
        f"SX: Tgt {target_rot_x:5.1f}° | Real {platform.rotation_x:5.1f}°\n"
        f"SZ: Tgt {target_rot_z:5.1f}° | Real {platform.rotation_z:5.1f}°"
    )

    # High-Res Graph Updating (Now sampling at ultra-high frequency)
    if current_time - last_graph_time > 0.01:
        hist_target_x.pop(0)
        hist_target_x.append(target_rot_x)
        hist_real_x.pop(0)
        hist_real_x.append(platform.rotation_x)

        hist_target_z.pop(0)
        hist_target_z.append(target_rot_z)
        hist_real_z.pop(0)
        hist_real_z.append(platform.rotation_z)

        for i in range(GRAPH_POINTS):
            dots_t_x[i].y = hist_target_x[i] / 50.0
            dots_r_x[i].y = hist_real_x[i] / 50.0

            dots_t_z[i].y = hist_target_z[i] / 50.0
            dots_r_z[i].y = hist_real_z[i] / 50.0

        last_graph_time = current_time

    if not camera_locked:
        cam_rot_y = held_keys['gamepad right stick x'] * 100 * time.dt
        cam_rot_x = held_keys['gamepad right stick y'] * 50 * time.dt
        camera_pivot.rotation_y += cam_rot_y
        camera_pivot.rotation_x = clamp(camera_pivot.rotation_x - cam_rot_x, -10, 80)

    # ---------------------------------------------------------
    # SUB-STEPPING PHYSICS ENGINE
    # ---------------------------------------------------------
    g = 9.81
    acc_x = g * math.sin(math.radians(platform.rotation_z))
    acc_z = -g * math.sin(math.radians(platform.rotation_x))

    SUB_STEPS = 3
    dt_sub = time.dt / SUB_STEPS
    friction = 0.96

    for _ in range(SUB_STEPS):
        ball.vel_x += acc_x * dt_sub
        ball.vel_z += acc_z * dt_sub

        ball.vel_x *= friction ** (1 / SUB_STEPS)
        ball.vel_z *= friction ** (1 / SUB_STEPS)

        ball.vel_x = clamp(ball.vel_x, -1.5, 1.5)
        ball.vel_z = clamp(ball.vel_z, -1.5, 1.5)

        step_x = ball.vel_x * dt_sub
        step_z = ball.vel_z * dt_sub

        ray_origin = Vec3(ball.x, ball.y, ball.z)

        if abs(ball.vel_x) > 0.0001:
            dir_x = 1 if ball.vel_x > 0 else -1
            look_ahead_x = abs(step_x) + 0.025
            hit_x = raycast(ray_origin, (dir_x, 0, 0), ignore=(ball, finish_line), distance=look_ahead_x)
            if hit_x.hit:
                ball.vel_x = 0
            else:
                ball.x += step_x

        if abs(ball.vel_z) > 0.0001:
            dir_z = 1 if ball.vel_z > 0 else -1
            look_ahead_z = abs(step_z) + 0.025
            hit_z = raycast(ray_origin, (0, 0, dir_z), ignore=(ball, finish_line), distance=look_ahead_z)
            if hit_z.hit:
                ball.vel_z = 0
            else:
                ball.z += step_z

        # Shielded Floor Collision
        ray_origin_y = platform.y + 0.4
        ray_down = raycast(Vec3(ball.x, ray_origin_y, ball.z), (0, -1, 0), ignore=(ball, finish_line), distance=0.8)

        if ray_down.hit:
            if ray_down.world_normal.y > 0.5:
                ball.y = ray_down.world_point.y + 0.015

        # Absolute boundary safeguards
        ball.x = clamp(ball.x, min_x + 0.03, max_x - 0.03)
        ball.z = clamp(ball.z, min_z + 0.03, max_z - 0.03)

    # ---------------------------------------------------------
    # MINIMAP & TRAIL UPDATES
    # ---------------------------------------------------------
    minimap_ball.x = ball.x / 1.5
    minimap_ball.y = ball.z / 1.5

    if current_time - last_trail_time > 0.1:
        dot = Entity(parent=minimap_bg, model='circle', scale=0.015, color=color.rgba(0, 255, 255, 150), z=-0.05,
                     position=minimap_ball.position)
        trail_dots.append(dot)
        last_trail_time = current_time
        if len(trail_dots) > 300:
            destroy(trail_dots.pop(0))

    dist_to_finish = math.sqrt((ball.x - finish_line.x) ** 2 + (ball.z - finish_line.z) ** 2)
    if dist_to_finish < 0.08:
        game_won = True
        victory_text.enabled = True


app.run()