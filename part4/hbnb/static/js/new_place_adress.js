const addressInput = document.getElementById("new-place-address");

addressInput.addEventListener("blur", async () => {
  const address = addressInput.value.trim();
  if (!address) return;

  try {
    const res = await fetch("/geocode-address", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({ address }),
    });

    const text = await res.text();
    let data;

    try {
      data = JSON.parse(text);
    } catch (jsonError) {
      console.error("Réponse non-JSON :", text);
      alert("Erreur : réponse invalide du serveur.");
      return;
    }

    if (!res.ok) {
      alert("Erreur serveur : " + (data.error || res.status));
      return;
    }

    // Vérifie que les valeurs existent bien
    if (!data.lat || !data.lon) {
      alert("Adresse non reconnue.");
      return;
    }

    const latInput = document.getElementById("new-place-latitude");
    const lonInput = document.getElementById("new-place-longitude");

    if (!latInput || !lonInput) {
    console.error("Un des champs hidden est manquant !");
    alert("Erreur interne : champs d'adresse manquants.");
    return;
    }

    latInput.value = data.lat;
    lonInput.value = data.lon;

  } catch (e) {
    console.error("Erreur réseau :", e);
    alert("Erreur réseau ou serveur inaccessible.");
  }
});