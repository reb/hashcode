use pyo3::prelude::*;
use pyo3::wrap_pyfunction;
use std::collections::HashMap;

struct Simulation {
    street_lengths: HashMap<String, i32>,
    street_ends: HashMap<String, usize>,
    bonus: i32,
    duration: i32,
    paths: Vec<Vec<String>>,
    light_schedule_streets: Vec<Vec<(String, f64)>>,
    light_schedule_total_cycles: Vec<f64>,
    t: i32,
    arriving_at: HashMap<i32, Vec<usize>>,
    waiting_at_intersection: Vec<HashMap<String, Vec<usize>>>,
    score: i32,
}

impl Simulation {
    fn new(
        street_lengths: HashMap<String, i32>,
        street_ends: HashMap<String, usize>,
        bonus: i32,
        duration: i32,
        paths: Vec<Vec<String>>,
        light_schedule_streets: Vec<Vec<(String, f64)>>,
        light_schedule_total_cycles: Vec<f64>,
    ) -> Simulation {
        let waiting_at_intersection = vec![HashMap::new(); light_schedule_streets.len()];
        let mut arriving_at = HashMap::new();
        arriving_at.insert(0, (0..paths.len()).collect());

        Simulation {
            street_lengths,
            street_ends,
            bonus,
            duration,
            paths,
            light_schedule_streets,
            light_schedule_total_cycles,
            t: 0,
            arriving_at,
            waiting_at_intersection,
            score: 0,
        }
    }

    fn do_tick(mut self) -> Simulation {
        // println!("Starting tick {}", self.t);
        // arrive vehicles at intersection at time t
        if let Some(vehicles_arriving) = self.arriving_at.get(&self.t) {
            for &vehicle_arriving in vehicles_arriving.iter() {
                if self.paths[vehicle_arriving].len() == 1 {
                    self.score += self.bonus + (self.duration - self.t);
                    // println!("Vehicle completed path!");
                    continue;
                }
                let vehicle_path = self.paths.get_mut(vehicle_arriving).unwrap();
                let street_name = vehicle_path.remove(0);
                // println!(
                //     "Vehicle {} is arriving at the end of {} at t={}",
                //     vehicle_arriving, street_name, self.t
                // );
                let &intersection = self.street_ends.get(&street_name).unwrap();
                self.waiting_at_intersection[intersection]
                    .entry(street_name)
                    .or_insert(Vec::new())
                    .push(vehicle_arriving)
            }
        }
        // cross vehicles that are first at green lights
        for (i_id, streets) in self.waiting_at_intersection.iter_mut().enumerate() {
            for (street_name, vehicles) in streets.iter_mut() {
                if !vehicles.is_empty() {
                    // println!(
                    //     "Vehicles {:?} waiting at intersection {} for street {}",
                    //     vehicles, i_id, street_name
                    // );
                }
                if !vehicles.is_empty()
                    && green_light(i_id, street_name, self.t, &self.light_schedule_streets, &self.light_schedule_total_cycles)
                {
                    let v_id = vehicles.remove(0);
                    // println!("Crossing vehicle {}", v_id);
                    let street_name = &self.paths[v_id][0];
                    let t_arrive = self.street_lengths.get(street_name).unwrap() + self.t;
                    self.arriving_at
                        .entry(t_arrive)
                        .or_insert(Vec::new())
                        .push(v_id);
                }
            }
        }
        self.t += 1;
        return self;
    }
}

fn green_light(
    intersection_id: usize,
    street_name: &String,
    t: i32,
    light_schedule_streets: &Vec<Vec<(String, f64)>>,
    light_schedule_total_cycles: &Vec<f64>,
) -> bool {
    let mut cycle_t = t as f64 % light_schedule_total_cycles[intersection_id];

    for (street, duration) in light_schedule_streets[intersection_id].iter() {
        if street == street_name && cycle_t < *duration {
            return true;
        }
        cycle_t -= duration;
        if cycle_t < 0.0 {
            return false;
        }
    }

    return false;
}

#[pyfunction]
fn score(
    street_lengths: HashMap<String, i32>,
    street_ends: HashMap<String, usize>,
    bonus: i32,
    duration: i32,
    paths: Vec<Vec<String>>,
    light_schedule_streets: Vec<Vec<(String, f64)>>,
    light_schedule_total_cycles: Vec<f64>,
) -> PyResult<i32> {
    let mut simulation = Simulation::new(
        street_lengths,
        street_ends,
        bonus,
        duration,
        paths,
        light_schedule_streets,
        light_schedule_total_cycles,
    );
    while simulation.t <= duration {
        simulation = simulation.do_tick()
    }
    Ok(simulation.score)
}

#[pymodule]
fn fast(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(score, m)?)?;

    Ok(())
}
