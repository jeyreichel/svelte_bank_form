export enum Genre {
  FEMME = "F",
  HOMME = "H",
  NON_SPECIFIE = "non_specifie",
}

export enum Profession {
  AGRICULTEUR = "agriculteur",
  ARTISAN = "artisan",
  AU_FOYER = "au_foyer",
  COMMERCANT = "commercant",
  CHEF_ENTREPRISE = "chef_entreprise",
  EMPLOYE_BUREAU = "employe_bureau",
  ENSEIGNANT = "enseignant",
  ETUDIANT = "etudiant",
  FONCTIONNAIRE = "fonctionnaire",
  FORAIN = "forain",
  INTERMITTENT = "intermittent",
  MEDECIN_SPECIALISTE = "medecin_specialiste",
  PARAMEDICAL_LIBERAL = "paramedical_liberal",
  PROFESSION_LIBERALE = "profession_liberale",
  RECHERCHE_EMPLOI = "recherche_emploi",
  RETRAITE = "retraite",
  SALARIE_CADRE = "salarie_cadre",
  SALARIE_NON_CADRE = "salarie_non_cadre",
  SANS_ACTIVITE = "sans_activite",
  VETERINAIRE = "veterinaire",
  VRP = "vrp",
}

export enum TypePret {
  AMORTISSABLE = "pret_classique",
  IN_FINE = "in_fine",
  PRET_RELAIS = "pret_relais",
  PRET_TAUX_ZERO = "pret_taux_zero",
}

export interface Pret {
  montant: number;
  type_pret: TypePret;
  taux: number;
  taux_variable: boolean;
  duree: number;
  differe: number;
  premiere_mensualite: Date;
}

export enum DeplacementsPro {
  AUCUN = "aucun",
  MOINS_20000 = "moins_20000",
  PLUS_20000 = "plus_20000",
}

export enum TravauxManuels {
  AUCUN = "aucun",
  LEGERS = "legers",
  IMPORTANTS = "importants",
}

export interface Assure {
  genre: Genre;
  date_naissance: Date;
  profession: Profession;
  deplacements_pro: DeplacementsPro;
  travaux_manuels: TravauxManuels;
  fumeur: boolean;
  quotite: number;
  nom: string;
  prenom: string;
  adresse: string;
  code_postal: string;
  ville: string;
  telephone: string;
  email: string;
}

export enum Banque {
  CREDIT_AGRICOLE = "credit_agricole",
  CAISSE_EPARGNE = "caisse_epargne",
  SOCIETE_GENERALE = "societe_generale",
  BNP = "bnp",
  CREDIT_MUTUEL = "credit_mutuel",
  LCL = "lcl",
  BANQUE_POPULAIRE = "banque_populaire",
  LA_BANQUE_POSTALE = "la_banque_postale",
  CIC = "cic",
  CREDIT_DU_NORD = "credit_du_nord",
  AXA = "axa",
  BRED = "bred",
  FORTUNEO = "fortuneo",
  BOURSORAMA = "boursorama",
  HELLOBANK = "hellobank",
  GROUPAMA = "groupama",
  HSBC = "hsbc",
  ING = "ing",
  BARCLAYS = "barclays",
  CREDIT_FONCIER = "credit_foncier",
  AUTRE = "autre",
}

export enum ObjetPret {
  RESIDENCE_PRINCIPALE = "residence_principale",
  RESIDENCE_SECONDAIRE = "residence_secondaire",
  INVESTISSEMENT_LOCATIF = "investissement_locatif",
  AUTRE = "autre",
}

export enum ObjetDemande {
  NOUVEAU_PRET = "nouveau_pret",
  CHANGEMENT_ASSURANCE = "changement_assurance",
  RENEGOCIATION = "renegociation",
}

enum Garantie {
  DC_PTIA = "DC_PTIA",
  DC_PTIA_IPT_ITT = "DC_PTIA_IPT_ITT",
  DC_PTIA_IPT_ITT_MNO = "DC_PTIA_IPT_ITT_MNO",
  DC_PTIA_IPT_ITT_IPP = "DC_PTIA_IPT_ITT_IPP",
  DC_PTIA_IPT_ITT_IPP_MNO = "DC_PTIA_IPT_ITT_IPP_MNO",
}

export interface Simulation {
  origin: string;
  objet_pret: ObjetPret;
  objet_demande: ObjetDemande;
  banque: Banque;
  debut_contrat: Date;
  prets: Array<Pret>;
  assures: Array<Assure>;
  montantValue: String;
  tauxValue: String;
}

export interface SimulationId {
  id_simulation: string
}

interface Formule {
  garantie: Garantie;
  compagnie: string;
  nom_formule: string;
  id_formule: string;
  cout_total_sans_frais: number;
  economies : number;
  cout_moyen_mensuel: number
  taux_moyen_annuel: number
}


export interface SimulationResponse {
  id_simulation: string;
  formules: Array<Formule>;
}

export interface Adhesion {
  id_simulation: string;
  id_result: string;
}

export interface AdhesionResponse {
  url: string;
}
