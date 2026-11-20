
const packetForm = document.getElementById("packetForm");

packetForm.addEventListener("submit", async function(event) {

    event.preventDefault();

    const resultBox = document.getElementById("result");
    const decision = document.getElementById("decision");
    const reason = document.getElementById("reason");

    const formData = new FormData(packetForm);

    resultBox.style.display = "block";
    decision.textContent = "Checking packet...";
    reason.textContent = "Evaluating firewall rules.";

    try {

        const response = await fetch("/test_packet", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Request failed");
        }

        decision.textContent = data.decision;
        reason.textContent = data.reason;

        if (data.decision === "ALLOW") {

            resultBox.style.borderLeft = "5px solid #22c55e";
            decision.style.color = "#4ade80";

        } else {

            resultBox.style.borderLeft = "5px solid #ef4444";
            decision.style.color = "#f87171";

        }

        // Refresh logs and dashboard statistics
        setTimeout(() => {
            window.location.reload();
        }, 1200);

    } catch (error) {

        decision.textContent = "ERROR";
        reason.textContent = error.message;
        decision.style.color = "#f87171";

    }

});
