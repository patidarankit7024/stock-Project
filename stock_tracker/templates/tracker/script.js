document.getElementById("fetchPortfolio").addEventListener("click", async () => {
    const response = await fetch("/api/portfolio-value/");
    const data = await response.json();
    document.getElementById("portfolioValue").textContent = `Portfolio Value: $${data.portfolio_value}`;
});

document.getElementById("tradeForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    const symbol = document.getElementById("symbol").value;
    const quantity = document.getElementById("quantity").value;
    const action = document.getElementById("action").value;

    const response = await fetch("/api/simulate-trade/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ symbol, quantity, action })
    });
    const data = await response.json();
    document.getElementById("tradeResult").textContent = data.status;
});
