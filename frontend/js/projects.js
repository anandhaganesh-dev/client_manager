let editingProjectId = null;
let projectsData = [];

const container = document.getElementById("projects-container");
const form = document.getElementById("project-form");
const submitButton = document.getElementById("submit-btn-project")


async function getProjects() {
    
    const response = await fetch(
        `http://127.0.0.1:8000/projects`
    );

    const projects = await response.json();
    projectsData = projects;

    container.innerHTML = "";

    projects.forEach(project => {

        const card = document.createElement("div");

        card.classList.add("project-card");

        card.innerHTML = `
        <h3>${project.title}</h3>
        <p>${project.description}</p>
        <p>${project.budget}</p>

        <button onclick="editProject(${project.id})">
        Edit </button>

        <button onclick="deleteProject(${project.id})">
        Delete </button>
        `;
        
        container.appendChild(card);

    });
}

getProjects();

form.addEventListener("submit", handleProjectSubmit);

async function handleProjectSubmit(event) {

    event.preventDefault();

    const title = document.getElementById("title").value;
    
    const description = document.getElementById("description").value;

    const budget = document.getElementById("budget").value;

    const status = document.getElementById("status").value;

    const clientId = document.getElementById("client-id").vlaue;
    
    const projectData = {
        title,description,budget,status,clientId: parseInt(clientId)
    };

    if (editingProjectId) {
        await fetch(
        `http://127.0.0.1:8000/project/${editingProjectId}`,
        {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(projectData)
        }
    );
    } else {
        await fetch(
        `http://127.0.0.1:8000/project`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(projectData)
        }
    );
    }

    editingProjectId = null;

    submitButton.textContent = "Add Project"

    form.reset();

    await getProjects();
}

async function deleteProject(projectId) {

    const confirmed = confirm(
        "Are you sure?"
    );

    if(!confirmed) {
        return;
    }

    await fetch(
        `http://127.0.0.1:8000/project/${projectId}`,
        {
            method: "DELETE"
        }
    );

    await getProjects();
    
}

function editProject(id) {
    const project = projectsData.find(
        project => project.id === id
    );
    
    document.getElementById("title").value = project.title;
    document.getElementById("description").value = project.description;
    document.getElementById("budget").value = project.budget;

    editingProjectId = project.id;

    submitButton.textContent = "Update Project";
}

async function loadClientsDropdown() {

    const response = await fetch(
        "http://127.0.0.1:8000/clients"
    );

    const clients = await response.json();

    const select = document.getElementById("client-id");

    select.innerHTML = "";

    clients.forEach(client =>{
        const option = document.createElement("option");

        option.value = client.id;
        option.textContent = `${client.company} (${client.name})`;

        select.appendChild(option);
    });
}

loadClientsDropdown();