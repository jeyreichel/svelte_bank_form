import { front_url, backend_url } from "$lib/config";
import type {
  Simulation,
  SimulationResponse,
  Adhesion,
  AdhesionResponse,
} from "./models";

async function get(route: string): Promise<Response> {
  return await fetch(backend_url + route, {
    method: "GET",
    headers: {
      "Access-Control-Allow-Origin": front_url,
    },
  });
}

async function post(route: string, body: string): Promise<Response> {
  return await fetch(backend_url + route, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Access-Control-Allow-Origin": front_url,
    },
    body: body,
  });
}

function replace_dates(key:string, value:string){
  if (["debut_contrat", "date_naissance", "premiere_mensualite"].includes(key)){
    return value.split('T')[0]
  }
  return value
}

export async function post_simulation(
  simulation: Simulation,
): Promise<SimulationResponse> {
  simulation.origin = "omeros"
  simulation.debut_contrat = new Date(Date.now())
  simulation.debut_contrat.setDate(simulation.debut_contrat.getDate() + 30)
  let res = await post("/simulation", JSON.stringify(simulation, replace_dates));
  return res.json();
}

export async function get_simulation(
  simulation_id: string,
): Promise<SimulationResponse> {
  let res = await get(`/simulation/${simulation_id}`);
  return res.json();
}

export async function post_adhesion(
  adhesion: Adhesion,
): Promise<AdhesionResponse> {
  let res = await post("/adhesion", JSON.stringify(adhesion));
  return res.json();
}
