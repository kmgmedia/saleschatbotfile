const API_URL = "/admin";
let adminKey = localStorage.getItem("adminKey");

function authenticate() {
  const key = document.getElementById("adminKey").value;
  if (!key) {
    showError("Please enter admin key");
    return;
  }

  adminKey = key;
  localStorage.setItem("adminKey", key);
  showDashboard();
  refreshDashboard();
}

function logout() {
  localStorage.removeItem("adminKey");
  adminKey = null;
  showAuth();
}

function showAuth() {
  document.getElementById("authSection").style.display = "block";
  document.getElementById("dashboard").classList.remove("active");
}

function showDashboard() {
  document.getElementById("authSection").style.display = "none";
  document.getElementById("dashboard").classList.add("active");
}

function showError(message) {
  const container = document.getElementById("errorContainer");
  container.innerHTML = `<div class="error">${message}</div>`;
  setTimeout(() => {
    container.innerHTML = "";
  }, 5000);
}

function showLoading() {
  document.getElementById("loadingContainer").style.display = "block";
  document.getElementById("contentContainer").style.display = "none";
}

function hideLoading() {
  document.getElementById("loadingContainer").style.display = "none";
  document.getElementById("contentContainer").style.display = "block";
}

async function refreshDashboard() {
  if (!adminKey) {
    showAuth();
    return;
  }

  showLoading();
  const days = document.getElementById("periodSelect").value;

  try {
    const response = await fetch(
      `${API_URL}/dashboard?days=${days}&api_key=${adminKey}`
    );

    if (!response.ok) {
      throw new Error("Unauthorized");
    }

    const result = await response.json();

    if (result.success) {
      renderDashboard(result.data);
      hideLoading();
    } else {
      showError(result.error || "Failed to load dashboard data");
    }
  } catch (error) {
    showError("Failed to load dashboard - check browser console");
    if (error.message === "Unauthorized") {
      logout();
    }
  }
}

function renderDashboard(data) {
  renderMetrics(data.conversion_metrics);
  renderFunnel(data.funnel_analysis);
  renderTopProducts(data.top_products);
}

function renderMetrics(metrics) {
  const grid = document.getElementById("metricsGrid");
  grid.innerHTML = `
    <div class="metric-card">
      <div class="metric-label">Conversion Rate</div>
      <div class="metric-value">${metrics.conversion_rate}%</div>
      <div class="metric-sub">${metrics.conversion_events} conversions</div>
    </div>
    <div class="metric-card">
      <div class="metric-label">Total Events</div>
      <div class="metric-value">${metrics.total_events}</div>
      <div class="metric-sub">User interactions</div>
    </div>
    <div class="metric-card">
      <div class="metric-label">Total Revenue</div>
      <div class="metric-value">$${metrics.total_revenue}</div>
      <div class="metric-sub">AOV: $${metrics.average_order_value}</div>
    </div>
  `;
}

function renderFunnel(funnel) {
  const container = document.getElementById("funnelContainer");
  const stages = [
    { label: "Greeting", value: funnel.greeting },
    {
      label: "Browsing",
      value: funnel.browsing,
      conversion: funnel.browsing_conversion,
    },
    {
      label: "Consideration",
      value: funnel.consideration,
      conversion: funnel.consideration_conversion,
    },
    {
      label: "Purchase",
      value: funnel.purchase,
      conversion: funnel.purchase_conversion,
    },
  ];

  const maxValue = Math.max(...stages.map((s) => s.value));

  container.innerHTML = stages
    .map(
      (stage) => `
        <div class="funnel-stage">
          <div class="funnel-label">
            <span>${stage.label}</span>
            <span>${stage.value} users ${
        stage.conversion ? `(${stage.conversion}% conv.)` : ""
      }</span>
          </div>
          <div class="funnel-bar" style="width: ${
            (stage.value / maxValue) * 100
          }%;">
            ${stage.value}
          </div>
        </div>
      `
    )
    .join("");
}

function renderTopProducts(products) {
  const container = document.getElementById("topProducts");
  if (products.length === 0) {
    container.innerHTML = "<p>No product data available</p>";
    return;
  }

  container.innerHTML = products
    .map(
      (product) => `
        <div class="product-card">
          <div class="product-name">📦 ${product.product_name}</div>
          <div class="product-stat">
            <span class="stat-label">Views:</span>
            <span class="stat-value">${product.total_views}</span>
          </div>
          <div class="product-stat">
            <span class="stat-label">Price Inquiries:</span>
            <span class="stat-value">${product.price_inquiries}</span>
          </div>
          <div class="product-stat">
            <span class="stat-label">Purchase Attempts:</span>
            <span class="stat-value">${product.purchase_attempts}</span>
          </div>
          <div class="product-stat">
            <span class="stat-label">Interest → Action:</span>
            <span class="stat-value">${product.interest_conversion}%</span>
          </div>
        </div>
      `
    )
    .join("");
}

window.addEventListener("load", () => {
  if (adminKey) {
    showDashboard();
    refreshDashboard();
  }
});

setInterval(() => {
  if (
    adminKey &&
    document.getElementById("dashboard").classList.contains("active")
  ) {
    refreshDashboard();
  }
}, 30000);
