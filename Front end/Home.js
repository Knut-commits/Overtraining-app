document.getElementById("year").textContent = new Date().getFullYear();

const tipsBtn = document.getElementById("tipsBtn");
const tipsModal = document.getElementById("tipsModal");
if (tipsBtn && tipsModal) {
  tipsBtn.addEventListener("click", () => tipsModal.showModal());
  tipsModal.addEventListener("click", (e) => {
    const dialogDimensions = tipsModal.getBoundingClientRect();
    if (
      e.clientX < dialogDimensions.left ||
      e.clientX > dialogDimensions.right ||
      e.clientY < dialogDimensions.top ||
      e.clientY > dialogDimensions.bottom
    ) {
      tipsModal.close();
    }
  });
}

const dashboard = document.getElementById("dashboard");
const scoreNumber = document.getElementById("scoreNumber");
const scoreDescriptor = document.getElementById("scoreDescriptor");
const chartHint = document.getElementById("chartHint");

async function fetchJSON(url, opts = {}) {
  const res = await fetch(url, {
    ...opts,
    credentials: "include",
    headers: { "Content-Type": "application/json", ...(opts.headers || {}) },
  });
  const data = await res.json().catch(() => ({}));
  return { ok: res.ok, status: res.status, data };
}

async function loadDashboard() {
  const scoreRes = await fetchJSON("http://localhost:5000/score");
  if (!scoreRes.ok) {
    dashboard.hidden = true;
    return;
  }

  dashboard.hidden = false;
  const { score, descriptor } = scoreRes.data || {};
  scoreNumber.textContent = typeof score === "number" ? score.toFixed(1) : "—";
  scoreDescriptor.textContent = descriptor || "—";

  const histRes = await fetchJSON("http://localhost:5000/history");
  if (!histRes.ok || !Array.isArray(histRes.data?.history)) {
    chartHint.textContent = "No history yet — add a daily entry.";
    return;
  }

  const history = histRes.data.history
    .slice(-14)
    .map((d) => ({
      date:
        typeof d.dateinput === "string"
          ? d.dateinput.slice(0, 10)
          : new Date(d.dateinput).toLocaleDateString(),
      score: Number(d.score ?? d.overtraining_score ?? NaN),
    }))
    .filter((d) => !Number.isNaN(d.score));

  if (history.length === 0) {
    chartHint.textContent = "No history yet — add a daily entry.";
    return;
  }

  chartHint.textContent = "";
  renderChart(
    history.map((h) => h.date),
    history.map((h) => h.score)
  );
}

function renderChart(labels, values) {
  const ctx = document.getElementById("trendChart").getContext("2d");
  new Chart(ctx, {
    type: "line",
    data: {
      labels,
      datasets: [
        {
          label: "Score",
          data: values,
          tension: 0.25,
          pointRadius: 3,
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: false },
        tooltip: { mode: "index", intersect: false },
      },
      scales: {
        y: { min: 0, max: 10, title: { display: true, text: "Score (0–10)" } },
        x: { title: { display: true, text: "Date" } },
      },
    },
  });
}

loadDashboard().catch(() => {
  dashboard.hidden = true;
});
