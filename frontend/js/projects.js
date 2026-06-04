const container = document.getElementById("projects-container");
const form = document.getElementById("project-form");



async function getProjects() {
    
    const response = await fetch(
        `http://127.0.0.1:8000/projects`
    );

    const projects = await response.json();

    container.innerHTML = "";

    projects.forEach(project => {

        const card = document.createElement("div");

        card.classList.add("project-card");

        card.innerHTML = `
        <h3>${project.title}</h3>
        <p>${project.description}</p>
        <p>${project.budget}</p>

        <button onclick="deleteProject(${project.id})">
        Delete </button>
        `;
        
        container.appendChild(card);

    });
}

getProjects();

form.addEventListener("submit", createProject);

async function createProject(event) {

    event.preventDefault();

    const title = document.getElementById("title").value;

    const description = document.getElementById("description").value;

    const budget = document.getElementById("budget").value;
    
    const projectData = {
        title,description,budget
    };

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