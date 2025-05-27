import time


def mettre_a_jour_temps(previous_time, elapsed_time):
    
    now = time.time()
    dt = now - previous_time
    return now, elapsed_time + dt, dt



def mise_a_jour_simulation(env, robot, simulation, dt, elapsed_time):

    env.update(robot, dt)
    simulation.mise_a_jour(elapsed_time)
    simulation.app.step()
