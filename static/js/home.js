document.addEventListener("DOMContentLoaded", () => {
    const menuItems = document.querySelectorAll(".menu-item");
    const contentArea = document.getElementById("content-area");

    menuItems.forEach(item => {
        item.addEventListener("click", () => {

            // Active menu
            menuItems.forEach(i => i.classList.remove("active"));
            item.classList.add("active");

            const view = item.getAttribute("data-view");

            // Contenu dynamique (placeholder)
            if (view === "formulaire") {
                contentArea.innerHTML = "<h2>Formulaire (Matrice)</h2><p>Module de saisie à venir.</p>";
            }

            if (view === "dashboard") {
                contentArea.innerHTML = "<h2>Tableau de bord</h2><p>Graphiques et indicateurs ici.</p>";
            }

            if (view === "profile") {
                contentArea.innerHTML = "<h2>Profil utilisateur</h2><p>Informations du compte.</p>";
            }

            if (view === "cartes") {
                contentArea.innerHTML = "<h2>Cartes</h2><p>Visualisation cartographique.</p>";
            }
        });
    });
});
