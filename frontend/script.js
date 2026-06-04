const container = document.getElementById("clients-container");
const form = document.getElementById("client-form");



async function getClients() {
    
    const response = await fetch(
        `http://127.0.0.1:8000/clients`
    );

    const clients = await response.json();

    container.innerHTML = "";

    clients.forEach(client => {

        const card = document.createElement("div");

        card.classList.add("client-card");

        card.innerHTML = `
        <h3>${client.name}</h3>
        <p>${client.email}</p>
        <p>${client.company}</p>

        <button onclick="deleteClient(${client.id})">
        Delete </button>
        `;
        
        container.appendChild(card);

    });
}

getClients();

form.addEventListener("submit", createClient);

async function createClient(event) {

    event.preventDefault();

    const name = document.getElementById("name").value;

    const email = document.getElementById("email").value;

    const company = document.getElementById("company").value;
    
    const clientData = {
        name, email, company
    };

    await fetch(
        `http://127.0.0.1:8000/client`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(clientData)
        }
    );

    form.reset();

    await getClients();
}

async function deleteClient(clientId) {

    const confirmed = confirm(
        "Are you sure?"
    );

    if(!confirmed) {
        return;
    }

    await fetch(
        `http://127.0.0.1:8000/client/${clientId}`,
        {
            method: "DELETE"
        }
    );

    await getClients();
    
}