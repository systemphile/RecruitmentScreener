document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("answer-form");
  if (form) {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const data = {};
      new FormData(form).forEach((val, key) => (data[key] = val));

      try {
        const response = await fetch("/api/answers/", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(data),
        });
        if (response.ok) {
          alert("Answers submitted!");
          window.location.href = "/";
        } else {
          alert("Error submitting answers.");
        }
      } catch (err) {
        console.error(err);
      }
    });
  }
});