const API_BASE_URL = "http://127.0.0.1:8000";

const entityDefinitions = {
    inputs: {
        countId: "inputsCount",
        containerId: "inputsComplexities",
        label: "Input"
    },

    outputs: {
        countId: "outputsCount",
        containerId: "outputsComplexities",
        label: "Output"
    },

    inquiries: {
        countId: "inquiriesCount",
        containerId: "inquiriesComplexities",
        label: "Inquiry"
    },

    files: {
        countId: "filesCount",
        containerId: "filesComplexities",
        label: "File"
    },

    interfaces: {
        countId: "interfacesCount",
        containerId: "interfacesComplexities",
        label: "Interface"
    }
};


// ============================================================
// DOM REFERENCES
// ============================================================

const estimationForm =
    document.getElementById("estimationForm");

const estimateButton =
    document.getElementById("estimateButton");

const status =
    document.getElementById("status");

const results =
    document.getElementById("results");

const projectSelect =
    document.getElementById("projectSelect");

const newProjectFields =
    document.getElementById("newProjectFields");

const projectNameInput =
    document.getElementById("projectName");

const projectDescriptionInput =
    document.getElementById("projectDescription");


// Authentication

const authCard =
    document.getElementById("authCard");

const appCard =
    document.getElementById("appCard");

const authForm =
    document.getElementById("authForm");

const authEmail =
    document.getElementById("authEmail");

const authPassword =
    document.getElementById("authPassword");

const loginButton =
    document.getElementById("loginButton");

const registerButton =
    document.getElementById("registerButton");

const authStatus =
    document.getElementById("authStatus");

const logoutButton =
    document.getElementById("logoutButton");

const userEmail =
    document.getElementById("userEmail");


// Dashboard / navigation

const dashboardButton =
    document.getElementById("dashboardButton");

const newEstimationButton =
    document.getElementById("newEstimationButton");

const dashboardView =
    document.getElementById("dashboardView");

const estimatorView =
    document.getElementById("estimatorView");

const dashboardStatus =
    document.getElementById("dashboardStatus");

const projectList =
    document.getElementById("projectList");


const TOKEN_KEY =
    "software_estimator_access_token";


// ============================================================
// COMPLEXITY CONTROLS
// ============================================================

function createComplexitySelect(
    label,
    index,
    selectedValue = "simple"
) {
    const wrapper =
        document.createElement("div");

    wrapper.className =
        "complexity-row";

    const item =
        document.createElement("label");

    item.className =
        "complexity-item";

    const text =
        document.createElement("span");

    text.className =
        "complexity-label";

    text.textContent =
        `${label} ${index + 1}`;

    const select =
        document.createElement("select");

    select.innerHTML = `
        <option value="simple">Simple</option>
        <option value="average">Average</option>
        <option value="complex">Complex</option>
    `;

    select.value =
        selectedValue;

    item.appendChild(text);
    item.appendChild(select);

    wrapper.appendChild(item);

    return wrapper;
}


function renderComplexities(entityType) {
    const definition =
        entityDefinitions[entityType];

    const countInput =
        document.getElementById(
            definition.countId
        );

    const container =
        document.getElementById(
            definition.containerId
        );

    let count =
        Number.parseInt(
            countInput.value,
            10
        );

    if (
        !Number.isInteger(count) ||
        count < 1
    ) {
        count = 1;
        countInput.value = 1;
    }

    container.innerHTML = "";

    for (let i = 0; i < count; i++) {
        container.appendChild(
            createComplexitySelect(
                definition.label,
                i
            )
        );
    }
}


function setupEntityControls() {
    for (
        const entityType of
        Object.keys(entityDefinitions)
    ) {
        const definition =
            entityDefinitions[entityType];

        const countInput =
            document.getElementById(
                definition.countId
            );

        countInput.addEventListener(
            "input",
            () => {
                renderComplexities(
                    entityType
                );
            }
        );

        renderComplexities(
            entityType
        );
    }
}


function getEntityData(entityType) {
    const definition =
        entityDefinitions[entityType];

    const countInput =
        document.getElementById(
            definition.countId
        );

    const container =
        document.getElementById(
            definition.containerId
        );

    const count =
        Number.parseInt(
            countInput.value,
            10
        );

    const complexities =
        Array.from(
            container.querySelectorAll(
                "select"
            )
        ).map(
            select => select.value
        );

    return {
        count,
        complexities
    };
}


// ============================================================
// ESTIMATION UI
// ============================================================

function setStatus(message) {
    status.textContent =
        message;
}


function showResults(estimation) {
    document.getElementById(
        "resultUfp"
    ).textContent =
        estimation.ufp;

    document.getElementById(
        "resultTcf"
    ).textContent =
        estimation.tcf;

    document.getElementById(
        "resultFp"
    ).textContent =
        Number(
            estimation.fp
        ).toFixed(2);

    document.getElementById(
        "resultEffort"
    ).textContent =
        `${estimation.effort_person_months} person-months`;

    document.getElementById(
        "resultTime"
    ).textContent =
        estimation.time_formatted;

    document.getElementById(
        "resultCost"
    ).textContent =
        new Intl.NumberFormat(
            "en-IN",
            {
                style: "currency",
                currency: "INR",
                maximumFractionDigits: 0
            }
        ).format(
            estimation.cost_rupees
        );

    results.classList.remove(
        "hidden"
    );
}


function clearResults() {
    results.classList.add(
        "hidden"
    );

    document.getElementById(
        "resultUfp"
    ).textContent = "—";

    document.getElementById(
        "resultTcf"
    ).textContent = "—";

    document.getElementById(
        "resultFp"
    ).textContent = "—";

    document.getElementById(
        "resultEffort"
    ).textContent = "—";

    document.getElementById(
        "resultTime"
    ).textContent = "—";

    document.getElementById(
        "resultCost"
    ).textContent = "—";
}


function sleep(milliseconds) {
    return new Promise(
        resolve => {
            setTimeout(
                resolve,
                milliseconds
            );
        }
    );
}


// ============================================================
// PROJECT FORM
// ============================================================

function updateProjectFields() {
    const creatingNewProject =
        projectSelect.value === "new";

    newProjectFields.classList.toggle(
        "hidden",
        !creatingNewProject
    );

    projectNameInput.disabled =
        !creatingNewProject;

    projectDescriptionInput.disabled =
        !creatingNewProject;

    projectNameInput.required =
        creatingNewProject;
}


function resetEstimatorForm() {
    estimationForm.reset();

    projectSelect.value =
        "new";

    updateProjectFields();

    for (
        const entityType of
        Object.keys(entityDefinitions)
    ) {
        renderComplexities(
            entityType
        );
    }

    clearResults();

    setStatus("");
}


// ============================================================
// AUTHENTICATION
// ============================================================

function getAccessToken() {
    return localStorage.getItem(
        TOKEN_KEY
    );
}


function setAccessToken(token) {
    localStorage.setItem(
        TOKEN_KEY,
        token
    );
}


function clearAccessToken() {
    localStorage.removeItem(
        TOKEN_KEY
    );
}


function authHeaders() {
    const token =
        getAccessToken();

    if (!token) {
        return {};
    }

    return {
        Authorization:
            `Bearer ${token}`
    };
}


function showAuthenticatedApp() {
    authCard.classList.add(
        "hidden"
    );

    appCard.classList.remove(
        "hidden"
    );
}


function showLogin() {
    authCard.classList.remove(
        "hidden"
    );

    appCard.classList.add(
        "hidden"
    );
}


function logout() {
    clearAccessToken();

    userEmail.textContent =
        "";

    dashboardStatus.textContent =
        "";

    projectList.innerHTML =
        "";

    showLogin();

    authForm.reset();

    authStatus.textContent =
        "";

    resetEstimatorForm();
}


// ============================================================
// API: PROJECTS
// ============================================================

async function createProject(
    name,
    description
) {
    const response =
        await fetch(
            `${API_BASE_URL}/projects`,
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json",
                    ...authHeaders()
                },

                body: JSON.stringify({
                    name,
                    description
                })
            }
        );

    if (!response.ok) {
        throw new Error(
            `Project creation failed (${response.status}).`
        );
    }

    return response.json();
}


async function getProjects() {
    const response =
        await fetch(
            `${API_BASE_URL}/projects`,
            {
                headers: {
                    ...authHeaders()
                }
            }
        );

    if (!response.ok) {
        throw new Error(
            `Could not load projects (${response.status}).`
        );
    }

    return response.json();
}


async function getProjectEstimations(
    projectId
) {
    const response =
        await fetch(
            `${API_BASE_URL}/projects/${projectId}/estimations`,
            {
                headers: {
                    ...authHeaders()
                }
            }
        );

    if (!response.ok) {
        throw new Error(
            `Could not load estimations for project ${projectId} (${response.status}).`
        );
    }

    return response.json();
}


async function loadProjects(
    selectedProjectId = null
) {
    const projects =
        await getProjects();

    projectSelect.innerHTML = `
        <option value="new">
            Create a new project
        </option>
    `;

    for (
        const project of projects
    ) {
        const option =
            document.createElement(
                "option"
            );

        option.value =
            project.id;

        option.textContent =
            project.name;

        projectSelect.appendChild(
            option
        );
    }

    if (
        selectedProjectId !== null
    ) {
        const matchingProject =
            projects.find(
                project =>
                    project.id ===
                    Number(selectedProjectId)
            );

        if (matchingProject) {
            projectSelect.value =
                String(
                    matchingProject.id
                );
        }
    }

    updateProjectFields();

    return projects;
}


// ============================================================
// API: ESTIMATIONS
// ============================================================

async function createEstimation(
    projectId,
    estimationData
) {
    const response =
        await fetch(
            `${API_BASE_URL}/projects/${projectId}/estimations`,
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json",
                    ...authHeaders()
                },

                body: JSON.stringify(
                    estimationData
                )
            }
        );

    if (!response.ok) {
        throw new Error(
            `Estimation creation failed (${response.status}).`
        );
    }

    return response.json();
}


async function getEstimation(
    estimationId
) {
    const response =
        await fetch(
            `${API_BASE_URL}/estimations/${estimationId}`,
            {
                headers: {
                    ...authHeaders()
                }
            }
        );

    if (!response.ok) {
        throw new Error(
            `Could not retrieve estimation (${response.status}).`
        );
    }

    return response.json();
}


async function waitForEstimation(
    estimationId
) {
    while (true) {
        const estimation =
            await getEstimation(
                estimationId
            );

        if (
            estimation.status ===
            "completed"
        ) {
            return estimation;
        }

        if (
            estimation.status ===
            "failed"
        ) {
            throw new Error(
                "The estimation failed while being processed."
            );
        }

        if (
            estimation.status ===
            "processing"
        ) {
            setStatus(
                "Estimation is being processed..."
            );
        } else {
            setStatus(
                "Estimation queued. Waiting for worker..."
            );
        }

        await sleep(1000);
    }
}


// ============================================================
// API: AUTH
// ============================================================

async function login(
    email,
    password
) {
    const body =
        new URLSearchParams();

    body.set(
        "username",
        email
    );

    body.set(
        "password",
        password
    );

    const response =
        await fetch(
            `${API_BASE_URL}/auth/login`,
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/x-www-form-urlencoded"
                },

                body
            }
        );

    if (!response.ok) {
        throw new Error(
            "Incorrect email or password."
        );
    }

    const data =
        await response.json();

    setAccessToken(
        data.access_token
    );
}


async function register(
    email,
    password
) {
    const response =
        await fetch(
            `${API_BASE_URL}/auth/register`,
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({
                    email,
                    password
                })
            }
        );

    if (!response.ok) {
        let data = {};

        try {
            data =
                await response.json();
        } catch {
            // Ignore JSON parsing failure.
        }

        throw new Error(
            data.detail ||
            "Could not create account."
        );
    }

    return response.json();
}


async function getCurrentUser() {
    const response =
        await fetch(
            `${API_BASE_URL}/auth/me`,
            {
                headers: {
                    ...authHeaders()
                }
            }
        );

    if (!response.ok) {
        throw new Error(
            "Authentication expired."
        );
    }

    return response.json();
}


// ============================================================
// DASHBOARD
// ============================================================

function formatDate(
    dateValue
) {
    if (!dateValue) {
        return "Unknown date";
    }

    const date =
        new Date(dateValue);

    if (
        Number.isNaN(
            date.getTime()
        )
    ) {
        return "Unknown date";
    }

    return new Intl.DateTimeFormat(
        "en-IN",
        {
            dateStyle: "medium",
            timeStyle: "short"
        }
    ).format(date);
}


function formatCurrency(
    value
) {
    if (
        value === null ||
        value === undefined
    ) {
        return "—";
    }

    return new Intl.NumberFormat(
        "en-IN",
        {
            style: "currency",
            currency: "INR",
            maximumFractionDigits: 0
        }
    ).format(value);
}


function formatEstimationValue(
    value,
    suffix = ""
) {
    if (
        value === null ||
        value === undefined
    ) {
        return "—";
    }

    return `${value}${suffix}`;
}


function createEstimationCard(
    estimation
) {
    const card =
        document.createElement(
            "div"
        );

    card.className =
        "estimation-card";


    const header =
        document.createElement(
            "div"
        );

    header.className =
        "estimation-header";


    const title =
        document.createElement(
            "strong"
        );

    title.textContent =
        `Estimation #${estimation.id}`;


    const statusElement =
        document.createElement(
            "span"
        );

    statusElement.className =
        "estimation-status";

    statusElement.textContent =
        estimation.status || "unknown";


    header.appendChild(title);
    header.appendChild(statusElement);


    const summary =
        document.createElement(
            "div"
        );

    summary.className =
        "estimation-summary";


    const values = [
        [
            "Function Points",
            formatEstimationValue(
                estimation.fp
            )
        ],

        [
            "Effort",
            formatEstimationValue(
                estimation.effort_person_months,
                " PM"
            )
        ],

        [
            "Development Time",
            estimation.time_formatted || "—"
        ],

        [
            "Cost",
            formatCurrency(
                estimation.cost_rupees
            )
        ],

        [
            "Created",
            formatDate(
                estimation.created_at
            )
        ],

        [
            "Status",
            estimation.status || "—"
        ]
    ];


    for (
        const [label, value] of
        values
    ) {
        const valueWrapper =
            document.createElement(
                "div"
            );

        valueWrapper.className =
            "estimation-value";


        const labelElement =
            document.createElement(
                "span"
            );

        labelElement.textContent =
            label;


        const valueElement =
            document.createElement(
                "strong"
            );

        valueElement.textContent =
            value;


        valueWrapper.appendChild(
            labelElement
        );

        valueWrapper.appendChild(
            valueElement
        );

        summary.appendChild(
            valueWrapper
        );
    }


    card.appendChild(header);
    card.appendChild(summary);

    return card;
}


function createProjectCard(
    project,
    estimations
) {
    const card =
        document.createElement(
            "article"
        );

    card.className =
        "project-card";


    const header =
        document.createElement(
            "div"
        );

    header.className =
        "project-card-header";


    const information =
        document.createElement(
            "div"
        );


    const title =
        document.createElement(
            "h3"
        );

    title.textContent =
        project.name;


    const description =
        document.createElement(
            "p"
        );

    description.className =
        "project-description";

    description.textContent =
        project.description ||
        "No description provided.";


    information.appendChild(
        title
    );

    information.appendChild(
        description
    );


    const estimateButton =
        document.createElement(
            "button"
        );

    estimateButton.type =
        "button";

    estimateButton.className =
        "nav-button";

    estimateButton.textContent =
        "Estimate This Project";


    estimateButton.addEventListener(
        "click",
        () => {
            showEstimator(
                project.id
            );
        }
    );


    header.appendChild(
        information
    );

    header.appendChild(
        estimateButton
    );


    const estimationContainer =
        document.createElement(
            "div"
        );

    estimationContainer.className =
        "project-estimations";


    if (
        estimations.length === 0
    ) {
        const empty =
            document.createElement(
                "div"
            );

        empty.className =
            "empty-state";

        empty.textContent =
            "No estimations yet for this project.";

        estimationContainer.appendChild(
            empty
        );

    } else {
        for (
            const estimation of
            estimations
        ) {
            estimationContainer.appendChild(
                createEstimationCard(
                    estimation
                )
            );
        }
    }


    card.appendChild(header);
    card.appendChild(
        estimationContainer
    );

    return card;
}


async function loadDashboard() {
    dashboardStatus.textContent =
        "Loading dashboard...";

    projectList.innerHTML =
        "";

    try {
        const projects =
            await getProjects();

        if (
            projects.length === 0
        ) {
            const empty =
                document.createElement(
                    "div"
                );

            empty.className =
                "empty-state";

            const title =
                document.createElement(
                    "strong"
                );

            title.textContent =
                "No projects yet.";


            const message =
                document.createElement(
                    "span"
                );

            message.textContent =
                "Create your first project by starting a new estimation.";


            empty.appendChild(title);
            empty.appendChild(message);

            projectList.appendChild(
                empty
            );

            dashboardStatus.textContent =
                "";

            return;
        }


        for (
            const project of projects
        ) {
            const estimations =
                await getProjectEstimations(
                    project.id
                );

            const projectCard =
                createProjectCard(
                    project,
                    estimations
                );

            projectList.appendChild(
                projectCard
            );
        }

        dashboardStatus.textContent =
            "";

    } catch (error) {
        console.error(error);

        dashboardStatus.textContent =
            error.message ||
            "Could not load dashboard.";
    }
}


// ============================================================
// VIEW NAVIGATION
// ============================================================

function showDashboard() {
    dashboardView.classList.remove(
        "hidden"
    );

    estimatorView.classList.add(
        "hidden"
    );

    loadDashboard();
}


function showEstimator(
    projectId = null
) {
    dashboardView.classList.add(
        "hidden"
    );

    estimatorView.classList.remove(
        "hidden"
    );


    clearResults();
    setStatus("");


    if (
        projectId !== null
    ) {
        projectSelect.value =
            String(projectId);

        updateProjectFields();

    } else {
        resetEstimatorForm();
    }


    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });
}


// ============================================================
// AUTH EVENTS
// ============================================================

logoutButton.addEventListener(
    "click",
    logout
);


dashboardButton.addEventListener(
    "click",
    () => {
        showDashboard();
    }
);


newEstimationButton.addEventListener(
    "click",
    () => {
        showEstimator();
    }
);


authForm.addEventListener(
    "submit",
    async (event) => {
        event.preventDefault();

        loginButton.disabled =
            true;

        registerButton.disabled =
            true;

        authStatus.textContent =
            "Signing in...";

        try {
            await login(
                authEmail.value.trim(),
                authPassword.value
            );

            const user =
                await getCurrentUser();

            userEmail.textContent =
                user.email;

            authStatus.textContent =
                "";

            showAuthenticatedApp();

            await loadProjects();

            showDashboard();

        } catch (error) {
            console.error(error);

            clearAccessToken();

            authStatus.textContent =
                error.message ||
                "Could not sign in.";

            showLogin();

        } finally {
            loginButton.disabled =
                false;

            registerButton.disabled =
                false;
        }
    }
);


registerButton.addEventListener(
    "click",
    async () => {
        const email =
            authEmail.value.trim();

        const password =
            authPassword.value;

        if (
            !email ||
            !password
        ) {
            authStatus.textContent =
                "Enter an email and password first.";

            return;
        }


        loginButton.disabled =
            true;

        registerButton.disabled =
            true;

        authStatus.textContent =
            "Creating account...";


        try {
            await register(
                email,
                password
            );

            authStatus.textContent =
                "Account created. Signing in...";


            await login(
                email,
                password
            );


            const user =
                await getCurrentUser();


            userEmail.textContent =
                user.email;

            authStatus.textContent =
                "";

            showAuthenticatedApp();

            await loadProjects();

            showDashboard();

        } catch (error) {
            console.error(error);

            clearAccessToken();

            authStatus.textContent =
                error.message ||
                "Could not create account.";

        } finally {
            loginButton.disabled =
                false;

            registerButton.disabled =
                false;
        }
    }
);


// ============================================================
// ESTIMATION EVENTS
// ============================================================

projectSelect.addEventListener(
    "change",
    updateProjectFields
);


estimationForm.addEventListener(
    "submit",
    async (event) => {
        event.preventDefault();

        estimateButton.disabled =
            true;

        results.classList.add(
            "hidden"
        );


        try {
            let projectId;


            // ----------------------------------------------
            // Create or select project
            // ----------------------------------------------

            if (
                projectSelect.value ===
                "new"
            ) {
                const projectName =
                    projectNameInput.value.trim();

                const projectDescription =
                    projectDescriptionInput
                        .value
                        .trim();


                if (!projectName) {
                    throw new Error(
                        "Project name is required."
                    );
                }


                setStatus(
                    "Creating project..."
                );


                const project =
                    await createProject(
                        projectName,
                        projectDescription ||
                        null
                    );


                projectId =
                    project.id;


                // Refresh project dropdown so the
                // newly created project is available.
                await loadProjects(
                    projectId
                );

            } else {
                projectId =
                    Number.parseInt(
                        projectSelect.value,
                        10
                    );
            }


            // ----------------------------------------------
            // Build estimation payload
            // ----------------------------------------------

            const estimationData = {
                inputs:
                    getEntityData(
                        "inputs"
                    ),

                outputs:
                    getEntityData(
                        "outputs"
                    ),

                inquiries:
                    getEntityData(
                        "inquiries"
                    ),

                files:
                    getEntityData(
                        "files"
                    ),

                interfaces:
                    getEntityData(
                        "interfaces"
                    ),

                environment_complexity:
                    Number.parseInt(
                        document.getElementById(
                            "environmentComplexity"
                        ).value,
                        10
                    ),

                project_mode:
                    document.getElementById(
                        "projectMode"
                    ).value,

                language:
                    document.getElementById(
                        "language"
                    ).value,

                salary_per_month:
                    Number.parseInt(
                        document.getElementById(
                            "salary"
                        ).value,
                        10
                    ),

                team_size:
                    Number.parseInt(
                        document.getElementById(
                            "teamSize"
                        ).value,
                        10
                    )
            };


            // ----------------------------------------------
            // Submit estimation
            // ----------------------------------------------

            setStatus(
                "Submitting estimation..."
            );


            const estimation =
                await createEstimation(
                    projectId,
                    estimationData
                );


            setStatus(
                "Estimation queued. Waiting for worker..."
            );


            const completedEstimation =
                await waitForEstimation(
                    estimation.id
                );


            showResults(
                completedEstimation
            );


            setStatus(
                "Estimation completed."
            );

        } catch (error) {
            console.error(error);

            setStatus(
                error.message ||
                "Something went wrong."
            );

        } finally {
            estimateButton.disabled =
                false;
        }
    }
);


// ============================================================
// APPLICATION INITIALIZATION
// ============================================================

async function initializeApp() {
    setupEntityControls();

    updateProjectFields();


    const token =
        getAccessToken();


    if (!token) {
        showLogin();
        return;
    }


    try {
        const user =
            await getCurrentUser();

        userEmail.textContent =
            user.email;

        showAuthenticatedApp();

        await loadProjects();

        showDashboard();

    } catch (error) {
        console.error(error);

        clearAccessToken();

        showLogin();
    }
}


initializeApp();