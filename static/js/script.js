const apiBase = "/api/catalogues";

const form = document.getElementById("catalogue-form");
const tableBody = document.querySelector("#catalogue-table tbody");
const msgBox = document.getElementById("global-msg");
const formMsg = document.getElementById("form-msg");

const catalogueIdField = document.getElementById("catalogue-id");
const nameField = document.getElementById("name");
const descField = document.getElementById("description");
const startDateField = document.getElementById("start_date");
const endDateField = document.getElementById("end_date");
const statusField = document.getElementById("status");

const searchIdInput = document.getElementById("search-id");
const searchButton = document.getElementById("btn-search-id");
const showFormButton = document.getElementById("btn-show-form");
const cancelButton = document.getElementById("btn-cancel");

const filters = document.querySelectorAll(".filter");
const pagination = document.getElementById("pagination");
const pageInfo = document.getElementById("page-info");
const prevPage = document.getElementById("prev-page");
const nextPage = document.getElementById("next-page");

let currentCatalogues = [];
let currentPage = 1;
const itemsPerPage = 8;
let currentFilter = "all";

function showMessage(msg, isSuccess = true, targetBox = msgBox) {
  targetBox.textContent = msg;
  targetBox.className = isSuccess ? "message success show" : "message error show";

  setTimeout(() => {
    targetBox.className = "message";
    targetBox.textContent = "";
  }, 4000);
}


function renderTable(data) {
  tableBody.innerHTML = "";
  data.forEach(c => {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${c.catalogue_id ?? "N/A"}</td>
      <td>${c.name}</td>
      <td>${c.description}</td>
      <td>${c.start_date}</td>
      <td>${c.end_date}</td>
      <td class="${c.status === 'active' ? 'status-active' : 'status-inactive'}">${c.status}</td>

      <td>
          <button class="btn btn-secondary tooltip" data-tooltip="Edit" onclick="editCatalogue(${c.catalogue_id})">✏️</button>
           <button class="btn btn-secondary tooltip" data-tooltip="Delete" onclick="deleteCatalogue(${c.catalogue_id})">🗑️</button>
      </td>

    `;
    tableBody.appendChild(row);
  });
}

function filterAndPaginate() {
  let filtered = [...currentCatalogues];

  if (currentFilter !== "all") {
    filtered = filtered.filter(c => c.status === currentFilter);
    pagination.style.display = "none";
  } else {
    pagination.style.display = "flex";
  }

  const start = (currentPage - 1) * itemsPerPage;
  const paginated = currentFilter === "all" ? filtered.slice(start, start + itemsPerPage) : filtered;
  renderTable(paginated);
  pageInfo.textContent = `Page ${currentPage} of ${Math.ceil(filtered.length / itemsPerPage)}`;
}

function fetchAllCatalogues() {
  fetch(apiBase)
    .then(res => res.json())
    .then(data => {
      currentCatalogues = data.sort((a, b) => b.catalogue_id - a.catalogue_id); // newest first
      currentPage = 1;
      filterAndPaginate();
    })
    .catch(() => showMessage("Error loading catalogues", false));
}

function fetchCatalogueById(id) {
  fetch(`${apiBase}/${id}`)
    .then(res => res.ok ? res.json() : Promise.reject("Not found"))
    .then(data => {
      renderTable([data]);
      pagination.style.display = "none";
      filters.forEach(btn => btn.classList.remove("active"));
    })
    .catch(() => showMessage("Catalogue not found", false));
}

function deleteCatalogue(id) {
  fetch(`${apiBase}/${id}`, { method: "DELETE" })
    .then(res => res.json().then(d => ({ ok: res.ok, data: d })))
    .then(({ ok, data }) => {
      if (ok) {
        showMessage(data.message);
        fetchAllCatalogues();
      } else {
        showMessage(data.error || data.message || "Unable to delete", false);
      }
    })
    .catch(() => showMessage("Delete request failed", false));
}

function editCatalogue(id) {
  fetch(`${apiBase}/${id}`)
    .then(res => res.json())
    .then(data => {
      catalogueIdField.value = id;
      nameField.value = data.name;
      descField.value = data.description;
      startDateField.value = data.start_date;
      endDateField.value = data.end_date;
      statusField.value = data.status;
      form.classList.remove("hidden");
    })
    .catch(() => showMessage("Error loading catalogue data", false));
}

form.addEventListener("submit", e => {
  e.preventDefault();
  formMsg.textContent = "";

  const id = catalogueIdField.value;
  const payload = {
    name: nameField.value.trim(),
    description: descField.value.trim(),
    start_date: startDateField.value,
    end_date: endDateField.value,
    status: statusField.value
  };

  const method = id ? "PUT" : "POST";
  const url = id ? `${apiBase}/${id}` : apiBase;

  fetch(url, {
    method,
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  })
    .then(res => res.json().then(d => ({ ok: res.ok, data: d })))
    .then(({ ok, data }) => {
      if (ok) {
        showMessage(data.message);
        form.reset();
        form.classList.add("hidden");
        fetchAllCatalogues();
      } else {
        showMessage(data.error || data.message || "Failed to save", false, formMsg);
      }
    })
    .catch(() => showMessage("Request failed", false, formMsg));
});

filters.forEach(btn => {
  btn.addEventListener("click", () => {
    filters.forEach(b => b.classList.remove("active"));
    btn.classList.add("active");
    currentFilter = btn.dataset.status;
    currentPage = 1;
    filterAndPaginate();
  });
});

searchButton.addEventListener("click", () => {
  const id = parseInt(searchIdInput.value);
  if (id) fetchCatalogueById(id);
});

showFormButton.addEventListener("click", () => {
  form.reset();
  catalogueIdField.value = "";
  form.classList.remove("hidden");
});

cancelButton.addEventListener("click", () => {
  form.reset();
  form.classList.add("hidden");
});

prevPage.addEventListener("click", () => {
  if (currentPage > 1) {
    currentPage--;
    filterAndPaginate();
  }
});

nextPage.addEventListener("click", () => {
  const total = currentCatalogues.filter(c => currentFilter === "all" || c.status === currentFilter).length;
  if (currentPage < Math.ceil(total / itemsPerPage)) {
    currentPage++;
    filterAndPaginate();
  }
});

fetchAllCatalogues();
