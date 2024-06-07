<script lang="ts">
  import CreditAgricole from "$lib/images/banques/credit-agricole.png";
  import CaisseEpargne from "$lib/images/banques/caisse-d-epargne.png";
  import SocieteGenerale from "$lib/images/banques/societe-generale.png";
  import BNP from "$lib/images/banques/bnp.png";
  import CreditMutuel from "$lib/images/banques/credit-mutuel.png";
  import LCL from "$lib/images/banques/lcl.png";
  import BanquePopulaire from "$lib/images/banques/banque-populaire.png";
  import LaBanquePostale from "$lib/images/banques/la-banque-postale.png";
  import CIC from "$lib/images/banques/cic.png";
  import CreditDuNord from "$lib/images/banques/credit-du-nord.png";
  import AXA from "$lib/images/banques/axa.png";
  import BRED from "$lib/images/banques/bred.png";
  import Fortuneo from "$lib/images/banques/fortuneo.png";
  import Boursorama from "$lib/images/banques/boursorama.png";
  import HelloBank from "$lib/images/banques/hello-bank.png";
  import Groupama from "$lib/images/banques/groupama.png";
  import HSBC from "$lib/images/banques/hsbc.png";
  import ING from "$lib/images/banques/ing.png";
  import Barclays from "$lib/images/banques/barclays.png";
  import CreditFoncier from "$lib/images/banques/credit-foncier.png";

  import StepComponent from "$lib/components/StepComponent.svelte";
  import { changeStep } from "$lib/utils.js";
  import Card from "$lib/components/Card.svelte";

  import { Banque, type Simulation } from "$lib/api/models";

  export let step: number;
  export let simulation: Partial<Simulation>;

  function updateSimulation(data: Partial<Simulation>) {
    simulation = { ...simulation, ...data };
    step = changeStep(step);
  }

  const banque_options = [
    {
      banque: Banque.CREDIT_AGRICOLE,
      text: "Crédit Agricole",
      image: CreditAgricole,
    },
    {
      banque: Banque.CAISSE_EPARGNE,
      text: "Caisse d'Épargne",
      image: CaisseEpargne,
    },
    {
      banque: Banque.SOCIETE_GENERALE,
      text: "Société Générale",
      image: SocieteGenerale,
    },
    {
      banque: Banque.BNP,
      text: "BNP",
      image: BNP,
    },
    {
      banque: Banque.CREDIT_MUTUEL,
      text: "Crédit Mutuel",
      image: CreditMutuel,
    },
    { banque: Banque.LCL, text: "LCL", image: LCL },
    {
      banque: Banque.BANQUE_POPULAIRE,
      text: "Banque Populaire",
      image: BanquePopulaire,
    },
    {
      banque: Banque.LA_BANQUE_POSTALE,
      text: "La Banque Postale",
      image: LaBanquePostale,
    },
    { banque: Banque.CIC, text: "CIC", image: CIC },
    {
      banque: Banque.CREDIT_DU_NORD,
      text: "Crédit du Nord",
      image: CreditDuNord,
    },
    { banque: Banque.AXA, text: "AXA", image: AXA },
    { banque: Banque.BRED, text: "BRED", image: BRED },
    { banque: Banque.FORTUNEO, text: "Fortuneo", image: Fortuneo },
    { banque: Banque.BOURSORAMA, text: "Boursorama", image: Boursorama },
    { banque: Banque.HELLOBANK, text: "Hellobank", image: HelloBank },
    { banque: Banque.GROUPAMA, text: "Groupama", image: Groupama },
    { banque: Banque.HSBC, text: "HSBC", image: HSBC },
    { banque: Banque.ING, text: "ING", image: ING },
    { banque: Banque.BARCLAYS, text: "Barclays", image: Barclays },
    {
      banque: Banque.CREDIT_FONCIER,
      text: "Crédit Foncier",
      image: CreditFoncier,
    },
  ];
</script>

<StepComponent bind:step>
  <div slot="title">Vous avez contracté ce prêt aurpès de :</div>
  <div slot="body">
    <div
      class="grid lg:grid-cols-4 md:grid-cols-3 max-md:grid-cols-2 gap-4 text-center"
    >
      {#each banque_options as banque}
        <Card
          image={banque.image}
          alt=""
          on:click={() => updateSimulation({ banque: banque.banque })}
        >
          <div slot="description">{banque.text}</div>
        </Card>
      {/each}
    </div>
    <div class="grid grid-rows-1 mt-4 justify-center">
      <Card on:click={() => updateSimulation({ banque: Banque.AUTRE })} alt="">
        <slot slot="description">Une autre banque</slot>
      </Card>
    </div>
  </div>
</StepComponent>
