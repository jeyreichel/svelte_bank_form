export let backend_url: string,
  front_url: string,
  website_url: string,
  clear_storage = false;

if (process.env.NODE_ENV === "development") {
  backend_url = "https://backend.techfin.lab.inekto.fr";
  clear_storage = true;
  front_url = "http://localhost:5173/";
  website_url = "https://omeros.fr";
} else {
  backend_url = "https://backend.techfin.lab.inekto.fr";
  front_url = "https://techfin.lab.inekto.fr";
  website_url = "https://omeros.fr";
}
