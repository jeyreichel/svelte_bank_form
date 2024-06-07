<script lang="ts">
  import Generali from "$lib/images/assurances/GENERALI.png";
  import CNP from "$lib/images/assurances/CNP.webp";
  import AXA from "$lib/images/assurances/AXA.png";
  import MNCAP from "$lib/images/assurances/MNCAP.png";
  import SwissLife from "$lib/images/assurances/swisslife.jpg";
  import MAIF from "$lib/images/assurances/MAIF.png";
  import MALAKOFF from "$lib/images/assurances/Malakoff_Humanis.jpeg";
  import HARMONIE from "$lib/images/assurances/Harmonie_Mutuelle.jpg";
  import GROUPAMA from "$lib/images/assurances/groupama.png";
  import Suravenir from "$lib/images/assurances/suravenir.png";

  import { get_simulation, post_adhesion, post_simulation } from "$lib/api/api";
  import type {
    Adhesion,
    Simulation,
    SimulationResponse,
  } from "$lib/api/models";
  import { onMount } from "svelte";
  import Loading from "$lib/components/Loading.svelte";
  import StepComponent from "$lib/components/StepComponent.svelte";
  import CardResult from "$lib/components/CardResult.svelte";
  import Button from "$lib/components/Button.svelte";
  import { setTokenWithExpiry } from "$lib/utils";
  import { goto } from "$app/navigation";
  import { Notifications, acts } from "@tadashi/svelte-notification";

  export let id_simulation: string | undefined = undefined,
    simulation: Simulation | undefined = undefined,
    step: number = 1;

  let loading: boolean,
    response: SimulationResponse,
    subscription_success: boolean = false,
    error: unknown;
  let duree: number, montant: number, average_price: number;

  let images = {
    GENERALI: Generali,
    CNP: CNP,
    AXA: AXA,
    MNCAP: MNCAP,
    "SWISS LIFE": SwissLife,
    "MAIF VIE": MAIF,
    "MALAKOFF HUMANIS": MALAKOFF,
    "HARMONIE MUTUELLE": HARMONIE,
    "GROUPAMA GAN VIE": GROUPAMA,
    SURAVENIR: Suravenir,
  };

  function new_simulation() {
    step = 1;
    simulation = undefined;
    setTokenWithExpiry("step", step.toString());
    // acts.add({ mode: "success", message: "session expired", lifetime: 4 });
    goto("/");
  }

  async function subscribe(id_simulation: string, id_result: string) {
    loading = true;
    let adhesion: Adhesion = { id_simulation, id_result };
    try {
      await post_adhesion(adhesion);
      // TODO: Redirect to success page
      subscription_success = true;
    } catch (e) {
      error = e;
    }
    loading = false;
  }

  function calculateAge(birthday: Date) {
    var ageDifMs = Date.now() - birthday.valueOf();
    var ageDate = new Date(ageDifMs); // from epoch
    return Math.abs(ageDate.getUTCFullYear() - 1970);
  }

  onMount(async () => {
    loading = true;
    if (!id_simulation && !simulation) {
      error = "aucun identifiant fourni";
      loading = false;
      return;
    }
    try {
      let simulationwithresponse;
      if (id_simulation) {
        simulationwithresponse = await get_simulation(id_simulation);
        simulation = simulationwithresponse.simulation;
        response = simulationwithresponse.response;
      } else if (simulation) {
        response = await post_simulation(simulation);
      }
      response.formules.sort((a, b) => {
        return a.cout_total_sans_frais - b.cout_total_sans_frais;
      });
      duree = simulation!.prets.reduce((r, p) => Math.max(p.duree, r), 0);
      montant = simulation!.prets.reduce((r, p) => p.montant + r, 0);
      const mean_rate =
        calculateAge(simulation!.assures[0].date_naissance) < 30
          ? 0.0026
          : 0.004;
      average_price = (duree / 12) * montant * mean_rate;
    } catch (e) {
      error = e;
    }
    loading = false;
    if (error) {
      acts.add({ mode: "danger", message: error, lifetime: 4 });
    } else if (response) {
      if ((response.formules = [])) {
        acts.add({
          mode: "warning",
          message: `réponse vide`,
          lifetime: 4,
        });
      } else {
        acts.add({
          mode: "success",
          message: `Non propositions trouvées`,
          lifetime: 4,
        });
      }
    }
  });
</script>

{#if loading}
  <Loading />
{:else if subscription_success}
  <div class="text-center">
    <div class="text-green-600 mb-6">
      Souscription enregistrée. Vous allez bientôt être contacté par un
      conseiller.
    </div>
  </div>
{:else if error}
  <div class="text-center">
    <Button on:click={new_simulation}>Refaire une simulation</Button>
  </div>
{:else if response}
  <StepComponent flying={false} overflow_y={false}>
    <div slot="up">
      <div class="flex justify-center mb-10 mt-10">
        <div class="col-start-5 col-end-7 text-right">
          <Button on:click={new_simulation}>Refaire une simulation</Button>
        </div>
      </div>
    </div>

    <div slot="body">
      <div class="text-center">
        {#each response.formules as result}
          <CardResult
            flying={true}
            alt={result.compagnie}
            image={images[result.compagnie]}
            name={result.nom_formule}
          >
            <div slot="description">
              <div class="grid lg:grid-cols-6">
                <div class="md:col-span-2 max-sm:col-span-3">
                  <span class="font-bold text-4xl"
                    >{parseFloat(
                      (result.cout_total_sans_frais / duree).toFixed(2)
                    )}
                    €
                  </span><br />
                  /mois
                </div>
                <div class="md:col-span-2 max-sm:col-span-3">
                  <span
                    class="font-bold text-4xl md:col-span-2 max-sm:col-span-3"
                    >{parseFloat(
                      (
                        (100 * result.cout_total_sans_frais) /
                        (montant * (duree / 12))
                      ).toFixed(2)
                    )}
                    %
                  </span><br />
                  Taux moyen annuel
                </div>
                <Button
                  class_name="md:col-span-2 max-sm:col-span-4 max-sm:col-start-2 max-sm:justify-center max-sm:mt-4"
                  on:click={() =>
                    subscribe(response.id_simulation, result.id_formule)}
                  >Souscrire
                </Button>
              </div>
              <div class="mt-10 text-center self-end">
                <span class="text-emerald-500">
                  {parseFloat(
                    Math.max(
                      average_price - result.cout_total_sans_frais,
                      0
                    ).toFixed(0)
                  )}
                  €
                </span>
                <span class="italic"
                  >d'économies par rapport à une banque classique</span
                >
              </div>
            </div>
          </CardResult>
        {/each}
      </div>
    </div>
  </StepComponent>
{/if}
<Notifications />
