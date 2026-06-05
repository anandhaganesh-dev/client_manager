let editingClientId = null;
let clientsData = [];

const container = document.getElementById("clients-container");
const form = document.getElementById("client-form");
const submitButton = document.getElementById("submit-btn-client");


async function getClients() {
    
    const response = await fetch(
        `http://127.0.0.1:8000/clients`
    );

    const clients = await response.json();
    clientsData = clients;

    container.innerHTML = "";

    clients.forEach(client => {

        const card = document.createElement("div");

        card.classList.add("client-card");

        card.innerHTML = `
        <h3>${client.name}</h3>
        <p>${client.email}</p>
        <p>${client.company}</p>

        <button onclick="editClient(${client.id})">
        Edit </button>

        <button onclick="deleteClient(${client.id})">
        Delete </button>
        `;
        
        container.appendChild(card);

    });
}

getClients();

form.addEventListener("submit", handleClientSubmit);

async function handleClientSubmit(event) {

    event.preventDefault();

    const name = document.getElementById("name").value;

    const email = document.getElementById("email").value;

    const company = document.getElementById("company").value;
    
    const clientData = {
        name, email, company
    };

    if (editingClientId) {
        await fetch(
        `http://127.0.0.1:8000/client/${editingClientId}`,
        {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(clientData)
        }
    );
    } else {
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
    }

    editingClientId = null;

    submitButton.textContent = "Add Client";

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

function editClient(id) {
    const client = clientsData.find(
        client => client.id === id
    );
    
    document.getElementById("name").value = client.name;
    document.getElementById("email").value = client.email;
    document.getElementById("company").value = client.company;

    editingClientId = client.id;

    submitButton.textContent = "Update Client";
}

