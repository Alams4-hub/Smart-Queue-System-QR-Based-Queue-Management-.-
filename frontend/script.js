const API = "http://127.0.0.1:8000";

// User joins the queue
async function joinQueue() {
    const name = document.getElementById("name").value;
    const service = document.getElementById("service").value;

    const res = await fetch(`${API}/join?name=${name}&service=${service}`, { method: "POST" });
    const data = await res.json();

    document.getElementById("ticket").innerText = "Ticket: " + data.ticket;
    document.getElementById("wait").innerText = "Estimated wait: " + data.estimated_wait + " minutes";
    document.getElementById("qr").src = `data:image/png;base64,${data.qr_ticket}`;
}

// Admin calls next customer
async function nextCustomer() {
    const res = await fetch(`${API}/next`, { method: "POST" });
    const data = await res.json();
    document.getElementById("serving").innerText = "Now Serving: " + data.serving;
}

// Admin live queue display
async function loadQueue() {
    const res = await fetch(`${API}/queue`);
    const queue = await res.json();

    const list = document.getElementById("queueList");
    if (!list) return;
    list.innerHTML = "";

    queue.forEach(ticket => {
        const item = document.createElement("div");
        item.className = "queue-item";
        item.innerText = `Ticket ${ticket.ticket_number} | ${ticket.name} | ${ticket.service_type}`;
        list.appendChild(item);
    });
}

// Refresh queue every 3 seconds
setInterval(loadQueue, 3000);
